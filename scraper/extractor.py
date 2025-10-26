import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

def extract_pokemon_data(driver):

    try:
        numero_raw = driver.find_element(
            By.CSS_SELECTOR, "div.pokedex-pokemon-pagination-title span.pokemon-number"
        ).get_attribute("innerText").strip()
        numero = re.sub(r"\D", "", numero_raw)
    except NoSuchElementException:
        numero = None

    try:
        nombre_raw = driver.find_element(
            By.CSS_SELECTOR, "div.pokedex-pokemon-pagination-title"
        ).text.strip()
        nombre = re.sub(r"N\.º.*", "", nombre_raw).strip()
    except NoSuchElementException:
        nombre = None

    try:
        tipos_elements = driver.find_elements(By.CSS_SELECTOR, ".dtm-type li")
    
        tipos_list = [li.text.strip() for li in tipos_elements if li.text.strip()]
    
        tipos = "/".join(tipos_list) if tipos_list else ""
    except Exception:
        tipos = ""

    try:
        descripcion = driver.find_element(
            By.CSS_SELECTOR, ".version-descriptions.active p.version-x"
        ).get_attribute("innerText").strip()
    except NoSuchElementException:
        descripcion = "(sin descripción versión X)"

    try:
        imagen = driver.find_element(
            By.CSS_SELECTOR, "div.pokedex-pokemon-profile img"
        ).get_attribute("src")
    except Exception:
        imagen = None

    return {
        "No. Pokedex": numero,
        "Nombre": nombre,
        "Descripción": descripcion,
        "Tipo": tipos,
        "URL": imagen
    }
