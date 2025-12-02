import pandas as pd
import geopandas as gpd
from playwright.sync_api import sync_playwright
import time
import random
import sqlite3


def acept_cookies(page):
# --- BLOQUE NUEVO: GESTIÓN DE COOKIES ---
    try:
        print("Buscando botón 'Rejeitar tudo'...")
        boton_rechazar = page.get_by_role("button", name="Rejeitar tudo")
        if boton_rechazar.is_visible():
            boton_rechazar.click()
            print("Botón clickeado. Esperando navegación...")
            page.wait_for_load_state("networkidle")
        else:
            print("El botón no apareció (quizás ya no hay cookies o el texto es distinto).")
            
    except Exception as e:
        print(f"Error gestionando cookies: {e}")
    # Pequeña pausa humana antes de extraer datos
    time.sleep(random.uniform(3, 10))
    return page

def search_term(page, search_word):
    try:
        # --- BLOQUE DE BÚSQUEDA ---
        print("Introduciendo término de búsqueda...")
        page.locator("#searchboxinput").fill(search_word)
        # Pequeña pausa para simular comportamiento humano (opcional pero recomendada)
        time.sleep(random.uniform(1, 3))

        print("Búsqueda realizada. Esperando resultados...")
        page.keyboard.press('ArrowDown')
        time.sleep(random.uniform(1, 2))
        page.keyboard.press("Enter")
        time.sleep(random.uniform(1, 4))
    except:
        print("ERROR seaching: ", search_word)
    
    return page

def get_comments(page, max_reviews, search_word):
    try:
        page.wait_for_selector("div[role='feed']", timeout=10000)
        page.locator("a.hfpxzc").first.click()
        print("Clic realizado. Esperando actualización de URL...")
        # Opcional: Esperar a que cargue el título para confirmar visualmente
        page.wait_for_selector("h1", timeout=5000)
        time.sleep(random.uniform(1, 4))
    except Exception as e:
        print(f"Error obteniendo la URL: {e}")

    try:
        # El selector busca cualquier pestaña que tenga ese texto (insensible a mayúsculas)
        tab_reviews = page.locator("button[role='tab']", has_text="Críticas").or_(
                        page.locator("button[role='tab']", has_text="Comentários"))
        
        # Esperamos a que sea visible y clicamos
        tab_reviews.first.wait_for(state="visible", timeout=5000)
        tab_reviews.first.click()
        print("Pestaña de Críticas abierta.")
        page.wait_for_url("**/place/**", timeout=15000)
        
        # Ahora sí es seguro capturar la URL
        nueva_url = page.url
        print("-" * 30)
        print(f"URL FINAL: {nueva_url}")
        print("-" * 30)
        time.sleep(2) # Pausa vital para que cargue el panel de reseñas
    except Exception as e:
        print(f"No se encontró la pestaña 'Críticas': {e}")
        return []
    
    # 6. Scroll para cargar reseñas
    # El contenedor de reseñas suele ser el segundo div con role='main' o similar.
    # Estrategia: Buscar las tarjetas de reseñas (class 'jftiEf') y hacer scroll al último
    print(f"--- Iniciando descarga de {max_reviews} reseñas ---")
    
    reviews_locator = page.locator("div.jftiEf")
    container_scroll = page.locator('.m6QErb.DxyBCb.kA9KIf.dS8AEf').nth(1) # Contenedor habitual

    last_count = 0
    while True:
        count = reviews_locator.count()
        print(f"Cargadas: {count} / {max_reviews}")
        
        if count >= max_reviews:
            break
        
        if count == last_count and count > 0:
            # Si no ha cargado más, intentamos forzar scroll
            # Mover el ratón al centro para asegurar foco
            page.mouse.move(500, 500) 
            page.keyboard.press("PageDown")
            time.sleep(1)
            
            # Chequeo de seguridad por si llegamos al final real
            if reviews_locator.count() == last_count:
                print("Parece que no hay más reseñas.")
                break
        else:
            # Método estándar: ir al último elemento
            reviews_locator.last.scroll_into_view_if_needed()
            
        last_count = count
        time.sleep(1.5) # Espera técnica para dar tiempo a cargar

    # 7. Expandir textos largos ("Mais" / "Ver más")
    botones_mas = page.locator("button", has_text="Mais").or_(page.locator("button", has_text="Ver más"))
    for btn in botones_mas.all():
        if btn.is_visible():
            try: btn.click()
            except: pass

    # 8. Extraer Datos
    data = []
    reviews = reviews_locator.all()
    
    # Limitamos al máximo pedido para no procesar de más
    for i, review in enumerate(reviews[:max_reviews]):
        try:
            # Texto (A veces no hay texto, solo estrellas)
            text_el = review.locator(".wiI7pd")
            texto = text_el.inner_text() if text_el.count() > 0 else ""
            
            # Estrellas (Buscamos el aria-label)
            stars_el = review.locator("span[role='img']")
            stars_attr = stars_el.get_attribute("aria-label") if stars_el.count() > 0 else "0"
            # Limpiamos "5 estrelas" -> "5"
            estrellas = stars_attr.split(" ")[0].replace(",", ".") if stars_attr else "0"

            # Fecha (Ej: "hace 2 meses")
            fecha = review.locator(".rsqaWe").inner_text()
            
            data.append({
                "url": nueva_url,
                "search_word": search_word,
                "Estrellas": estrellas,
                "Fecha": fecha,
                "Comentario": texto.replace("\n", " ") # Quitamos saltos de línea para el CSV
            })
        except Exception as e:
            print(f"Error en reseña {i}: {e}")
    data = pd.DataFrame(data)
    return data


def scrape_google(url, ls_locations, path_db, max_reviews=50):
    ls_loc_saved = []
    with sync_playwright() as p:
        # 1. Lanzamos el navegador
        browser = p.firefox.launch(headless=False, slow_mo=500)
        context = browser.new_context(locale="pt-PT")
        page = context.new_page()
        reviews_data = []
        
        page.set_viewport_size({"width": 1280, "height": 720})

        print(f"Navegando a: {url}")
        page.goto(url, timeout=60000)
        time.sleep(random.uniform(1, 3))
        # 1. Cookies
        page = acept_cookies(page)
        for search_word in ls_locations:
            time.sleep(random.uniform(1, 3))
            try:
                print("Search in google: ", search_word)
                # 2. Search terms
                page = search_term(page, search_word)
                # 3. Select and get new url
                data = get_comments(page, max_reviews, search_word)
                print(data)
                with sqlite3.connect(path_db) as connection:
                    if isinstance(data, pd.DataFrame):
                        data.to_sql("googleplaces", connection, if_exists="append")
                        ls_loc_saved.append(search_word)

            except Exception as e:
                print("ERROR saving data: ", e)  
        browser.close()
        return ls_loc_saved


# --- EJECUCIÓN ---
if __name__ == "__main__":
    # URL de ejemplo (Un hotel en Madrid, cambia esto por tu URL objetivo)
    target_url = "https://www.google.com/maps"
    NOME_DB = "data/raw/scrapcomments.db"
    file_name = "data/raw/espacios_verdes_coimbra.geojson"
    gdf_parques = gpd.read_file(file_name)
    gdf = gdf_parques.loc[gdf_parques['name'].notna(), :].copy()
    gdf['name'] = gdf['name'] + ' coimbra'
    ls_locations = gdf['name'].str.lower().to_list()
    
    locations_saved = scrape_google(url=target_url, 
                               ls_locations=ls_locations, 
                               path_db=NOME_DB,
                               max_reviews=100)
    print(locations_saved)
    print("END SCRAPING")