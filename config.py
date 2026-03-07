# ================================================================
# config.py — FOS Bot Settings
# ================================================================

BOT_TOKEN      = "8555471297:AAFNAyi8VBIERtoHrA46z47cdOcK5sznZ6g"
SUPER_ADMIN_ID = 6806779180
MASTER_SHEET   = "FOS_Master"
ADMIN_GMAIL    = "salmankhatri299@gmail.com"
TRIAL_DAYS     = 3

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Apna service account JSON yahan paste karo
GOOGLE_CREDS = {
  "type": "service_account",
  "project_id": "fos-bot-489505",
  "private_key_id": "420da90f3128e9d1e295353f7d24ac5f9d88f22e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDU1JILivB1ASCu\nX0ibPJMdsBUaxkAG3nuMmkiLygNfRvWjX7/ycC/QsgrxOINN5/LyUPyjnnFVpd9U\nDrxEZtq+qIZS7+dHRY2G25P7JH4YzA+NjwiFXigDzxfCsXkx9TuXydXy49bGXNG3\n+4qiQlp5U1G1OoktiprtC8bjIB7DqXhXklS7hxLj/36Oukj5o7xSP4HlIXAlgQFl\n9LIs+7lCJUnUujcSaobWjDRfHhzQsYsZydKF6PB+b+TdMG02EkQDSAdahaaWtCgy\ntfG1/nAVmYTIAy2umTH3tyahixNvabA9wi72Q8QIgp0ofSKrXsDG98aQgjtyR7+X\n3r256wKdAgMBAAECggEAAdfu2pS918rxCob0F7bNm2s5Xj2rXk6HtBm+A8qgftnG\n1OnGaDDak9cxoGdEk+SCG+E3CapyAYjp8fjICVukDL9kR8xLgjgzAqEHm3GfJKiC\ngKUQMNTg9ITTCDJbV2MavLTYhT29+tfg+n6o88DZYcWmpog27023tn1B9W5YyzRk\n36WxwBSJIID8nRqteAOAby2aTac5Bq3TtHT6C2xlA2JJWDT+9ZlDasVHZPI2MX+k\nzQz2nFJuQuE8M5PeSubZGTNDWzvneI0pMaxox+x9JsoIpMtnMAKGUV8eHTWmddIX\n20h/5ssaueJJzmgd+Abvj05ze5nrtSBMvLSGCVzrTQKBgQDxpM4LSxX8b9i3p+PV\nVemL9nE6OxL0/+/2NM8qSpJpNFdTKXQjErmDV6EhWudjl8+TuzwE3G1l4NihsM6V\nO+tpAFK45kXIJ+TnutP3PN+Iq94yi/wEjcHvVXwWqtmgV8ZZnjMkaxBxgOkrSyC3\n8DucFECMaEh2T2AKsjhhNqFI8wKBgQDheYnIQ13AwHbYmUo+HQ0dj/N+RDN0bS/D\nDyq3Wzkpq88jZJ5kmrlstN75XC4Xmvd6ScPsDIbacoZjukFutFaoezQw6ryepAok\nlTlpaV2N/us6thGw+/2+2Ob2j9QFvtkmMypkTgQv9e4Q5MLrCrN9R4fR9a976G0a\n0FY0k/5qLwKBgQDW0PDO/1gzSub5Fcqn+7EcWOB9qMiIfwI++OF2MkcIOZyr9H0n\nNN0wkvVOZravReUl6txHYgHrAMD0tO5hopv7g2sGrsc4UabgDqmi8D20DT4B54oK\nLk9Kyc7/g7DmJ0HQp5/Fb1x12ujuMOKMQodrkGF1sLtCWfwCZj9SxLMK2wKBgFB/\nuedb1c8JZ+Tw5YbDjHkvebls1AoPKWw0sAWCdigghPWX6Mz2SJk9AhZ5CKO42f44\n89AEsOiw1rYoO1Aw5neEdR+5ztm8qzpgZHzz90jI6GavtiU/8ln+yobg1suuVYzD\n27CwAeK1pOc3JTgRO//QV/doBdzxIHLgSsa+x6hVAoGAQ/HpGXfYmaMPpqyCHKFI\nohLYdef9ba7VFRrpGF6e2UnLw3yII1sIq6rMP3+LOqk9iyS5jZixw/E4Uth5Gh4s\nCndr4AZpQCefNXbvuV6JT1kMoZSy7b6hPtyeKRsiNcMgkFqrBs8yy+Sl8cnI13xQ\n3r6beM7bp/IjaFDIcZ+GcD0=\n-----END PRIVATE KEY-----\n",
  "client_email": "fos-bot@fos-bot-489505.iam.gserviceaccount.com",
  "client_id": "117062468439326604410",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/fos-bot%40fos-bot-489505.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}


# ── Conversation States ──────────────────────────────────────
(REG_NAME, REG_PHONE)    = range(2)
(AA_NAME, AA_PHONE, AA_TID, AA_RATE) = range(10, 14)
(APP_NO, APP_DOB, APP_PASS)          = range(20, 23)
(PAY_AMOUNT, PAY_CONFIRM)            = range(30, 32)
(BC_TYPE, BC_MSG)                    = range(40, 42)   # agent broadcast
(ABC_TYPE, ABC_MSG)                  = range(50, 52)   # admin broadcast
UR_RATE = 60
