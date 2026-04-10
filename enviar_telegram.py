import requests
import json

TOKEN_ID = "8751348429:AAF9mD7yww3StoYg9u9l3OxMMZU2PzJpvQY"
CHAT_ID = "539555901"


def enviar_telegram(msg): 
    url = f"https://api.telegram.org/bot{TOKEN_ID}/sendMessage" 
    payload = { 
        "chat_id": CHAT_ID, 
        "text": msg, 
        "parse_mode": "HTML" 
        } 
    requests.post(url, data=payload) 
    
def formatar_msg(resultados): 
    for r in resultados: 
        if isinstance(r['turnos'], list) and isinstance(r['vagas'], list): 
            for turno, vaga in zip(r['turnos'], r['vagas']): 
                if vaga.isdigit() and int(vaga) > 0: 
                    msg = f""" 
                    <b>VAGA DISPONÍVEL!</b> 
                    <b>Escola:</b> {r['escola']} 
                    <b>Endereço:</b> {r['endereco']} 
                    <b>Turno:</b> {turno} 
                    <b>Vagas:</b> {vaga} 
                    """ 
                    enviar_telegram(msg)
