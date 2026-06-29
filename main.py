import os
import sys
import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import TimeoutException, WebDriverException

from webdriver_manager.chrome import ChromeDriverManager

from Biblioteca_Protheus.Protheus_Biblioteca import *
from encontrar_id_grupo import *
from verificar_horarios import dados_horarios


# =========================
# SAFE GET (anti-travamento)
# =========================
def safe_get(driver, url, tentativas=3):
    for i in range(tentativas):
        try:
            driver.get(url)
            return True
        except TimeoutException:
            print(f"[WARN] Timeout tentativa {i+1}")
            driver.execute_script("window.stop();")
            time.sleep(3)
        except Exception as e:
            print(f"[ERRO] tentativa {i+1}: {e}")
            time.sleep(3)
    return False


# =========================
# DADOS JSON
# =========================
teste_local = 0

if teste_local == 0:
    raw = sys.argv[1].strip()

    start = raw.find('{')
    end = raw.rfind('}')

    json_str = raw[start:end + 1]
    dados_json = json.loads(json_str)

    print("TESTE DE RECEBIDO: ", dados_json)
else:
    dados_json =  {
        "user":"gustavo.elicker",

        "Domingo":["00:00","23:00"],

        "Terça":["08:00","22:00"],

        "Sábado":["12:00","14:00"]

        }

# =========================
# CONFIG
# =========================
homologacao = False
teste = 0

base_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(base_dir)


# =========================
# CHROME OPTIONS
# =========================
profile_path = r"C:\selenium_chrome_profile"

chrome_options = Options()

# ❌ REMOVIDO PERFIL PARA EVITAR TRAVAMENTO
if teste == 0:
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--remote-debugging-port=9222")

chrome_options.add_argument(f"--user-data-dir={profile_path}")
chrome_options.add_argument("--profile-directory=Default")

chrome_options.add_argument("--window-size=1920,1080")

# estabilidade
chrome_options.add_argument("--no-first-run")
chrome_options.add_argument("--no-default-browser-check")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")

prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)


credenciais = ["robo.horarios", "rbhr2026"]


# =========================
# DRIVER
# =========================
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("chrome://version")
time.sleep(3)

print(driver.find_element(By.TAG_NAME, "body").text)
driver.set_page_load_timeout(180)
driver.set_script_timeout(180)

wait = WebDriverWait(driver, 60)


# =========================
# HELPERS
# =========================
def esperar_load(driver):
    WebDriverWait(driver, 60).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


# =========================
# INÍCIO
# =========================
log("INICIANDO AMBIENTE")

iniciar_ambiente(homologacao, driver)
esperar_load(driver)

log("CONFIRMANDO BASE")
confirmaBase(driver, wait, valor="SIGACFG")

log("REALIZANDO LOGIN")
login(driver, wait, credenciais)

funcao_tres_e_demais(driver, "wa-button", "Fechar")

log("SELECIONANDO AMBIENTE")
sel_ambiente(driver, wait, "02", homologacao, None, None, ambiente_padrão=False)

time.sleep(8)


# =========================
# DIAGNÓSTICO
# =========================
print("\n" + "=" * 80)
print("DIAGNÓSTICO TOTVS")
print("=" * 80)

time.sleep(5)

print("URL:", driver.current_url)
print("TITLE:", driver.title)

print("\nWINDOWS:", driver.window_handles)

try:
    html = driver.execute_script("return document.documentElement.outerHTML;")
    print("POPUP detectado:", "Release Expirando" in html)
except:
    pass


# =========================
# POPUP TESTES
# =========================
try:
    ActionChains(driver).send_keys(Keys.ENTER).perform()
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(1)
    ActionChains(driver).send_keys(Keys.TAB, Keys.ENTER).perform()
except:
    pass


# =========================
# MENU
# =========================
menus_acesso = ["U", "Senhas", "Grupos"]

for menu in menus_acesso:
    funcao_tres_e_demais(driver, "wa-menu-item", menu)


# =========================
# GRUPO
# =========================
print(dados_json)
id_grupo = encontrar_id_grupo(dados_json['user'])
print("ID GRUPO:", id_grupo)

inserir_texto(driver, "COMP7503", id_grupo)

funcao_tres_e_demais(driver, "wa-button", "Confirmar")

esperar_existir(driver, "wa-button", "I")
funcao_tres_e_demais(driver, "wa-button", "A")

esperar_existir(driver, "wa-button", "Confirmar")

driver.find_element(By.ID, "BUTTON-COMP7520").click()


# =========================
# HORÁRIOS
# =========================
dados_horarios(driver, dados_json)


# =========================
# FINALIZAÇÃO
# =========================
log("FINALIZANDO")

time.sleep(5)

try:
    driver.find_element(By.ID, "COMP6014").click()
except:
    pass

time.sleep(3)

encerrar_sistema(driver)

time.sleep(3)

driver.quit()

log("FINALIZADO")