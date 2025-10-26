import gspread
from google.oauth2.service_account import Credentials
from pathlib import Path
import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


THIS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = THIS_DIR.parent
SERVICE_ACCOUNT_FILE = PROJECT_ROOT / "credentials" / "service_account.json"

def upload_to_sheet(sheet_id, data):

    if not SERVICE_ACCOUNT_FILE.exists():
        raise FileNotFoundError(
            f"Credenciales no encontradas en: {SERVICE_ACCOUNT_FILE}\n"
            "Coloca tu archivo de credenciales JSON en la carpeta 'credentials' "
            "y asegúrate que se llame 'service_account.json'."
        )

    creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.sheet1

    worksheet.clear()

    if not data:
        worksheet.update("A1", [["No hay datos"]])
        return

    headers = list(data[0].keys())
    rows = [headers] + [[str(d.get(h, "")) for h in headers] for d in data]

    worksheet.update("A1", rows)
    print("Datos enviados correctamente a Google Sheets.")
