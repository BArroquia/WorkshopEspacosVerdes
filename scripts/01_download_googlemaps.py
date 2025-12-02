from playwright.sync_api import sync_playwright
import pandas as pd
import time
import random

def scrape_google(url):
    with sync_playwright() as p:
        # 1. Lanzamos el navegador en modo 'headless=False' para ver qué pasa
        # Esto también ayuda a evitar ser detectado como bot inmediatamente
        reviews_data = []
        browser = p.firefox.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        # Simulamos una ventana de tamaño normal
        page.set_viewport_size({"width": 1280, "height": 720})

        print(f"Navegando a: {url}")
        page.goto(url, timeout=60000)
        time.sleep(random.uniform(0.5, 1))
        time.sleep(1005)

        # browser.close()
        return reviews_data


def scrape_google_cookies(url):
    with sync_playwright() as p:
        # 1. Lanzamos el navegador
        browser = p.firefox.launch(headless=False, slow_mo=500)
        context = browser.new_context(locale="pt-PT")
        page = context.new_page()
        reviews_data = []
        
        page.set_viewport_size({"width": 1280, "height": 720})

        print(f"Navegando a: {url}")
        page.goto(url, timeout=60000)
        time.sleep(10)
        # --- BLOQUE NUEVO: GESTIÓN DE COOKIES ---
        try:
            print("Buscando botón 'Rejeitar tudo'...")
            
            # Usamos get_by_role para buscar un botón que contenga ese texto.
            # Esto es "case-insensitive" (no importa mayúsculas/minúsculas) por defecto a veces, 
            # pero mejor ser exacto con el texto que ves.
            boton_rechazar = page.get_by_role("button", name="Rejeitar tudo")
            
            # Verificamos si existe y es visible
            if boton_rechazar.is_visible():
                boton_rechazar.click()
                print("Botón clickeado. Esperando navegación...")
                
                # Esperamos a que la página termine de cargar tras el click
                # 'networkidle' significa que espera hasta que no haya conexiones de red activas (la web cargó)
                page.wait_for_load_state("networkidle")
            else:
                print("El botón no apareció (quizás ya no hay cookies o el texto es distinto).")
                
        except Exception as e:
            print(f"Error gestionando cookies: {e}")

        # --- FIN BLOQUE NUEVO ---

        # Pequeña pausa humana antes de extraer datos
        # time.sleep(random.uniform(3, 10))
        time.sleep(1000)
        
        # AQUI IRÍA TU LÓGICA DE EXTRACCIÓN (Scraping)
        # Por ejemplo: verificar si estamos en la página correcta imprimiendo el título
        print(f"Título de la página actual: {page.title()}")

        browser.close()
        return reviews_data
    

def scrape_google_pesquisa(url, search_word):
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
        # --- BLOQUE DE BÚSQUEDA ---
        print("Introduciendo término de búsqueda...")
        
        # 1. Localizar la barra por su ID y escribir el texto
        # .fill() borra lo que haya y escribe el nuevo texto
        page.locator("#searchboxinput").fill(search_word)
        # Pequeña pausa para simular comportamiento humano (opcional pero recomendada)
        time.sleep(random.uniform(1, 3))

        # 2. Hacer clic en el botón de búsqueda
        # En Google Maps, el botón de la lupa suele tener el id "searchbox-searchbutton"
        # Si prefieres buscarlo por el tooltip "Pesquisar", usaríamos get_by_role
        
        # Opción A (Más robusta por ID):
        page.locator("#searchbox-searchbutton").click()
        
        # Opción B (Si prefieres simular la tecla Enter, que a veces falla menos):
        # page.keyboard.press("Enter")

        print("Búsqueda realizada. Esperando resultados...")
        
        # Esperamos a que cargue la lista de resultados (buscamos un elemento que solo sale tras buscar)
        # El panel de resultados suele tener role="feed" o contener la clase 'm6QErb'
        page.wait_for_selector("div[role='feed']", timeout=10000)
        
        # --- FIN BLOQUE DE BÚSQUEDA ---
        time.sleep(1000)
        
        # AQUI IRÍA TU LÓGICA DE EXTRACCIÓN (Scraping)
        # Por ejemplo: verificar si estamos en la página correcta imprimiendo el título
        print(f"Título de la página actual: {page.title()}")

        browser.close()
        return reviews_data

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
        
        # 1. Localizar la barra por su ID y escribir el texto
        # .fill() borra lo que haya y escribe el nuevo texto
        page.locator("#searchboxinput").fill(search_word)
        # Pequeña pausa para simular comportamiento humano (opcional pero recomendada)
        time.sleep(random.uniform(1, 3))
        # page.keyboard.press("Enter")

        print("Búsqueda realizada. Esperando resultados...")
        
        # Esperamos a que cargue la lista de resultados (buscamos un elemento que solo sale tras buscar)
        # El panel de resultados suele tener role="feed" o contener la clase 'm6QErb'
        # page.wait_for_selector("div[role='feed']", timeout=10000)
        page.keyboard.press('ArrowDown')
        time.sleep(random.uniform(1, 2))
        page.keyboard.press("Enter")
        time.sleep(random.uniform(1, 4))
    except:
        print("ERROR seaching: ", search_word)
    
    return page
    
  

def scrape_google_select(url, search_word, max_reviews=50):
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
        # 2. Search terms
        page = search_term(page, search_word)
 
        # 3. Select and get new url
        try:
            page.wait_for_selector("div[role='feed']", timeout=10000)
            page.locator("a.hfpxzc").first.click()
            print("Clic realizado. Esperando actualización de URL...")
            # --- LA CLAVE ESTÁ AQUÍ ---
            # Le decimos: "Espera hasta que la URL contenga la palabra '/place/'"
            # Los asteriscos ** son comodines (significa cualquier texto antes o después)
            page.wait_for_url("**/place/**", timeout=15000)
            
            # Ahora sí es seguro capturar la URL
            nueva_url = page.url
            print("-" * 30)
            print(f"URL FINAL: {nueva_url}")
            print("-" * 30)

            # Opcional: Esperar a que cargue el título para confirmar visualmente
            page.wait_for_selector("h1", timeout=5000)
            time.sleep(random.uniform(1, 4))
        except Exception as e:
            print(f"Error obteniendo la URL: {e}")

# 5. Entrar en la pestaña "Críticas" (Reviews)
        # Buscamos el botón tab que contenga la palabra "Críticas" o "Comentários"
        try:
            # El selector busca cualquier pestaña que tenga ese texto (insensible a mayúsculas)
            tab_reviews = page.locator("button[role='tab']", has_text="Críticas").or_(
                          page.locator("button[role='tab']", has_text="Comentários"))
            
            # Esperamos a que sea visible y clicamos
            tab_reviews.first.wait_for(state="visible", timeout=5000)
            tab_reviews.first.click()
            print("Pestaña de Críticas abierta.")
            time.sleep(2) # Pausa vital para que cargue el panel de reseñas
        except Exception as e:
            print(f"No se encontró la pestaña 'Críticas': {e}")
            browser.close()
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
                    "Estrellas": estrellas,
                    "Fecha": fecha,
                    "Comentario": texto.replace("\n", " ") # Quitamos saltos de línea para el CSV
                })
            except Exception as e:
                print(f"Error en reseña {i}: {e}")

        browser.close()
        return data



def scrape_google_get_comments(url, search_word, max_reviews=50):
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
        # 2. Search terms
        page = search_term(page, search_word)
 
        # 3. Select and get new url
        try:
            page.wait_for_selector("div[role='feed']", timeout=10000)
            page.locator("a.hfpxzc").first.click()
            print("Clic realizado. Esperando actualización de URL...")
            # --- LA CLAVE ESTÁ AQUÍ ---
            # Le decimos: "Espera hasta que la URL contenga la palabra '/place/'"
            # Los asteriscos ** son comodines (significa cualquier texto antes o después)
            page.wait_for_url("**/place/**", timeout=15000)
            
            # Ahora sí es seguro capturar la URL
            nueva_url = page.url
            print("-" * 30)
            print(f"URL FINAL: {nueva_url}")
            print("-" * 30)

            # Opcional: Esperar a que cargue el título para confirmar visualmente
            page.wait_for_selector("h1", timeout=5000)
            time.sleep(random.uniform(1, 4))
        except Exception as e:
            print(f"Error obteniendo la URL: {e}")

# 5. Entrar en la pestaña "Críticas" (Reviews)
        # Buscamos el botón tab que contenga la palabra "Críticas" o "Comentários"
        try:
            # El selector busca cualquier pestaña que tenga ese texto (insensible a mayúsculas)
            tab_reviews = page.locator("button[role='tab']", has_text="Críticas").or_(
                          page.locator("button[role='tab']", has_text="Comentários"))
            
            # Esperamos a que sea visible y clicamos
            tab_reviews.first.wait_for(state="visible", timeout=5000)
            tab_reviews.first.click()
            print("Pestaña de Críticas abierta.")
            time.sleep(2) # Pausa vital para que cargue el panel de reseñas
        except Exception as e:
            print(f"No se encontró la pestaña 'Críticas': {e}")
            browser.close()
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
                    "Estrellas": estrellas,
                    "Fecha": fecha,
                    "Comentario": texto.replace("\n", " ") # Quitamos saltos de línea para el CSV
                })
            except Exception as e:
                print(f"Error en reseña {i}: {e}")

        browser.close()
        return data


# --- EJECUCIÓN ---
if __name__ == "__main__":
    # URL de ejemplo (Un hotel en Madrid, cambia esto por tu URL objetivo)
    target_url = "https://www.google.com/maps"
    NOMBRE_ARCHIVO = "criticas_parco_verde.csv"
    # 1 step: go to google
    # datos = scrape_google(target_url)
    # 2 step: acept cookies
    # datos = scrape_google_cookies(target_url)
    # 3 step: search
    # datos = scrape_google_pesquisa(url=target_url, search_word='parco verde')
    
    # 4 step: select and get data
    resultados = scrape_google_select(url=target_url, search_word='parco verde coimbra', max_reviews=10)

    if resultados:
        # Guardar a CSV usando Pandas
        df = pd.DataFrame(resultados)
        df.to_csv(NOMBRE_ARCHIVO, index=False, encoding="utf-8-sig") # utf-8-sig es clave para abrir en Excel con acentos
        print(f"¡Éxito! Archivo guardado: {NOMBRE_ARCHIVO}")
        print(df.head())
    else:
        print("No se obtuvieron datos.")