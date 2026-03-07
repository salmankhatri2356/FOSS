# ================================================================
# db.py — Google Sheets Database Layer
# Saare read/write operations yahan hain
# ================================================================

import re, logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

import gspread
from google.oauth2.service_account import Credentials
from gspread.exceptions import SpreadsheetNotFound, WorksheetNotFound

from config import GOOGLE_CREDS, SCOPES, MASTER_SHEET, ADMIN_GMAIL, TRIAL_DAYS
from utils import now_ist, safe_float, safe_int, IST

logger = logging.getLogger(__name__)

# ── Tab headers ───────────────────────────────────────────────
HDR = {
    "agents":  ["agent_id","agent_name","phone","telegram_id","sheet_name",
                 "rate_per_app","qr_file_id","joined_at","status",
                 "total_apps","total_clients","trial_end"],
    "logs":    ["event","agent","detail","timestamp"],

    "clients": ["client_code","full_name","phone","telegram_id",
                "joined_at","status","total_apps","balance"],
    "applications": ["app_id","app_no","dob","password","client_code",
                     "agent_id","created_at","status","done_at","balance_deducted"],
    "payments": ["payment_id","client_code","amount_paid","balance_added",
                 "payment_date","payment_time","status","approved_by","approved_at"],
    "agent_logs": ["event","user","role","time","details"],
    "settings": ["key","value"],
}

# ── Colors ────────────────────────────────────────────────────
COLORS = {
    "green":  {"red": 0.72, "green": 0.96, "blue": 0.73},
    "yellow": {"red": 1.0,  "green": 0.98, "blue": 0.80},
    "red":    {"red": 1.0,  "green": 0.80, "blue": 0.80},
    "blue":   {"red": 0.80, "green": 0.90, "blue": 1.0},
}

STATUS_COLOR = {
    "done": "green", "paid": "green", "active": "green", "approved": "green",
    "pending": "yellow", "trial": "yellow",
    "blocked": "red", "rejected": "red", "expired": "red", "deleted": "red",
}


# ── Sheet Manager ─────────────────────────────────────────────
class DB:
    def __init__(self):
        self._gc = None

    # ── Connection ──
    def connect(self) -> bool:
        try:
            creds   = Credentials.from_service_account_info(GOOGLE_CREDS, scopes=SCOPES)
            self._gc = gspread.authorize(creds)
            logger.info("✅ Google Sheets connected")
            return True
        except Exception as e:
            logger.error(f"connect error: {e}")
            return False

    def _client(self):
        if not self._gc:
            self.connect()
        return self._gc

    # ── Open / Create spreadsheet ──
    def open(self, name: str):
        try:
            return self._client().open(name)
        except SpreadsheetNotFound:
            return None
        except Exception:
            try:
                self.connect()
                return self._client().open(name)
            except Exception:
                return None

    def create(self, name: str):
        try:
            sh = self._client().create(name)
            # Share with service account + admin Gmail
            sh.share(GOOGLE_CREDS["client_email"], perm_type="user", role="writer", notify=False)
            try:
                sh.share(ADMIN_GMAIL, perm_type="user", role="writer", notify=False)
            except Exception:
                pass
            return sh
        except Exception as e:
            logger.error(f"create error {name}: {e}")
            return None

    # ── Worksheet helpers ──
    def ws(self, sh, tab: str):
        try:
            return sh.worksheet(tab)
        except WorksheetNotFound:
            return None

    def ensure_ws(self, sh, tab: str):
        w = self.ws(sh, tab)
        if w is None:
            try:
                cols = len(HDR.get(tab, [])) + 2
                w = sh.add_worksheet(tab, rows=2000, cols=cols)
                hdrs = HDR.get(tab, [])
                if hdrs:
                    w.append_row(hdrs)
            except Exception as e:
                logger.error(f"ensure_ws {tab}: {e}")
        return w

    def color(self, ws, row: int, status: str):
        try:
            key   = STATUS_COLOR.get(status.lower(), "blue")
            bg    = COLORS[key]
            ncols = len(ws.row_values(1))
            ec    = chr(64 + min(ncols, 26))
            ws.format(f"A{row}:{ec}{row}", {
                "backgroundColor": bg,
                "horizontalAlignment": "CENTER",
            })
        except Exception:
            pass

    # ── Generic row finder ──
    def find_row(self, ws, col_idx: int, value: str):
        """Returns (row_index, row_values) or (None, None). col_idx is 0-based."""
        try:
            for i, row in enumerate(ws.get_all_values()[1:], start=2):
                if len(row) > col_idx and str(row[col_idx]) == str(value):
                    return i, row
        except Exception:
            pass
        return None, None

    def update_field(self, ws, key_col: int, key_val: str, field: str, value) -> bool:
        try:
            headers = ws.row_values(1)
            if field not in headers:
                return False
            fc = headers.index(field) + 1
            ri, _ = self.find_row(ws, key_col, key_val)
            if ri is None:
                return False
            ws.update_cell(ri, fc, value)
            return True
        except Exception as e:
            logger.error(f"update_field {field}: {e}")
            return False


db = DB()


# ================================================================
# MASTER SHEET — Agents
# ================================================================

def _master():
    sh = db.open(MASTER_SHEET)
    return sh

def _aws():   # agents worksheet
    sh = _master()
    return db.ws(sh, "agents") if sh else None

def _mlws():  # master logs worksheet
    sh = _master()
    return db.ws(sh, "logs") if sh else None


def all_agents() -> list[dict]:
    try:
        w = _aws()
        return w.get_all_records() if w else []
    except Exception:
        return []


def agent_by_tid(tid: int) -> dict | None:
    for a in all_agents():
        if str(a.get("telegram_id","")) == str(tid):
            return a
    return None


def agent_by_id(aid: str) -> dict | None:
    for a in all_agents():
        if a.get("agent_id","") == aid:
            return a
    return None


def add_agent(data: dict) -> bool:
    try:
        w = _aws()
        if w is None:
            return False
        trial_end = (datetime.now(IST) + timedelta(days=TRIAL_DAYS)).strftime("%Y-%m-%d")
        row = [
            data["agent_id"], data["agent_name"], data["phone"],
            data["telegram_id"], data["sheet_name"], data["rate"],
            "", now_ist(), "trial", 0, 0, trial_end,
        ]
        w.append_row(row)
        try:
            db.color(w, len(w.get_all_values()), "trial")
        except Exception:
            pass
        master_log("AGENT_ADDED", data["agent_name"], f"ID:{data['agent_id']} trial:{trial_end}")
        return True
    except Exception as e:
        logger.error(f"add_agent: {e}")
        return False


def set_agent_field(agent_id: str, field: str, value) -> bool:
    w = _aws()
    if w is None:
        return False
    return db.update_field(w, 0, agent_id, field, value)


def remove_agent(agent_id: str) -> bool:
    try:
        w = _aws()
        if w is None:
            return False
        ri, _ = db.find_row(w, 0, agent_id)
        if ri:
            w.delete_rows(ri)
            return True
    except Exception as e:
        logger.error(f"remove_agent: {e}")
    return False


def master_log(event: str, agent: str, detail: str):
    try:
        w = _mlws()
        if w:
            w.append_row([event, agent, detail, now_ist()])
    except Exception:
        pass


def agent_status(agent: dict) -> str:
    """Returns: active | trial | expired | blocked | deleted"""
    st = str(agent.get("status", "active"))
    if st in ("blocked", "deleted", "expired"):
        return st
    if st == "trial":
        te = str(agent.get("trial_end", ""))
        if te:
            try:
                ed = datetime.strptime(te, "%Y-%m-%d").replace(tzinfo=IST)
                if datetime.now(IST) > ed:
                    return "expired"
            except Exception:
                pass
    return st


def trial_end_date(days=TRIAL_DAYS) -> str:
    return (datetime.now(IST) + timedelta(days=days)).strftime("%Y-%m-%d")


# ================================================================
# AGENT SHEET — Setup
# ================================================================

def make_agent_sheet(agent_name: str, tid: str) -> str | None:
    safe = re.sub(r'[^a-zA-Z0-9]', '', agent_name)[:14]
    name = f"FOS_{safe}_{tid}"
    # If exists, return as is
    if db.open(name):
        return name
    sh = db.create(name)
    if sh is None:
        return None
    # Rename default Sheet1 → clients
    try:
        sh.sheet1.update_title("clients")
        sh.worksheet("clients").append_row(HDR["clients"])
    except Exception:
        pass
    for tab in ("applications", "payments", "agent_logs", "settings"):
        db.ensure_ws(sh, tab)
    # Seed settings
    try:
        sw = db.ws(sh, "settings")
        if sw:
            sw.append_row(["rate_per_app", "0"])
            sw.append_row(["qr_file_id",   ""])
            sw.append_row(["agent_name",    agent_name])
    except Exception:
        pass
    return name


# ================================================================
# AGENT SHEET — Helpers
# ================================================================

def _sh(agent: dict):
    return db.open(agent.get("sheet_name", ""))

def _w(agent: dict, tab: str):
    sh = _sh(agent)
    return db.ws(sh, tab) if sh else None


# ── Settings ──
def get_setting(agent: dict, key: str) -> str:
    try:
        w = _w(agent, "settings")
        if w is None:
            return ""
        for row in w.get_all_values():
            if len(row) >= 2 and row[0] == key:
                return str(row[1])
    except Exception:
        pass
    return ""

def put_setting(agent: dict, key: str, val: str) -> bool:
    try:
        w = _w(agent, "settings")
        if w is None:
            return False
        for i, row in enumerate(w.get_all_values(), start=1):
            if len(row) >= 1 and row[0] == key:
                w.update_cell(i, 2, val)
                return True
        w.append_row([key, val])
        return True
    except Exception as e:
        logger.error(f"put_setting {key}: {e}")
        return False


# ── Clients ──
def all_clients(agent: dict) -> list[dict]:
    try:
        w = _w(agent, "clients")
        return w.get_all_records() if w else []
    except Exception:
        return []

def client_by_tid(agent: dict, tid: int) -> dict | None:
    for c in all_clients(agent):
        if str(c.get("telegram_id","")) == str(tid):
            return c
    return None

def client_by_code(agent: dict, code: str) -> dict | None:
    for c in all_clients(agent):
        if c.get("client_code","") == code:
            return c
    return None

def add_client(agent: dict, data: dict) -> bool:
    try:
        w = _w(agent, "clients")
        if w is None:
            return False
        row = [data["client_code"], data["full_name"], data["phone"],
               data["telegram_id"], now_ist(), "active", 0, 0]
        w.append_row(row)
        try:
            db.color(w, len(w.get_all_values()), "active")
        except Exception:
            pass
        agent_log(agent, "CLIENT_REG", data["full_name"], "client", data["client_code"])
        set_agent_field(agent["agent_id"], "total_clients",
                        safe_int(agent.get("total_clients", 0)) + 1)
        return True
    except Exception as e:
        logger.error(f"add_client: {e}")
        return False

def set_client_field(agent: dict, code: str, field: str, value) -> bool:
    w = _w(agent, "clients")
    if w is None:
        return False
    return db.update_field(w, 0, code, field, value)


# ── Balance ──
def get_balance(agent: dict, code: str) -> float:
    c = client_by_code(agent, code)
    return safe_float(c.get("balance", 0)) if c else 0.0

def add_balance(agent: dict, code: str, amount: float) -> bool:
    cur = get_balance(agent, code)
    return set_client_field(agent, code, "balance", round(cur + amount, 2))

def deduct_balance(agent: dict, code: str, amount: float) -> bool:
    cur = get_balance(agent, code)
    if cur < amount:
        return False
    return set_client_field(agent, code, "balance", round(cur - amount, 2))


# ── Applications ──
def all_apps(agent: dict) -> list[dict]:
    try:
        w = _w(agent, "applications")
        return w.get_all_records() if w else []
    except Exception:
        return []

def app_by_id(agent: dict, app_id: str) -> dict | None:
    for a in all_apps(agent):
        if a.get("app_id","") == app_id:
            return a
    return None

def app_exists(agent: dict, app_no: str, code: str) -> bool:
    for a in all_apps(agent):
        if a.get("app_no","") == app_no and a.get("client_code","") == code:
            return True
    return False

def add_app(agent: dict, data: dict) -> bool:
    try:
        w = _w(agent, "applications")
        if w is None:
            return False
        row = [data["app_id"], data["app_no"], data["dob"], data["password"],
               data["client_code"], agent["agent_id"], now_ist(), "PENDING", "", ""]
        w.append_row(row)
        try:
            db.color(w, len(w.get_all_values()), "pending")
        except Exception:
            pass
        agent_log(agent, "APP_SUBMIT", data["client_code"], "client", data["app_id"])
        set_agent_field(agent["agent_id"], "total_apps",
                        safe_int(agent.get("total_apps", 0)) + 1)
        return True
    except Exception as e:
        logger.error(f"add_app: {e}")
        return False

def mark_done(agent: dict, app_id: str) -> bool:
    try:
        w = _w(agent, "applications")
        if w is None:
            return False
        hdrs = w.row_values(1)
        ri, _ = db.find_row(w, 0, app_id)
        if ri is None:
            return False
        w.update_cell(ri, hdrs.index("status") + 1, "DONE")
        w.update_cell(ri, hdrs.index("done_at") + 1, now_ist())
        w.update_cell(ri, hdrs.index("balance_deducted") + 1, "YES")
        db.color(w, ri, "done")
        agent_log(agent, "APP_DONE", "", "agent", app_id)
        return True
    except Exception as e:
        logger.error(f"mark_done: {e}")
        return False

def inc_client_apps(agent: dict, code: str):
    c = client_by_code(agent, code)
    if c:
        set_client_field(agent, code, "total_apps", safe_int(c.get("total_apps", 0)) + 1)


# ── Payments ──
def all_payments(agent: dict) -> list[dict]:
    try:
        w = _w(agent, "payments")
        return w.get_all_records() if w else []
    except Exception:
        return []

def add_payment(agent: dict, data: dict) -> bool:
    try:
        w = _w(agent, "payments")
        if w is None:
            return False
        ts = now_ist().split(" ")
        row = [data["pay_id"], data["client_code"], data["amount"], "",
               ts[0], ts[1] if len(ts) > 1 else "", "PENDING", "", ""]
        w.append_row(row)
        try:
            db.color(w, len(w.get_all_values()), "pending")
        except Exception:
            pass
        return True
    except Exception as e:
        logger.error(f"add_payment: {e}")
        return False

def approve_payment(agent: dict, pay_id: str, by: str) -> bool:
    try:
        w = _w(agent, "payments")
        if w is None:
            return False
        hdrs = w.row_values(1)
        ri, row = db.find_row(w, 0, pay_id)
        if ri is None:
            return False
        w.update_cell(ri, hdrs.index("status") + 1, "PAID")
        amt = row[hdrs.index("amount_paid")] if "amount_paid" in hdrs else ""
        w.update_cell(ri, hdrs.index("balance_added") + 1, amt)
        w.update_cell(ri, hdrs.index("approved_by") + 1, by)
        w.update_cell(ri, hdrs.index("approved_at") + 1, now_ist())
        db.color(w, ri, "paid")
        return True
    except Exception as e:
        logger.error(f"approve_payment: {e}")
        return False

def reject_payment(agent: dict, pay_id: str) -> bool:
    w = _w(agent, "payments")
    if w is None:
        return False
    return db.update_field(w, 0, pay_id, "status", "REJECTED")


# ── Agent Log ──
def agent_log(agent: dict, event: str, user: str, role: str, detail: str):
    try:
        w = _w(agent, "agent_logs")
        if w:
            w.append_row([event, user, role, now_ist(), detail])
    except Exception:
        pass


# ── Role detection ──
def detect_role(tid: int) -> str:
    from config import SUPER_ADMIN_ID
    if tid == SUPER_ADMIN_ID:
        return "admin"
    if agent_by_tid(tid):
        return "agent"
    for ag in all_agents():
        if client_by_tid(ag, tid):
            return "client"
    return "unknown"

def find_client(tid: int):
    """Returns (client_dict, agent_dict) or (None, None)"""
    for ag in all_agents():
        c = client_by_tid(ag, tid)
        if c:
            return c, ag
    return None, None
