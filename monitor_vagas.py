import os
import sys
import time

from botcity.web import WebBot, Browser, By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from dotenv import load_dotenv
from botcity.maestro import BotMaestroSDK, AutomationTaskFinishStatus, AlertType, MessageType

load_dotenv()

SERVER = os.getenv('MAESTRO_SERVER')
LOGIN = os.getenv('MAESTRO_LOGIN')
KEY = os.getenv('MAESTRO_KEY')
USUARIO = os.getenv('USUARIO')
SENHA = os.getenv('SENHA')

def conectar_ao_maestro():
    if len(sys.argv) > 1:
        maestro = BotMaestroSDK.from_sys_args()
        task_id = maestro.get_execution().task_id
    else:
        maestro = BotMaestroSDK()
        maestro.login(server=SERVER, login=LOGIN, key=KEY)
        task_id = None
    return maestro, task_id

def iniciar_bot():
    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()
    bot.start_browser()
    return bot

def abrir_portal(bot, url_portal):
    url = str(url_portal).replace("\\", "/")
    bot.browse(url)

def pegar_vagas(bot, dados):
    resultados = []
    
    bot.find_element(selector="cpf", by=By.ID).send_keys(USUARIO)
    bot.find_element(selector="senha", by=By.ID).send_keys(SENHA)
    bot.find_element(selector= "/html/body/div[1]/div/div[2]/main/div/div/div/div/div[1]/div[5]/button[1]", by=By.XPATH).click()

    alunos = bot.find_elements(selector=".card-alunos", by= By.CSS_SELECTOR)

    nome_desejado = dados['Nome'].strip().lower()

    for aluno in alunos:
        try:
            nome = aluno.find_element(By.CSS_SELECTOR, "h3").text.strip().lower()

            if nome == nome_desejado:
                print(f"Encontrado: {nome}")

                aluno.find_element(
                    By.CSS_SELECTOR,
                    ".btn.btn-card.group.btn-reservar-vaga"
                ).click()

        except Exception as e:
            print("Erro ao processar aluno:", e)
            

    time.sleep(3)
    municipio = dados['Municipio'].strip().upper()

    select = Select(bot.find_element("cidade", By.ID, waiting_time=10000))

    for option in select.options:
        if option.text.strip().upper() == municipio:
            option.click()
            break

    time.sleep(3)
    Select(bot.find_element("ensinofase", By.ID, waiting_time=10000)).select_by_index(0)
    
    time.sleep(3)
    bairro = dados['Bairro'].strip().upper()

    select = Select(bot.find_element("bairro", By.ID, waiting_time=10000))

    for option in select.options:
        if option.text.strip().upper() == bairro:
            option.click()
            break

    time.sleep(3)

    escolas = bot.find_elements(selector=".card-escola", by=By.CSS_SELECTOR)
    print(f"{len(escolas)} escolas encontrados.")

    for escola in escolas:
        try:
            nomeEscola = escola.find_element(
                By.CSS_SELECTOR, ".label-escola"
            ).text

            endereco = escola.find_element(
                By.CSS_SELECTOR, ".label-endereco"
            ).text

            botao = escola.find_element(By.CSS_SELECTOR, ".btn.btn-secondary")

            bot.driver.execute_script("arguments[0].scrollIntoView(true);", botao)

            WebDriverWait(bot.driver, 10).until(
                ec.element_to_be_clickable(botao)
            )

            try:
                botao.click()
            except:
                bot.driver.execute_script("arguments[0].click();", botao)

            time.sleep(3)

            turnos = [t.text for t in escola.find_elements(By.CSS_SELECTOR, ".label-turno")]
            vagas = [v.text for v in escola.find_elements(By.CSS_SELECTOR, ".label-vagas")]

        except Exception as e:
            print(e)
            nomeEscola = 'nao tem'
            endereco = 'nao tem'
            turnos = []
            vagas = []

        resultados.append({
            'escola': nomeEscola.strip(),
            'endereco': endereco,
            'turnos': turnos,
            'vagas': vagas
        })
    return resultados

def finalizar_task(maestro, task_id):
    if task_id:
        maestro.finish_task(
            task_id=task_id,
            status=AutomationTaskFinishStatus.SUCCESS,
            message=f"OK"
        )
