import csv # Modulo per leggere e scrivere file CSV
import time # Modulo per introdurre pause nel codice (utili nello scraping web)
from datetime import datetime # Modulo per lavorare con date e orari
from selenium import webdriver # Il modulo principale di Selenium per interagire con i browser
from selenium.webdriver.common.by import By # Usato per specificare come trovare gli elementi (es. per ID, per classe, per XPath)
from selenium.webdriver.common.keys import Keys # Usato per inviare tasti speciali (es. INVIO) a un elemento
from selenium.webdriver.firefox.service import Service as FirefoxService # Necessario per configurare il servizio di Firefox (geckodriver)
from selenium.webdriver.firefox.options import Options as FirefoxOptions # Permette di configurare opzioni specifiche per Firefox (es. modalità headless)
from selenium.webdriver.support.ui import WebDriverWait # Usato per implementare attese esplicite (aspettare che una condizione sia vera)
from selenium.webdriver.support import expected_conditions as EC # Contiene una serie di condizioni predefinite per WebDriverWait (es. elemento visibile, cliccabile)
from selenium.common.exceptions import TimeoutException, NoSuchElementException # Eccezioni comuni di Selenium che è utile gestire

# Importa WebDriverManager per Firefox (gestisce automaticamente geckodriver)
# Questo modulo semplifica la configurazione di Selenium, scaricando automaticamente il driver del browser corretto
from webdriver_manager.firefox import GeckoDriverManager

# Lista delle città e dei paesi da cui estrarre i dati
# Queste saranno le località per cui lo script cercherà le informazioni meteo
CITIES = [
    "Roma, Italia", "Milano, Italia", "Torino, Italia", "Venezia, Italia",
    "Firenze, Italia", "Napoli, Italia", "Palermo, Italia", "Tokyo, Giappone",
    "New York, Stati Uniti", "Los Angeles, Stati Uniti", "Parigi, Francia",
    "Londra, Regno Unito", "Seul, Corea del Sud"
]

def setup_driver():
    """
    Configura e restituisce un'istanza del WebDriver di Firefox.
    Utilizza GeckoDriverManager per gestire automaticamente il geckodriver,
    il che significa che non devi scaricarlo o specificare il suo percorso manualmente.
    """
    firefox_options = FirefoxOptions() # Crea un oggetto per configurare le opzioni di Firefox
    # Puoi scommentare la riga seguente per eseguire Firefox in modalità headless (senza interfaccia grafica)
    # Questa modalità è utile per l'esecuzione su server o per rendere lo scraping più veloce
    # firefox_options.add_argument("--headless")
    # Aggiungi argomenti comuni per la modalità headless su sistemi Linux, spesso necessari per prevenire errori
    # firefox_options.add_argument("--no-sandbox")
    # firefox_options.add_argument("--disable-dev-shm-usage")

    # Inizializza il servizio di Firefox usando GeckoDriverManager
    # Questo metodo scarica e configura il geckodriver (il bridge tra Selenium e Firefox)
    service = FirefoxService(GeckoDriverManager().install())

    print("Avvio del browser Firefox...")
    # Inizializza il WebDriver di Firefox con il servizio e le opzioni definite
    driver = webdriver.Firefox(service=service, options=firefox_options)
    # Imposta un'attesa implicita globale: il driver aspetterà fino a 10 secondi per trovare un elemento prima di sollevare un'eccezione
    driver.implicitly_wait(10)
    return driver

def handle_cookie_consent(driver: webdriver.Firefox):
    """
    Tenta di gestire il consenso ai cookie su MSN Meteo.
    Questa parte è molto sensibile ai cambiamenti del sito web,
    poiché i selettori degli elementi (ID, classi) possono cambiare frequentemente.
    """
    try:
        print("Tentativo di gestione del consenso ai cookie...")
        # Attende esplicitamente che il bottone di accettazione dei cookie sia presente nel DOM (Document Object Model)
        # Questo è più robusto di un semplice time.sleep() perché aspetta una condizione specifica
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "onetrust-accept-btn-handler"))
        )
        # Tenta di trovare il bottone "Rifiuta tutto". Se esiste e è visibile, lo clicca.
        reject_button = driver.find_element(By.ID, "onetrust-reject-all-handler")
        if reject_button.is_displayed(): # Verifica se il bottone è visibile all'utente
            reject_button.click() # Clicca sul bottone
            print("Cookie rifiutati.")
        else:
            # Se il bottone "Rifiuta tutto" non è visibile, prova a cliccare quello di accettazione
            accept_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
            accept_button.click()
            print("Cookie accettati (Rifiuta tutto non trovato).")

    except TimeoutException:
        # Questa eccezione viene sollevata se WebDriverWait non trova l'elemento entro il tempo limite
        print("Timeout: Nessun pop-up/barra per i cookie trovato o caricamento lento.")
    except NoSuchElementException:
        # Questa eccezione viene sollevata se find_element non trova l'elemento con l'ID specificato
        print("Nessun bottone per i cookie con ID noto trovato. Proseguo.")
    except Exception as e:
        # Cattura qualsiasi altro errore inaspettato
        print(f"Errore generico durante la gestione dei cookie: {e}")
    time.sleep(2) # Piccola pausa per lasciare che l'interfaccia utente si assesti dopo l'interazione con i cookie

def get_weather_data(driver: webdriver.Firefox, city: str) -> dict | None:
    """
    Naviga su MSN Meteo, cerca la città e tenta di estrarre i dati meteo desiderati.
    Restituisce un dizionario con i dati o None in caso di errore.
    """
    print(f"  Ricerca dati meteo per: {city}")
    try:
        # Apre la pagina di MSN Meteo
        driver.get("https://www.msn.com/it-it/meteo")
        
        # Gestione dei cookie subito dopo il caricamento della pagina per ogni città.
        # È importante gestirli qui perché potrebbero riapparire o essere specifici per sessione/pagina.
        handle_cookie_consent(driver) 

        # Attendi che la casella di ricerca sia cliccabile.
        # Usiamo un selettore CSS che è più robusto, cercando sia per classe che per placeholder testuale.
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input.querybox-searchBox, input[placeholder*='Cerca località']"))
        )
        search_box.clear() # Pulisce qualsiasi testo preesistente nella casella di ricerca
        search_box.send_keys(city) # Digita il nome della città nella casella di ricerca
        
        # *** INIZIO MODIFICHE PER SELEZIONE SUGGERIMENTO PIÙ ROBUSTA ***
        # Estrai solo il nome della città (es. "Roma" da "Roma, Italia")
        city_name_only = city.split(',')[0].strip() 
        
        try:
            # Attendi che il contenitore dei suggerimenti appaia dopo aver digitato la città
            WebDriverWait(driver, 5).until( # Breve attesa per la comparsa del box suggerimenti
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul[role='listbox']"))
            )
            # Attendi che il primo suggerimento all'interno del listbox sia cliccabile.
            # Usiamo un XPath per trovare un bottone all'interno della lista che contenga il nome della città.
            first_suggestion = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, f"//ul[@role='listbox']//button[contains(., '{city_name_only}')]"))  
            )
            first_suggestion.click() # Clicca sul suggerimento
            print(f"    Selezionato il suggerimento per {city}.")
            time.sleep(3) # Pausa più lunga dopo il click sul suggerimento per dare tempo alla pagina di caricarsi
        except TimeoutException:
            # Se nessun suggerimento specifico viene trovato, prova a premere INVIO come fallback
            print(f"    Nessun suggerimento specifico trovato o cliccabile per {city_name_only} dopo aver digitato. Tentativo con ENTER.")
            search_box.send_keys(Keys.ENTER) # Simula la pressione del tasto INVIO
            time.sleep(5) # Pausa più lunga dopo INVIO, poiché potrebbe portare a una pagina di ricerca generica o a un caricamento più lungo
        # *** FINE MODIFICHE PER SELEZIONE SUGGERIMENTO ***


        # *** AGGIORNATO: Attendi che l'elemento della temperatura attuale sia VISIBILE ***
        # Questo è l'indicatore più affidabile che la pagina specifica della città è caricata con i dati.
        print(f"    Attesa del caricamento dei dati meteo per {city}...")
        WebDriverWait(driver, 25).until( # Aumentato il timeout per il caricamento dei dati, specialmente su connessioni lente
            EC.visibility_of_element_located((By.CLASS_NAME, "u1SummaryTemperatureCompact-DS-EntryPoint1-1"))
        )
        print(f"    Dati meteo per {city} caricati correttamente.")
        time.sleep(3) # Pausa aggiuntiva per garantire il caricamento completo di tutto il contenuto dinamico della pagina

        # Inizializza un dizionario per i dati meteo della città corrente
        data = {"Citta": city, "Data_Estrazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        # --- Estrazione Dati Attuali ---
        try:
            # Trova l'elemento della temperatura attuale tramite la sua classe CSS e estrae il testo
            current_temp = driver.find_element(By.CLASS_NAME, "u1SummaryTemperatureCompact-DS-EntryPoint1-1").text.strip()
            data["Temperatura_Attuale"] = current_temp
            print(f"    Temperatura attuale trovata: {current_temp}")
        except NoSuchElementException:
            # Se l'elemento non viene trovato, imposta il valore su "N/A"
            data["Temperatura_Attuale"] = "N/A"
            print(f"    Temperatura attuale non trovata per {city}.")

        try:
            # Trova l'elemento della condizione attuale (es. "Soleggiato", "Parzialmente nuvoloso")
            current_condition = driver.find_element(By.CLASS_NAME, "u1SummaryCaptionCompact-DS-EntryPoint1-1").text.strip()
            data["Condizione_Attuale"] = current_condition
            print(f"    Condizione attuale trovata: {current_condition}")
        except NoSuchElementException:
            data["Condizione_Attuale"] = "N/A"
            print(f"    Condizione attuale non trovata per {city}.")
        
        try:
            # Trova l'elemento dell'indice UV attuale tramite il suo ID
            uv_element = driver.find_element(By.ID, "CurrentDetailLineUVIndexValue")
            data["UV_Index_Attuale"] = uv_element.text.strip()
            print(f"    Indice UV attuale trovato: {data['UV_Index_Attuale']}")
        except NoSuchElementException:
            data["UV_Index_Attuale"] = "N/A"
            print(f"    Indice UV attuale non trovato o non nel formato atteso per {city}.")

        print(f"  Dati estratti per {city}.")
        return data

    except TimeoutException:
        # Se si verifica un timeout durante il caricamento della pagina o la ricerca di elementi cruciali
        print(f"  Timeout durante il caricamento della pagina meteo per {city}. La pagina non si è stabilizzata entro il tempo previsto.")
        return None
    except NoSuchElementException as e:
        # Se un elemento cruciale non viene trovato
        print(f"  Elemento cruciale non trovato per {city}: {e}. La pagina potrebbe non essere stata caricata correttamente o il selettore è errato.")
        return None
    except Exception as e:
        # Cattura qualsiasi altro errore inaspettato durante il processo di estrazione
        print(f"  Errore generico durante l'estrazione per {city}: {e}")
        return None

def main():
    """
    Funzione principale per eseguire lo scraping e salvare i dati in un file CSV.
    Orchestra le chiamate alle altre funzioni.
    """
    driver = None # Inizializza il driver a None, per gestirlo nella clausola finally
    all_weather_data = [] # Lista per contenere tutti i dati meteo estratti
    output_filename = "msn_meteo_dati_semplificati.csv" # Nome del file CSV di output

    try:
        driver = setup_driver() # Inizializza il browser

        # Prepara l'intestazione del CSV con solo i dati richiesti
        header = ["Citta", "Data_Estrazione", "Temperatura_Attuale", "Condizione_Attuale", "UV_Index_Attuale"]
        all_weather_data.append(header) # Aggiunge l'intestazione come prima riga della lista dei dati

        for city in CITIES: # Itera su ogni città definita nella lista CITIES
            data = get_weather_data(driver, city) # Ottiene i dati meteo per la città corrente
            if data:
                # Se i dati sono stati recuperati con successo, crea una riga CSV.
                # Si usa data.get(col, "N/A") per assicurarsi che ogni colonna dell'header abbia un valore,
                # anche se un dato specifico non è stato trovato per quella città.
                row = [data.get(col, "N/A") for col in header]
                all_weather_data.append(row)
            else:
                # Se i dati per una città non sono stati recuperati (es. a causa di un errore),
                # aggiungi una riga con "Errore" per indicare il problema.
                error_row = [city, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Errore", "Errore", "Errore"]
                all_weather_data.append(error_row)

    except Exception as e:
        # Cattura qualsiasi errore critico che si verifica nella funzione principale
        print(f"Errore critico nello script principale: {e}")
    finally:
        # Questa blocco viene eseguito sempre, sia che ci siano errori o meno.
        # Assicura che il browser venga chiuso correttamente.
        if driver: # Controlla se il driver è stato inizializzato
            print("Chiusura del browser...")
            driver.quit() # Chiude il browser e termina la sessione del WebDriver
            print("Browser chiuso.")

    # Scrivi i dati raccolti nel file CSV
    print(f"\nSalvataggio dei dati nel file: {output_filename}...")
    try:
        # Apre il file in modalità scrittura ('w'), senza aggiungere righe vuote (newline='') e con codifica UTF-8
        with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile) # Crea un oggetto writer CSV
            csv_writer.writerows(all_weather_data) # Scrive tutte le righe (header + dati) nel file
        print(f"Dati meteo salvati con successo in {output_filename}!")
    except IOError as e:
        # Gestisce errori durante la scrittura del file
        print(f"Errore durante la scrittura del file CSV: {e}")

if __name__ == "__main__":
    # Questo blocco assicura che la funzione main() venga eseguita solo quando lo script viene eseguito direttamente,
    # e non quando viene importato come modulo in un altro script.
    main()
