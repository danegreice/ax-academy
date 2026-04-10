import os
import sys
import time

from monitor_vagas import pegar_vagas, abrir_portal, iniciar_bot, conectar_ao_maestro, finalizar_task
from recuperar_planilha import conectar_sheets, ler_planilha
from enviar_telegram import formatar_msg, enviar_telegram

def main():
    maestro, task_id, credentials = conectar_ao_maestro()
    bot = iniciar_bot()
    try:
        abrir_portal(bot, 'https://reserva.matriculas.am.gov.br/login')

        print('\nConectando ao Google Sheets...')
        aba = conectar_sheets()
        dados = ler_planilha(aba)

        resultados = pegar_vagas(bot, dados[0], credentials)

        vagas = [
            r for r in resultados
            if isinstance(r['vagas'], list) and any(
                str(v).isdigit() and int(v) > 0 for v in r['vagas']
            )
        ]
        if vagas:
            print(f'\n{len(vagas)} escola(s) com vaga(s) encontrada(s)! Enviando alerta...')
            formatar_msg(vagas)
        else:
            print('\nNenhuma vaga encontrada. Sem alerta.')

    finally:
        #fechar o navegador
        bot.stop_browser()
        #finalizar a task
        finalizar_task(maestro, task_id)


if __name__ == '__main__':
    main()