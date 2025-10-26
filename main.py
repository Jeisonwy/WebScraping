import json
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from scraper.google_sheets import upload_to_sheet
from config import START_URL, OUTPUT_FILE, MAX_ITERATIONS, WAIT_SECONDS
from scraper.driver import create_driver
from scraper.extractor import extract_pokemon_data
import os
from config import SHEET_ID
from config import MAX_ITERATIONS as DEFAULT_MAX_ITERATIONS

sys.stderr = open(os.devnull, "w")

def main():
    driver = create_driver()
    wait = WebDriverWait(driver, WAIT_SECONDS)
    collected = []
    iteration = 0


    if len(sys.argv) > 1:
        try:
            MAX_ITERATIONS = int(sys.argv[1])
        except ValueError:
            MAX_ITERATIONS = DEFAULT_MAX_ITERATIONS
    else:
        MAX_ITERATIONS = DEFAULT_MAX_ITERATIONS
    try:
        driver.get(START_URL)

        while iteration < MAX_ITERATIONS:
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".pokemon-number")))
            except TimeoutException:
                print("Timeout esperando que cargue la ficha del Pokémon.")

            data = extract_pokemon_data(driver)
            if data and (data.get("Nombre") or data.get("numero")):
                iteration += 1
                collected.append(data)
                print(f"[{iteration}/{MAX_ITERATIONS}] {data.get('Nombre') or data.get('numero')}")
                with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                    json.dump(collected, f, ensure_ascii=False, indent=2)
            else:
                print("No se obtuvo información del Pokémon actual.")

            if iteration >= MAX_ITERATIONS:
                break

            try:
                next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.next")))
                driver.execute_script("arguments[0].click();", next_btn)
            except (TimeoutException, NoSuchElementException):
                print("Botón 'siguiente' no encontrado: fin de la secuencia.")
                break

            

    except Exception as e:
        print("Error general:", e, file=sys.stderr)
    finally:

        print(f" Terminado. Pokémon extraídos: {len(collected)}")
        print(" Archivo guardado en:", OUTPUT_FILE)
        if collected:
            upload_to_sheet(SHEET_ID, collected)


if __name__ == "__main__":
    main()
