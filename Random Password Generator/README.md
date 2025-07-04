## Descrizione
Questo progetto è un tool da riga di comando (CLI) scritto in Python.
Genera password basandosi su vari parametri forniti dall'utente. Il tool supporta la generazione di password completamente casuali o la creazione di "passphrase" più memorizzabili utilizzando parole, numeri e simboli.

---

### OPZIONI

* `-l LUNGHEZZA`, `--length LUNGHEZZA`
    * Specifica la lunghezza desiderata della password.
    * Il valore predefinito è `16`.

* `--no-lowercase`
    * Esclude le lettere minuscole (a-z) dalla password.
    * Nota: In modalità dizionario (`--dictionary`), le parole contengono lettere. Non è possibile escludere sia minuscole che maiuscole contemporaneamente in tale modalità.

* `--no-uppercase`
    * Esclude le lettere maiuscole (A-Z) dalla password.
    * Nota: Come per `--no-lowercase`, non è possibile escludere entrambe le forme letterali in modalità dizionario.

* `--no-digits`
    * Esclude i numeri (0-9) dalla password.

* `--no-symbols`
    * Esclude i simboli comuni (`!@#$%^&*()_+-=[]{}|;:,.<>_?`) dalla password.

* `--custom-symbols SIMBOLI`
    * Fornisce un set personalizzato di simboli da utilizzare invece di quelli predefiniti.
    * Esempio: `--custom-symbols "#@$-"` userà solo `#`, `@`, `$` e `-`.
    * Importante: Non può essere usato insieme a `--no-symbols`. Se tenti di usarli entrambi, il tool genererà un errore.

* `--include-spaces`
    * Include spazi (` `) nella password.
    * Disabilitato per impostazione predefinita per una migliore compatibilità.

* `--dictionary`
    * Attiva la modalità dizionario. Genera una password utilizzando parole reali, mescolate con numeri, simboli e caratteri casuali.
    * Le parole possono essere prese da liste interne (italiano/inglese) o da file esterni.
    * Il tool cercherà di randomizzare la capitalizzazione delle parole, a meno che non siano escluse esplicitamente minuscole o maiuscole.

* `--dictionary-files FILENAME`
    * Specifica il file contenente parole per la modalità dizionario, per semplicità mettilo nella stessa cartella dello script.
    * Le parole all'interno del file devono essere separate da virgole (es. `parola1,parola2,altraparola`).
    * Richiede l'uso dell'opzione `--dictionary`.
      
---

### ESEMPI D'USO

* python3 generate_password.py --dictionary -l 20 --no-digits
usando questo comando nella cartella dove si trova il file python si otterrà una password che rispetta le opzioni scelte --dictionary: userà parole di senso compiute(è raccomandato l'uso di --dictionary-files e di un file di testo ricco di parole per avere più varietà di password),  -l 20: Lunghezza password di 20, --no-digits: senza numeri
* python3 generate_password.py --length 10 --custom-symbols "*-$"
usando questo comando nella cartella dove si trova il file python si otterrà una password che rispetta le opzioni scelte --length 10: Lunghezza password di 10, --custom-symbols "*-$" la password può usare solo questo sottoinsieme di caratteri speciali

