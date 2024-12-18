import subprocess
import os

# Codici ANSI per il colore del testo
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RESET = "\033[0m"

def check_host_reachable(file_path):
    try:
        # Verifico che il file esista
        if not os.path.isfile(file_path):
            print(f"{RED}Errore: il file '{file_path}' non esiste.{RESET}\n")
            return
        
        # Apro il file e lo leggo riga per riga
        with open(file_path, "r") as file:
            urls = file.readlines()

        i = 0
        # Itero sugli URL
        for url in urls:
            url = url.strip()  # Rimuovo spazi vuoti e newline
            if not url:
                continue  # Salto le righe vuote

            print(f"{CYAN}Controllo l'host: '{url}' ...{RESET}")

            # Costruisco il comando di ping
            command = ['ping', '-c', '1', url]

            try:
                # Eseguo il comando
                result = subprocess.run(command, capture_output=True, text=True)
                
                # Verifico il return code
                if result.returncode == 0:
                    with open("alive.txt", "w") as alive:  # Uso append per non sovrascrivere
                        i += 1
                        alive.write(f"[{i}]\t""http://""{url}\n")
                    print(f"{GREEN}[+] L'host '{url}' è UP.{RESET}")
                else:
                    continue
            
            except Exception as e:
                print(f"{RED}[!] Errore nell'eseguire il ping su {url}: {e}{RESET}")
    
    except Exception as e:
        print(f"{RED}Errore: {e}{RESET}")

def find_subfinder(URL):
    # Verifico che l'URL sia UP
    command = ['ping', '-c', '1', URL]

    try:
        result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if result.returncode == 0:
            print(f"{GREEN}[+] L'host '{URL}' è UP.{RESET}")
        else:
            print(f"{YELLOW}[-] L'host '{URL}' sembra essere DOWN.{RESET}\n")
            exit(-1)

        # Host è UP, eseguo subfinder
        command = ['subfinder', '-d', URL, '-all']
        try:
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                with open("subdomains.txt", "w") as file:
                    file.write(result.stdout)
                print(f"{GREEN}[+] Sottodomini salvati in 'subdomains.txt'.{RESET}\n")
            else:
                print(f"{RED}[!] Errore nell'eseguire subfinder. Return code: {result.returncode}{RESET}")
        except Exception as e:
            print(f"{RED}[!] Errore nell'eseguire subfinder su {URL}: {e}{RESET}")

    except Exception as e:
        print(f"{RED}[!] Errore nell'eseguire il ping su {URL}: {e}{RESET}")

if __name__ == "__main__":

    # Se utente sceglie 1 allora deve inserire già il file contenente i subdomain
    # Se sceglie 2 allora richiedo solamente un URL
    scelta = int(input(f"{CYAN}Inserisci 1 per vedere se i subdomains sono UP o DOWN, Inserisci 2 per trovare anche i subdomains: {RESET}"))

    if scelta == 1:
        file_path = input(f"{CYAN}Inserisci il path del file.txt contenente gli URL: {RESET}").strip()
        check_host_reachable(file_path)
    elif scelta == 2:
        URL = input(f"{CYAN}Inserisci l'URL del quale trovare i sottodomini: {RESET}").strip()
        find_subfinder(URL)
        check_host_reachable("subdomains.txt")
