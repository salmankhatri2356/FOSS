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
  "private_key_id": "9025ffa382d3efb56e251bb5d3db548528442a50",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC5K12V4rmOowhw\nX1wkUgz/AXhvrmrYEs1jxIW9cLy/wu/jfbf5L+tSi6DRbwwxXsXv0Ek9wh6CR52T\nCxmRkGf5APPq7t2nHAoITeaj9J6CSYQYpWb6W4xmdo2LRlarSJcbmLHstaseryZh\nJvAYN2TrPKw+owWtoPPA1GDHOIaj5/cmiMXAZqalpmiwJTtAqPSeXsWfydMPq8eA\nEuJgksF1SeK5RO6JhZxBBlIWHUxJkJtRw0FE2A26HdSGy1T9+Nm1Ii0ci/f8KM6y\nSJDwDuVK8GmC4hxpl0Tb497El9RoFDD3vNGOyZ+gCq0s0bGDnP8fEKwzfxBrGQGt\naSRe+PcTAgMBAAECggEAG+KtecyGkDX6J94chLW8kkyY5Ay6t2aBetRWJbTMH/7N\n3I8KvSKbyDcR1WhpSCgTG+3ckcnhiVIap1HFHHhISCX+FbO6OpfM5PpCUQ+eLVW/\n6GxESVCvIKEa6M4DcFECvJuus8yaBAlxeLEB+EujTY+6CsbHLKIwAyqYlnfrQtSC\n/ZjU+qMnSQpKEin+BNDbp5ks3KppwTkPgtX+5eCoD4h97aqgBwGJQy6mZ4HpIRr/\nZIPKDgMLTxS7lR7ZQGHKixTXvfaBIhCJvt3TK06baN29ZChqA9ELKNjnV+OUkNbS\nUuj5gotX2QocdIVdcdWHC8H8qVpKy7+l77kXkdRs5QKBgQDcM39mAA9wqiJbiX4M\ngRC8m9xDDGIGWaVzR0+VMaU5NA464oPOS8OKD0EsYwddfGbNBA4+il+maojormsA\nfhb1oWBOzrsK3f9KDxIoweCa0HBZpZQMVW5qSeEpOJOZXyxFDAAaZ2Z8/kSWzwf+\n/YepddSCB5n3WX8FYNIv29+CtwKBgQDXReOHHSHYK78cRjtGEnVVD+Kw5/U0l1gi\nCI5XjI0sHcllxPjgLsbm0dAaofiXw63zGNOkaICKOIjHHr/MzyzeOznGDnfJPjsO\nteziI8kIzY0qzeO5NGmfckXv0roS2F1ug+J4k6U3ZhPP7Uwaor8AXi5eF24+bp5P\n/jqN+rBihQKBgDLVLI7GasoObHoHJnMKhGuV62YLAMIIhdoz1xpQ6Jxo+PP9AIJq\nGQzQ8rGldrjNFAo16nfjh6sqIsrcINVvRiuUAmCO9rzOfLWC/yUrhIcYoScAw0mJ\nm0CsJ29VoTUhtF2IJKnzvsQSCpFp36Wsr1meWt1dldx06465SCxGLLXHAoGAZuG+\n2L8CgsZ9gmzKPTXrH2kFJRjmZmkCNNmz9YF1oqTlsJ6PdszEQGH7vA62uQlK5Ah0\ndXmAHQ7hx5AZiC9nORpDBTW659G29dPaT0Vc+bkLA278q3GyHQLHC9PBG+qN1Jhx\nLsEZT72YMGIvYfdvoyRfspYuGOZTANX2dA5gJ+UCgYEAobydYs3srdGO9g9M9JPE\nEdg3ypWUST5sHcTu2e87CvKmpeMHfBRrDdDrq/q+JK/yhOCNjoRHcsF3cbfJk9+8\nAXSF7XX79yXL0S6wHHHnnhlg2xywFvRPgwf39BjogWFknTl02vuoanOLX7WTk8Bk\nhOhgYIIhZlnFqGfU/A934bw=\n-----END PRIVATE KEY-----\n",
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
