from Biblioteca_Protheus.Biblioteca_Protheus.Protheus_Biblioteca import *
import os
import sys
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from encontrar_id_grupo import *
from webdriver_manager.chrome import ChromeDriverManager
import sys
import json
import ast
import json
import sys

import json
import sys
teste_local = 0
if teste_local == 0: 
    raw = sys.argv[1]
    raw = raw.encode().decode('unicode_escape').strip()

    start = raw.find('{')
    end = raw.rfind('}')

    json_str = raw[start:end+1]

    dados_json = json.loads(json_str)
    print(dados_json)
else: 
    dados_json = {"user":"gustavo.elicker",

                    "Segunda":["10:00","15:00"],

                    "Sexta":["07:00","22:00"],

                    "Sábado":["10:00","15:00"]

                    }

habilitar_retroativo = False
#verifica data retroativa
if habilitar_retroativo:
    None
    # if hoje.day == 1:
    #     print("iniciar com data retroativa")
    #     dia = hoje.day - 1
    #     mes = hoje.month - 1
    #     ano = hoje.year
    #     # se janeiro, volta para dezembro do ano anterior
    #     if mes == 0:
    #         mes = 12
    #         ano -= 1
    #     nova_data = date(ano, mes, dia)
    #     print("Mês anterior:", nova_data)
    #     print("Mês anterior ajustado:", nova_data.strftime("%d%m%Y"))
    #     DataRetroativa =  nova_data.strftime("%d%m%Y")
    #     print("Data retroativa: ", DataRetroativa)
    #     DataRetroativaBool = True
    # else:
    #     DataRetroativaBool = None
    #     DataRetroativa = None
    #     print("segue normal")
else: 
    DataRetroativaBool = None
    DataRetroativa = None

# =========================
# CORREÇÃO CRÍTICA (AGENDADOR)
# =========================
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(base_dir)


# =========================
# CONFIG
# =========================
homologacao = False
teste = 1

chrome_options = Options()

# =========================
# PERFIL
# =========================
profile_path = os.path.join(base_dir, "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={profile_path}")

# =========================
# MODO EXECUÇÃO
# =========================
if not homologacao and teste == 0:
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    credenciais = ["robo.horarios", "rbhr2026"]

elif not homologacao and teste == 1:
    chrome_options.add_argument("--start-maximized")
    credenciais = ["robo.horarios", "rbhr2026"]

else:
    chrome_options.add_argument("--start-maximized")
    credenciais = ["robo.horarios", "rbhr2026"]

# =========================
# ESTABILIDADE
# =========================
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")

# =========================
# CONFIG EXTRA
# =========================
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--use-fake-ui-for-media-stream")

chrome_options.add_argument(
    "--unsafely-treat-insecure-origin-as-secure=http://protheus.dalba.com.br:1239"
)

# =========================
# PREFS
# =========================
prefs = {
    "profile.default_content_setting_values.notifications": 2
}
chrome_options.add_experimental_option("prefs", prefs)

# =========================
# DRIVER (AUTO + FALLBACK)
# =========================
while True: 
    try:
        # tenta baixar automaticamente
        service = Service(ChromeDriverManager().install())
    except Exception as e:
        print("Erro ao baixar driver automático:", e)
        print("Usando driver local...")

        driver_path = os.path.join(base_dir, "chromedriver.exe")
        service = Service(driver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)

# =========================
# INÍCIO DO FLUXO
# =========================


    log("INICIANDO AMBIENTE")
    iniciar_ambiente(homologacao, driver)
    log("CONFIRMANDO BASE")
    if confirmaBase(driver, wait, valor="SIGACFG"):
        break
    else:    
        driver.quit()
        time.sleep(2)

log("REALIZANDO LOGIN")
login(driver, wait, credenciais)

funcao_tres_e_demais(driver,"wa-button", "Fechar")
log("SELECIONANDO AMBIENTE 02")
sel_ambiente(driver, wait, "02", homologacao, DataRetroativaBool, DataRetroativa,ambiente_padrão=False)

try: 
    funcao_tres_e_demais(driver, "wa-button", "Confirmar")
except: 
    None
time.sleep(5)
#############################################################

# =========================
# testes
# =========================
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

print("\n" + "=" * 80)
print("DIAGNÓSTICO COMPLETO TOTVS")
print("=" * 80)

# Aguarda alguns segundos para garantir que o popup apareceu
time.sleep(5)

# Dados básicos
print("\nURL:", driver.current_url)
print("TITLE:", driver.title)

# Handles
print("\nWINDOW HANDLES:")
print(driver.window_handles)
print("CURRENT HANDLE:", driver.current_window_handle)

# Frames
try:
    print("\nFRAMES:", driver.execute_script("return window.frames.length"))
except Exception as e:
    print("ERRO FRAMES:", e)

# Verificações no DOM
try:
    html = driver.execute_script("""
        return document.documentElement.outerHTML;
    """)

    print("\nCONTÉM 'Release Expirando'? ", "Release Expirando" in html)
    print("CONTÉM 'COMP4517'? ", "COMP4517" in html)
    print("CONTÉM 'Fechar'? ", "Fechar" in html)

except Exception as e:
    print("ERRO HTML:", e)

# Verifica se existe botão com ID
try:
    existe = driver.execute_script("""
        return document.querySelector('#COMP4517') !== null;
    """)
    print("\nCOMP4517 EXISTE:", existe)
except Exception as e:
    print("ERRO COMP4517:", e)

# Lista wa-buttons
try:
    botoes = driver.execute_script("""
        return [...document.querySelectorAll('wa-button')]
            .map(x => ({
                id: x.id,
                texto: x.textContent.trim()
            }));
    """)
    print("\nWA-BUTTONS:")
    print(botoes)
except Exception as e:
    print("ERRO WA-BUTTONS:", e)

# Procura popup em todas as janelas
print("\n" + "=" * 80)
print("VARREDURA DE JANELAS")
print("=" * 80)

for handle in driver.window_handles:
    try:
        driver.switch_to.window(handle)

        print("\nHANDLE:", handle)
        print("TITLE :", driver.title)

        tem_popup = driver.execute_script("""
            return document.body.innerText.includes('Release Expirando')
        """)

        print("TEM POPUP:", tem_popup)

    except Exception as e:
        print("ERRO HANDLE:", e)

# Tenta fechar com ENTER
print("\n" + "=" * 80)
print("TESTE ENTER")
print("=" * 80)

try:
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    print("ENTER enviado")
except Exception as e:
    print("ERRO ENTER:", e)

time.sleep(3)

# Tenta fechar com ESC
print("\n" + "=" * 80)
print("TESTE ESC")
print("=" * 80)

try:
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    print("ESC enviado")
except Exception as e:
    print("ERRO ESC:", e)

time.sleep(3)

# Teste TAB + ENTER (muito comum em popups TOTVS)
print("\n" + "=" * 80)
print("TESTE TAB + ENTER")
print("=" * 80)

try:
    ActionChains(driver).send_keys(Keys.TAB).perform()
    time.sleep(1)

    ActionChains(driver).send_keys(Keys.ENTER).perform()
    print("TAB + ENTER enviado")
except Exception as e:
    print("ERRO TAB+ENTER:", e)

print("\n" + "=" * 80)
print("FIM DOS TESTES")
print("=" * 80)
# =========================
# testes
# =========================
menus_acesso = ["U","Senhas", "Grupos"]
for menu in menus_acesso: 
    funcao_tres_e_demais(driver, "wa-menu-item", menu)

id_grupo = encontrar_id_grupo(dados_json['user'])
print(id_grupo)
time.sleep(3)
inserir_texto(driver,"COMP7503",id_grupo)
time.sleep(3)
funcao_tres_e_demais(driver,"wa-button","Confirmar")
esperar_existir(driver,"wa-button","I")
funcao_tres_e_demais(driver,"wa-button","A")
esperar_existir(driver,"wa-button","Confirmar")
time.sleep(1)
driver.find_element(By.ID, "BUTTON-COMP7520").click()
from verificar_horarios import *

dados_horarios(driver,dados_json)

log("FINALIZANDO")
time.sleep(5)
driver.find_element(By.ID, "COMP6014").click()
time.sleep(5)
encerrar_sistema(driver)
time.sleep(5)
driver.quit()
log("FINALIZADO")