import streamlit as st
import pandas as pd
from datetime import datetime
import locale
from dateutil.relativedelta import relativedelta

# try:
#     locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
# except locale.Error:
#     print("⚠️ Locale pt_BR.UTF-8 não disponível no sistema. Usando formato numérico.")

@st.cache_data
def read_excel():
    df = pd.read_excel(r"Bases de Indicadores - Jornada de Segurança 2026 - Todas.xlsx", sheet_name="Previsto x realizado")
    return df

def name_Month(re_month:object) -> str:
    from re import match

    match_month:object = match(r"\d{4}-\d{2}-\d{2}", re_month)[0]

    month_raw:datetime = datetime(*list(map(int,match_month.split('-'))))

    month_str:str = month_raw.strftime("%B")

    return month_str.capitalize()

def colorir_pilar(valor):
    
    cores = {
        "COMPORTAMENTO": "background-color: #FD8C03; color: white;", # Laranja
        "FORNECEDOR": "background-color: #7030A0; color: white;",    # Roxo
        "LIDERANÇA": "background-color: #4472C4; color: white;",     # Azul
        "POPULAÇÃO": "background-color: #5B9BD5; color: white;"      # Azul Claro
    }
    
    return cores.get(valor, '')


def colorir_status(valor):
    
    if valor >= 1.0:
        cor = '#c8e6c9' # Verde (Atingiu a meta)
    elif valor >= 0.5:
        cor = '#fff9c4' # Amarelo (Atenção)
    else:
        cor = "#ff5050" # Vermelho (Abaixo do esperado)
        
    return f'background-color: {cor}; color: #000000;'