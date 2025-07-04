## Descrizione
`geometria_base` è un programma C++  per il calcolo di perimetro, area, diagonali e altezze di diverse figure. Supporta l'input da **tastiera** per una singola figura o da **file di testo** per elaborazioni multiple. I risultati vengono visualizzati a schermo e salvati in un file di output.

**Figure supportate:**

* **Quadrato**
* **Rettangolo**
* **Rombo**
* **Triangolo Isoscele**
* **Triangolo Rettangolo**
* **Triangolo Equilatero**
* **Triangolo Scaleno**

Il programma gestisce automaticamente i valori sconosciuti (`?`), tentando di calcolare le proprietà mancanti in base ai dati disponibili.

---

## Uso del File di Input

Il file di input è un file di testo in cui ogni record, separato da un punto e virgola (`;`), rappresenta una figura geometrica. I parametri della figura sono separati da virgole (`,`). I nomi delle figure e dei parametri **non sono case-sensitive**.

**Struttura del record:**
```
TipoFigura, (Azioni), Parametro1, Valore1, Parametro2, Valore2;
```


**Esempio di `dati.txt`:**
```
Rettangolo, perimetro, base, 7, altezza, 12;
Quadrato, area, lato, 5;
Triangolo Scaleno, Calcola tutto, LatoA, 3, LatoB, 4, LatoC, 5;
```

---

## Compilazione

Per compilare il programma, è necessario un **compilatore C++** (come `g++`). Per lo sviluppo e le modifiche al codice, è consigliato l'uso di un **IDE** come Visual Studio Code, Emacs, Eclipse o Notepad++.

Se usi un IDE, la compilazione e l'esecuzione sono solitamente gestite automaticamente tramite i controlli integrati dell'IDE (es. un pulsante "Run", "Build and Run" o un'opzione di menu). Consulta la documentazione specifica del tuo IDE per i dettagli su come compilare ed eseguire progetti C++.

Per compilare dal terminale, naviga nella directory del progetto ed esegui:

```bash
g++ geometria_base.cpp -o geometria_base
```
Puoi poi eseguire facendo:
```
./geometria_base
```
**Nota**: Dopo ogni modifica al codice sorgente C++, devi ricompilare il file prima di eseguire il programma per vedere le modifiche.

---

## EXIT STATUS
0: Il programma è terminato con successo.

1: Si è verificato un errore (es., input non valido, file non trovato).
