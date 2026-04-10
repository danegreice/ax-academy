import os
import asyncio
from datetime import datetime

import gspread
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

def conectar_sheets():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive',
    ]

    creds  = Credentials.from_service_account_file('credentials.json', scopes=scopes)
    client = gspread.authorize(creds)

    planilha = client.open('vagas-escolas')
    aba      = planilha.sheet1

    if not aba.row_values(1):
        aba.append_row(
            ['Data/Hora', 'Escola', 'Endereco', 'Turno', 'Vagas'],
            value_input_option='USER_ENTERED'
        )
        print('Cabeçalho criado na planilha.')

    return aba
    
def ler_planilha(aba):
    dados = aba.get_all_records()
    return dados