
### Descrizione
geometria_base è un programma c++ che calcola perimetro, area, diagonali e altezze di diverse figure geometriche. Supporta input da tastiera per una singola figura o da file per elaborazioni multiple. I risultati vengono visualizzati a schermo e salvati in un file di output.
Figure supportate: Quadrato, Rettangolo, Rombo, Triangolo Isoscele, Triangolo Rettangolo, Triangolo Equilatero, Triangolo Scaleno.
Il programma gestisce automaticamente valori sconosciuti (?) tentando di calcolare le proprietà mancanti.

### Uso file di testo come input
Il file di input è un testo con record separati da punto e virgola (;). Ogni record rappresenta una figura e i suoi parametri, separati da virgole (,). I nomi delle figure e dei parametri non sono case-sensitive.
Strutturato così:

TipoFigura, (Azioni), Parametro1, Valore1, Parametro2, Valore2;

### Compilatori
Per compilare, assicurati di avere un compilatore C++ come Visual Studio Code(Windows/Mac), g++(Linux), Emacs(Mac), Eclipse(Windows, Linux, Mac), Notepad++(Windows) ecc...

### EXIT STATUS
0 se il programma termina con successo, 1 in caso di errori (es. input non valido, file non trovato).
