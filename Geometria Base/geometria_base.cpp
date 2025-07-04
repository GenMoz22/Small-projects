#include <iostream>
#include <fstream>
#include <string>
#include <limits>    // Necessario per numeric_limits
#include <cmath>     // Necessario per sqrt
#include <cctype>    // Necessario per tolower
#include <sstream>   // Necessario per stringstream
#include <vector>    // Necessario per vector
#include <algorithm> // Necessario per std::transform
#include <iomanip>   // Necessario per std::fixed e std::setprecision
#include <memory>    // Necessario per std::unique_ptr e std::make_unique

using namespace std;

// Costanti per i tipi di input
const string INPUT_TASTIERA = "tastiera";
const string INPUT_FILE = "file";

// --- Funzioni di Utilità ---

// Funzione per ottenere un input double dall'utente in modo sicuro.
// Chiede all'utente con un messaggio e gestisce input non numerici o negativi.
double getDoubleInput(const string& prompt) {
    double value;
    string inputStr;
    while (true) {
        cout << prompt;
        cin >> inputStr;
        if (inputStr == "?") {
            return -1.0; // Valore sentinella per sconosciuto
        }
        try {
            value = stod(inputStr);
            if (value < 0) { // Non consentire valori negativi per dimensioni fisiche
                cerr << "Errore: I valori non possono essere negativi. Inserire un numero positivo o '?'.\n";
                cin.clear();
                cin.ignore(numeric_limits<streamsize>::max(), '\n');
                continue;
            }
            break;
        } catch (const invalid_argument& e) {
            cerr << "Errore: Input non valido. Inserire un numero o '?'.\n";
        } catch (const out_of_range& e) {
            cerr << "Errore: Numero troppo grande o troppo piccolo.\n";
        }
        cin.clear(); // Azzera lo stato di errore
        cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Scarta l'input rimanente nel buffer
    }
    return value;
}

// --- Classe Base per Figure Geometriche ---
// Questa classe astratta definisce l'interfaccia comune per tutte le figure geometriche.
class FiguraGeometrica {
public:
    string tipoFigura; // Nuovo membro per memorizzare il tipo di figura

    FiguraGeometrica(const string& tipo) : tipoFigura(tipo) {} // Costruttore
    virtual ~FiguraGeometrica() = default; // Distruttore virtuale per il polimorfismo
    virtual void calcola() = 0;           // Funzione virtuale pura per i calcoli
    virtual void stampaRisultato() const = 0; // Funzione virtuale pura per stampare i risultati
    // Nuovo metodo per impostare i parametri da un file, consente l'assegnazione dinamica delle proprietà.
    virtual void setParametro(const string& nomeParametro, double valore) = 0;
    // Funzione virtuale pura per ottenere i dati dall'input dell'utente.
    virtual void inserisciDati() = 0;

    // Nuovo metodo virtuale per ottenere una stringa formattata dei risultati
    virtual string getRisultatoFormattato() const = 0;
};

// --- Classi Derivate per Specifiche Figure Geometriche ---

// Classe per un Quadrato
class Quadrato : public FiguraGeometrica {
public:
    double lato;        // Lunghezza del lato
    double perimetro;   // Perimetro
    double area;        // Area
    double diagonale;   // Lunghezza della diagonale

    Quadrato() : FiguraGeometrica("Quadrato"), lato(0.0), perimetro(0.0), area(0.0), diagonale(0.0) {}

    void inserisciDati() override {
        cout << "Inserire la lunghezza del lato del quadrato (o '?' se sconosciuto): ";
        string input;
        cin >> input;
        if (input == "?") {
            lato = -1.0; // Valore sentinella per sconosciuto
        } else {
            try {
                lato = stod(input);
            } catch (const invalid_argument& e) {
                cerr << "Errore: Input non numerico per il lato." << endl;
                lato = 0.0; // Valore predefinito in caso di errore
            } catch (const out_of_range& e) {
                cerr << "Errore: Valore troppo grande o troppo piccolo per il lato." << endl;
                lato = 0.0;
            }
        }
    }

    void calcola() override {
        if (lato > 0) {
            perimetro = 4 * lato;
            area = lato * lato;
            diagonale = lato * sqrt(2);
        } else if (perimetro > 0) {
            lato = perimetro / 4;
            area = lato * lato;
            diagonale = lato * sqrt(2);
        } else if (area > 0) {
            lato = sqrt(area);
            perimetro = 4 * lato;
            diagonale = lato * sqrt(2);
        } else if (diagonale > 0) {
            lato = diagonale / sqrt(2);
            perimetro = 4 * lato;
            area = lato * lato;
        } else {
            cout << "Impossibile calcolare: Dati insufficienti." << endl;
        }
    }

    void stampaRisultato() const override {
        cout << "###Risultato per " << tipoFigura << "###" << endl;
        if (lato > 0) cout << "Lato: " << fixed << setprecision(2) << lato << endl;
        if (perimetro > 0) cout << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) cout << "Area: " << fixed << setprecision(2) << area << endl;
        if (diagonale > 0) cout << "Diagonale: " << fixed << setprecision(2) << diagonale << endl;
    }

    string getRisultatoFormattato() const override {
        stringstream ss;
        ss << "--- " << tipoFigura << " ---" << endl;
        if (lato > 0) ss << "Lato: " << fixed << setprecision(2) << lato << endl;
        if (perimetro > 0) ss << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) ss << "Area: " << fixed << setprecision(2) << area << endl;
        if (diagonale > 0) ss << "Diagonale: " << fixed << setprecision(2) << diagonale << endl;
        return ss.str();
    }

    void setParametro(const string& nomeParametro, double valore) override {
        string paramLower = nomeParametro;
        transform(paramLower.begin(), paramLower.end(), paramLower.begin(), ::tolower);
        if (paramLower == "lato") lato = valore;
        else if (paramLower == "perimetro") perimetro = valore;
        else if (paramLower == "area") area = valore;
        else if (paramLower == "diagonale") diagonale = valore;
        else cerr << "Avviso: Parametro '" << nomeParametro << "' non riconosciuto per Quadrato." << endl;
    }
};

// Classe per un Rettangolo
class Rettangolo : public FiguraGeometrica {
public:
    double base;      // Base
    double altezza;   // Altezza
    double perimetro; // Perimetro
    double area;      // Area
    double diagonale; // Diagonale

    Rettangolo() : FiguraGeometrica("Rettangolo"), base(0.0), altezza(0.0), perimetro(0.0), area(0.0), diagonale(0.0) {}

    // Metodo per ottenere i dati dall'input dell'utente
    void inserisciDati() override {
        string input;
        cout << "Inserire la base del rettangolo (o '?' se sconosciuta): ";
        cin >> input;
        if (input == "?") base = -1.0;
        else {
            try { base = stod(input); }
            catch (...) { cerr << "Errore: Input non numerico per la base." << endl; base = 0.0; }
        }

        cout << "Inserire l'altezza del rettangolo (o '?' se sconosciuta): ";
        cin >> input;
        if (input == "?") altezza = -1.0;
        else {
            try { altezza = stod(input); }
            catch (...) { cerr << "Errore: Input non numerico per l'altezza." << endl; altezza = 0.0; }
        }
    }

    // Metodo per calcolare il perimetro, l'area e la diagonale sulla base di valori noti.
    void calcola() override {
        if (base > 0 && altezza > 0) {
            perimetro = 2 * (base + altezza);
            area = base * altezza;
            diagonale = sqrt(base * base + altezza * altezza);
        } else if (base > 0 && area > 0) { // If base and area are known
            altezza = area / base;
            perimetro = 2 * (base + altezza);
            diagonale = sqrt(base * base + altezza * altezza);
        } else if (altezza > 0 && area > 0) { // If height and area are known
            base = area / altezza;
            perimetro = 2 * (base + altezza);
            diagonale = sqrt(base * base + altezza * altezza);
        } else {
            cout << "Impossibile calcolare: Dati insufficienti." << endl;
        }
    }

    // Metodo per stampare i risultati calcolati
    void stampaRisultato() const override {
        cout << "###Risultato per " << tipoFigura << "###" << endl;
        if (base > 0) cout << "Base: " << fixed << setprecision(2) << base << endl;
        if (altezza > 0) cout << "Altezza: " << fixed << setprecision(2) << altezza << endl;
        if (perimetro > 0) cout << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) cout << "Area: " << fixed << setprecision(2) << area << endl;
        if (diagonale > 0) cout << "Diagonale: " << fixed << setprecision(2) << diagonale << endl;
    }

    // Metodo per ottenere una stringa formattata dei risultati (per l'output su file)
    string getRisultatoFormattato() const override {
        stringstream ss;
        ss << "--- " << tipoFigura << " ---" << endl;
        if (base > 0) ss << "Base: " << fixed << setprecision(2) << base << endl;
        if (altezza > 0) ss << "Altezza: " << fixed << setprecision(2) << altezza << endl;
        if (perimetro > 0) ss << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) ss << "Area: " << fixed << setprecision(2) << area << endl;
        if (diagonale > 0) ss << "Diagonale: " << fixed << setprecision(2) << diagonale << endl;
        return ss.str();
    }

    // Metodo per impostare un parametro specifico per nome (utilizzato per l'inserimento di file)
    void setParametro(const string& nomeParametro, double valore) override {
        string paramLower = nomeParametro;
        transform(paramLower.begin(), paramLower.end(), paramLower.begin(), ::tolower); // Convert to lowercase
        if (paramLower == "base") {
            base = valore;
        } else if (paramLower == "altezza") {
            altezza = valore;
        } else if (paramLower == "perimetro") {
            perimetro = valore;
        } else if (paramLower == "area") {
            area = valore;
        } else if (paramLower == "diagonale") {
            diagonale = valore;
        } else {
            cerr << "Avviso: Parametro '" << nomeParametro << "' non riconosciuto per Rettangolo." << endl;
        }
    }
};

// Classe per un Triangolo Isoscele
class TriangoloIsoscele : public FiguraGeometrica {
public:
    double base;        // Lunghezza della base
    double latoObliquo; // Lunghezza del lato uguale
    double altezza;     // Altezza
    double perimetro;   // Perimetro
    double area;        // Area

    TriangoloIsoscele() : FiguraGeometrica("Triangolo Isoscele"), base(0.0), latoObliquo(0.0), altezza(0.0), perimetro(0.0), area(0.0) {}

    // Metodo per ottenere i dati dall'input dell'utente
    void inserisciDati() override {
        base = getDoubleInput("Inserire la base del triangolo isoscele (o '?' se sconosciuta): ");
        latoObliquo = getDoubleInput("Inserire il lato obliquo del triangolo isoscele (o '?' se sconosciuto): ");
        altezza = getDoubleInput("Inserire l'altezza del triangolo isoscele (o '?' se sconosciuta): ");
    }

    // Metodo per calcolare le proprietà sulla base di valori noti
    void calcola() override {
        if (base > 0 && latoObliquo > 0) {
            if (latoObliquo * latoObliquo - (base / 2) * (base / 2) >= 0) { // Check for valid triangle
                altezza = sqrt(latoObliquo * latoObliquo - (base / 2) * (base / 2));
                perimetro = base + 2 * latoObliquo;
                area = (base * altezza) / 2;
            } else {
                cerr << "Errore: Un triangolo isoscele con questi lati non è possibile." << endl;
            }
        }
        else if (base > 0 && altezza > 0) {
            latoObliquo = sqrt(altezza * altezza + (base / 2) * (base / 2));
            perimetro = base + 2 * latoObliquo;
            area = (base * altezza) / 2;
        }
        else if (latoObliquo > 0 && altezza > 0) {
            if (latoObliquo * latoObliquo - altezza * altezza >= 0) {
                base = 2 * sqrt(latoObliquo * latoObliquo - altezza * altezza);
                perimetro = base + 2 * latoObliquo;
                area = (base * altezza) / 2;
            } else {
                cerr << "Errore: Un triangolo isoscele con questi lati non è possibile." << endl;
            }
        }
        else if (area > 0 && base > 0) {
            altezza = (2 * area) / base;
            latoObliquo = sqrt(altezza * altezza + (base / 2) * (base / 2));
            perimetro = base + 2 * latoObliquo;
        }
        else if (area > 0 && altezza > 0) {
            base = (2 * area) / altezza;
            latoObliquo = sqrt(altezza * altezza + (base / 2) * (base / 2));
            perimetro = base + 2 * latoObliquo;
        }
        else {
            cout << "Impossibile calcolare: Dati insufficienti per il triangolo isoscele." << endl;
        }
    }

    // Metodo per stampare i risultati calcolati
    void stampaRisultato() const override {
        cout << "###Risultato per " << tipoFigura << "###" << endl;
        if (base > 0) cout << "Base: " << fixed << setprecision(2) << base << endl;
        if (latoObliquo > 0) cout << "Lato Obliquo: " << fixed << setprecision(2) << latoObliquo << endl;
        if (altezza > 0) cout << "Altezza: " << fixed << setprecision(2) << altezza << endl;
        if (perimetro > 0) cout << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) cout << "Area: " << fixed << setprecision(2) << area << endl;
    }

    string getRisultatoFormattato() const override {
        stringstream ss;
        ss << "--- " << tipoFigura << " ---" << endl;
        if (base > 0) ss << "Base: " << fixed << setprecision(2) << base << endl;
        if (latoObliquo > 0) ss << "Lato Obliquo: " << fixed << setprecision(2) << latoObliquo << endl;
        if (altezza > 0) ss << "Altezza: " << fixed << setprecision(2) << altezza << endl;
        if (perimetro > 0) ss << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) ss << "Area: " << fixed << setprecision(2) << area << endl;
        return ss.str();
    }

    // Metodo per impostare un parametro specifico per nome (utilizzato per l'inserimento di file)
    void setParametro(const string& nomeParametro, double valore) override {
        string paramLower = nomeParametro;
        transform(paramLower.begin(), paramLower.end(), paramLower.begin(), ::tolower); // Convert to lowercase
        if (paramLower == "base") {
            base = valore;
        } else if (paramLower == "latoobliquo") {
            latoObliquo = valore;
        } else if (paramLower == "altezza") {
            altezza = valore;
        } else if (paramLower == "perimetro") {
            perimetro = valore;
        } else if (paramLower == "area") {
            area = valore;
        } else {
            cerr << "Avviso: Parametro '" << nomeParametro << "' non riconosciuto per Triangolo Isoscele." << endl;
        }
    }
};

// Classe per un Triangolo Rettangolo
class TriangoloRettangolo : public FiguraGeometrica {
public:
    double cateto1;   // Cateto 1
    double cateto2;   // Cateto 2
    double ipotenusa; // Ipotenusa
    double perimetro; // Perimetro
    double area;      // Area

    TriangoloRettangolo() : FiguraGeometrica("Triangolo Rettangolo"), cateto1(0.0), cateto2(0.0), ipotenusa(0.0), perimetro(0.0), area(0.0) {}

    // Metodo per ottenere i dati dall'input dell'utente
    void inserisciDati() override {
        cateto1 = getDoubleInput("Inserire il primo cateto del triangolo rettangolo (o '?' se sconosciuto): ");
        cateto2 = getDoubleInput("Inserire il secondo cateto del triangolo rettangolo (o '?' se sconosciuto): ");
        ipotenusa = getDoubleInput("Inserire l'ipotenusa del triangolo rettangolo (o '?' se sconosciuta): ");
    }

    // Metodo per calcolare le proprietà sulla base di valori noti
    void calcola() override {
        // If both legs are known, calculate hypotenuse, perimeter, area
        if (cateto1 > 0 && cateto2 > 0) {
            ipotenusa = sqrt(cateto1 * cateto1 + cateto2 * cateto2);
            perimetro = cateto1 + cateto2 + ipotenusa;
            area = (cateto1 * cateto2) / 2;
        }
        // Se un cateto e l'ipotenusa sono note, calcolare l'altro cateto, il perimetro, l'area e la superficie.
        else if (cateto1 > 0 && ipotenusa > 0) {
            if (ipotenusa * ipotenusa - cateto1 * cateto1 >= 0) { // Check for valid triangle
                cateto2 = sqrt(ipotenusa * ipotenusa - cateto1 * cateto1);
                perimetro = cateto1 + cateto2 + ipotenusa;
                area = (cateto1 * cateto2) / 2;
            } else {
                cerr << "Errore: Triangolo rettangolo non possibile (il cateto non può essere maggiore dell'ipotenusa)." << endl;
            }
        }
        else if (cateto2 > 0 && ipotenusa > 0) {
            if (ipotenusa * ipotenusa - cateto2 * cateto2 >= 0) { // Check for valid triangle
                cateto1 = sqrt(ipotenusa * ipotenusa - cateto2 * cateto2);
                perimetro = cateto1 + cateto2 + ipotenusa;
                area = (cateto1 * cateto2) / 2;
            } else {
                cerr << "Errore: Triangolo rettangolo non possibile (il cateto non può essere maggiore dell'ipotenusa)." << endl;
            }
        }
        // Se l'area e un cateo sono noti, calcolare l'altro cateto, l'ipotenusa e il perimetro.
        else if (area > 0 && cateto1 > 0) {
            cateto2 = (2 * area) / cateto1;
            ipotenusa = sqrt(cateto1 * cateto1 + cateto2 * cateto2);
            perimetro = cateto1 + cateto2 + ipotenusa;
        }
        else if (area > 0 && cateto2 > 0) {
            cateto1 = (2 * area) / cateto2;
            ipotenusa = sqrt(cateto1 * cateto1 + cateto2 * cateto2);
            perimetro = cateto1 + cateto2 + ipotenusa;
        }
        else {
            cout << "Impossibile calcolare: Dati insufficienti per il triangolo rettangolo." << endl;
        }
    }

    // Metodo per stampare i risultati calcolati
    void stampaRisultato() const override {
        cout << "###Risultato per " << tipoFigura << "###" << endl;
        if (cateto1 > 0) cout << "Cateto 1: " << fixed << setprecision(2) << cateto1 << endl;
        if (cateto2 > 0) cout << "Cateto 2: " << fixed << setprecision(2) << cateto2 << endl;
        if (ipotenusa > 0) cout << "Ipotenusa: " << fixed << setprecision(2) << ipotenusa << endl;
        if (perimetro > 0) cout << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) cout << "Area: " << fixed << setprecision(2) << area << endl;
    }

    string getRisultatoFormattato() const override {
        stringstream ss;
        ss << "--- " << tipoFigura << " ---" << endl;
        if (cateto1 > 0) ss << "Cateto 1: " << fixed << setprecision(2) << cateto1 << endl;
        if (cateto2 > 0) ss << "Cateto 2: " << fixed << setprecision(2) << cateto2 << endl;
        if (ipotenusa > 0) ss << "Ipotenusa: " << fixed << setprecision(2) << ipotenusa << endl;
        if (perimetro > 0) ss << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) ss << "Area: " << fixed << setprecision(2) << area << endl;
        return ss.str();
    }

    // Metodo per impostare un parametro specifico per nome (utilizzato per l'inserimento di file)
    void setParametro(const string& nomeParametro, double valore) override {
        string paramLower = nomeParametro;
        transform(paramLower.begin(), paramLower.end(), paramLower.begin(), ::tolower); // Convert to lowercase
        if (paramLower == "cateto1" || paramLower == "cateto_1") {
            cateto1 = valore;
        } else if (paramLower == "cateto2" || paramLower == "cateto_2") {
            cateto2 = valore;
        } else if (paramLower == "ipotenusa") {
            ipotenusa = valore;
        } else if (paramLower == "perimetro") {
            perimetro = valore;
        } else if (paramLower == "area") {
            area = valore;
        } else {
            cerr << "Avviso: Parametro '" << nomeParametro << "' non riconosciuto per Triangolo Rettangolo." << endl;
        }
    }
};

// Classe per un Triangolo Equilatero
class TriangoloEquilatero : public FiguraGeometrica {
public:
    double lato;        // Lato
    double altezza;     // Altezza
    double perimetro;   // Perimetro
    double area;        // Area

    TriangoloEquilatero() : FiguraGeometrica("Triangolo Equilatero"), lato(0.0), altezza(0.0), perimetro(0.0), area(0.0) {}

    // Metodo per ottenere i dati dall'input dell'utente
    void inserisciDati() override {
        lato = getDoubleInput("Inserire la lunghezza del lato del triangolo equilatero (o '?' se sconosciuta): ");
    }

    // Metodo per calcolare le proprietà sulla base di valori noti
    void calcola() override {
        if (lato > 0) {
            perimetro = 3 * lato;
            altezza = (lato * sqrt(3)) / 2;
            area = (lato * lato * sqrt(3)) / 4;
        } else if (perimetro > 0) { // If perimeter is known
            lato = perimetro / 3;
            altezza = (lato * sqrt(3)) / 2;
            area = (lato * lato * sqrt(3)) / 4;
        } else if (altezza > 0) { // If height is known
            lato = (2 * altezza) / sqrt(3);
            perimetro = 3 * lato;
            area = (lato * lato * sqrt(3)) / 4;
        } else if (area > 0) { // If area is known
            lato = sqrt((4 * area) / sqrt(3));
            perimetro = 3 * lato;
            altezza = (lato * sqrt(3)) / 2;
        } else {
            cout << "Impossibile calcolare: Dati insufficienti per il triangolo equilatero." << endl;
        }
    }

    // Metodo per stampare i risultati calcolati
    void stampaRisultato() const override {
        cout << "###Risultato per " << tipoFigura << "###" << endl;
        if (lato > 0) cout << "Lato: " << fixed << setprecision(2) << lato << endl;
        if (altezza > 0) cout << "Altezza: " << fixed << setprecision(2) << altezza << endl;
        if (perimetro > 0) cout << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) cout << "Area: " << fixed << setprecision(2) << area << endl;
    }

    string getRisultatoFormattato() const override {
        stringstream ss;
        ss << "--- " << tipoFigura << " ---" << endl;
        if (lato > 0) ss << "Lato: " << fixed << setprecision(2) << lato << endl;
        if (altezza > 0) ss << "Altezza: " << fixed << setprecision(2) << altezza << endl;
        if (perimetro > 0) ss << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) ss << "Area: " << fixed << setprecision(2) << area << endl;
        return ss.str();
    }

    // Metodo per impostare un parametro specifico per nome (utilizzato per l'inserimento di file)
    void setParametro(const string& nomeParametro, double valore) override {
        string paramLower = nomeParametro;
        transform(paramLower.begin(), paramLower.end(), paramLower.begin(), ::tolower); // Convert to lowercase
        if (paramLower == "lato") {
            lato = valore;
        } else if (paramLower == "altezza") {
            altezza = valore;
        } else if (paramLower == "perimetro") {
            perimetro = valore;
        } else if (paramLower == "area") {
            area = valore;
        } else {
            cerr << "Avviso: Parametro '" << nomeParametro << "' non riconosciuto per Triangolo Equilatero." << endl;
        }
    }
};

// Classe per un Triangolo Scaleno
class TriangoloScaleno : public FiguraGeometrica {
public:
    double latoA;     // Side A
    double latoB;     // Side B
    double latoC;     // Side C
    double perimetro; // Perimeter
    double area;      // Area

    TriangoloScaleno() : FiguraGeometrica("Triangolo Scaleno"), latoA(0.0), latoB(0.0), latoC(0.0), perimetro(0.0), area(0.0) {}

    // Metodo per ottenere dati da input dell'utente
    void inserisciDati() override {
        latoA = getDoubleInput("Inserire il lato A del triangolo scaleno (o '?' se sconosciuto): ");
        latoB = getDoubleInput("Inserire il lato B del triangolo scaleno (o '?' se sconosciuto): ");
        latoC = getDoubleInput("Inserire il lato C del triangolo scaleno (o '?' se sconosciuto): ");
    }

    // Metodo per calcolare le proprietà sulla base di valori noti
    void calcola() override {
        if (latoA > 0 && latoB > 0 && latoC > 0) {
            // Check triangle inequality theorem
            if (latoA + latoB > latoC && latoA + latoC > latoB && latoB + latoC > latoA) {
                perimetro = latoA + latoB + latoC;
                // Heron's formula for area
                double s = perimetro / 2; // semi-perimeter
                area = sqrt(s * (s - latoA) * (s - latoB) * (s - latoC));
            } else {
                cerr << "Errore: Un triangolo con queste lunghezze di lato non è possibile (viola la disuguaglianza triangolare)." << endl;
            }
        } else {
            cout << "Impossibile calcolare: Per calcolare area/perimetro di un triangolo scaleno, tutti e tre i lati devono essere noti." << endl;
        }
    }

    // Metodo per stampare i risultati calcolati
    void stampaRisultato() const override {
        cout << "###Risultato per " << tipoFigura << "###" << endl;
        if (latoA > 0) cout << "Lato A: " << fixed << setprecision(2) << latoA << endl;
        if (latoB > 0) cout << "Lato B: " << fixed << setprecision(2) << latoB << endl;
        if (latoC > 0) cout << "Lato C: " << fixed << setprecision(2) << latoC << endl;
        if (perimetro > 0) cout << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) cout << "Area: " << fixed << setprecision(2) << area << endl;
    }

    string getRisultatoFormattato() const override {
        stringstream ss;
        ss << "--- " << tipoFigura << " ---" << endl;
        if (latoA > 0) ss << "Lato A: " << fixed << setprecision(2) << latoA << endl;
        if (latoB > 0) ss << "Lato B: " << fixed << setprecision(2) << latoB << endl;
        if (latoC > 0) ss << "Lato C: " << fixed << setprecision(2) << latoC << endl;
        if (perimetro > 0) ss << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) ss << "Area: " << fixed << setprecision(2) << area << endl;
        return ss.str();
    }

    // Metodo per impostare un parametro specifico per nome (utilizzato per l'inserimento di file)
    void setParametro(const string& nomeParametro, double valore) override {
        string paramLower = nomeParametro;
        transform(paramLower.begin(), paramLower.end(), paramLower.begin(), ::tolower); // Convert to lowercase
        if (paramLower == "latoa" || paramLower == "lato_a") {
            latoA = valore;
        } else if (paramLower == "latob" || paramLower == "lato_b") {
            latoB = valore;
        } else if (paramLower == "latoc" || paramLower == "lato_c") {
            latoC = valore;
        } else if (paramLower == "perimetro") {
            perimetro = valore;
        } else if (paramLower == "area") {
            area = valore;
        } else {
            cerr << "Avviso: Parametro '" << nomeParametro << "' non riconosciuto per Triangolo Scaleno." << endl;
        }
    }
};

// Classe per un Rombo
class Rombo : public FiguraGeometrica {
public:
    double lato;        // Side length (all sides are equal)
    double diagonaleMaggiore; // Major diagonal
    double diagonaleMinore;   // Minor diagonal
    double perimetro;   // Perimeter
    double area;        // Area

    Rombo() : FiguraGeometrica("Rombo"), lato(0.0), diagonaleMaggiore(0.0), diagonaleMinore(0.0), perimetro(0.0), area(0.0) {}

    // Metodo per ottenere dati da input dell'utente
    void inserisciDati() override {
        lato = getDoubleInput("Inserire la lunghezza del lato del rombo (o '?' se sconosciuta): ");
        diagonaleMaggiore = getDoubleInput("Inserire la diagonale maggiore del rombo (o '?' se sconosciuta): ");
        diagonaleMinore = getDoubleInput("Inserire la diagonale minore del rombo (o '?' se sconosciuta): ");
    }

    // Metodo per calcolare le proprietà sulla base di valori noti
    void calcola() override {
        // Se entrambe le diagonali sono note, calcolare l'area, poi il lato, quindi il perimetro.
        if (diagonaleMaggiore > 0 && diagonaleMinore > 0) {
            area = (diagonaleMaggiore * diagonaleMinore) / 2;
            lato = sqrt(pow(diagonaleMaggiore / 2, 2) + pow(diagonaleMinore / 2, 2));
            perimetro = 4 * lato;
        }
        // Se il lato e la diagonale maggiore sono noti, calcolare la diagonale minore, quindi l'area e il perimetro.
        else if (lato > 0 && diagonaleMaggiore > 0) {
            double halfDiagMajSq = pow(diagonaleMaggiore / 2, 2);
            if (lato * lato - halfDiagMajSq >= 0) {
                diagonaleMinore = 2 * sqrt(lato * lato - halfDiagMajSq);
                area = (diagonaleMaggiore * diagonaleMinore) / 2;
                perimetro = 4 * lato;
            } else {
                cerr << "Errore: Un rombo con questi valori non è possibile (lato troppo corto per la diagonale)." << endl;
            }
        }
        // Se il lato e la diagonale minore sono noti, calcolare la diagonale maggiore, quindi l'area e il perimetro.
        else if (lato > 0 && diagonaleMinore > 0) {
            double halfDiagMinSq = pow(diagonaleMinore / 2, 2);
            if (lato * lato - halfDiagMinSq >= 0) {
                diagonaleMaggiore = 2 * sqrt(lato * lato - halfDiagMinSq);
                area = (diagonaleMaggiore * diagonaleMinore) / 2;
                perimetro = 4 * lato;
            } else {
                cerr << "Errore: Un rombo con questi valori non è possibile (lato troppo corto per la diagonale)." << endl;
            }
        }
        // Se l'area e la diagonale maggiore sono note, calcolare la diagonale minore, poi il lato e infine il perimetro.
        else if (area > 0 && diagonaleMaggiore > 0) {
            diagonaleMinore = (2 * area) / diagonaleMaggiore;
            lato = sqrt(pow(diagonaleMaggiore / 2, 2) + pow(diagonaleMinore / 2, 2));
            perimetro = 4 * lato;
        }
        // Se si conoscono l'area e la diagonale minore, si calcola la diagonale maggiore, poi il lato e infine il perimetro.
        else if (area > 0 && diagonaleMinore > 0) {
            diagonaleMaggiore = (2 * area) / diagonaleMinore;
            lato = sqrt(pow(diagonaleMaggiore / 2, 2) + pow(diagonaleMinore / 2, 2));
            perimetro = 4 * lato;
        }
        // Se lato e perimetro sono noti 
        else if (lato > 0 && perimetro > 0 && perimetro == 4 * lato) {
            // Nothing new to calculate based on this combination if not diagonals/area
            cout << "Lato e Perimetro noti. Nessuna proprietà aggiuntiva può essere calcolata senza diagonali o area." << endl;
        }
        else {
            cout << "Impossibile calcolare: Dati insufficienti per il rombo. Sono necessarie almeno due proprietà (es. entrambe le diagonali, o lato e una diagonale)." << endl;
        }
    }

    // Metodo per stampare i risultati calcolati
    void stampaRisultato() const override {
        cout << "###Risultato per " << tipoFigura << "###" << endl;
        if (lato > 0) cout << "Lato: " << fixed << setprecision(2) << lato << endl;
        if (diagonaleMaggiore > 0) cout << "Diagonale Maggiore: " << fixed << setprecision(2) << diagonaleMaggiore << endl;
        if (diagonaleMinore > 0) cout << "Diagonale Minore: " << fixed << setprecision(2) << diagonaleMinore << endl;
        if (perimetro > 0) cout << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) cout << "Area: " << fixed << setprecision(2) << area << endl;
    }

    string getRisultatoFormattato() const override {
        stringstream ss;
        ss << "--- " << tipoFigura << " ---" << endl;
        if (lato > 0) ss << "Lato: " << fixed << setprecision(2) << lato << endl;
        if (diagonaleMaggiore > 0) ss << "Diagonale Maggiore: " << fixed << setprecision(2) << diagonaleMaggiore << endl;
        if (diagonaleMinore > 0) ss << "Diagonale Minore: " << fixed << setprecision(2) << diagonaleMinore << endl;
        if (perimetro > 0) ss << "Perimetro: " << fixed << setprecision(2) << perimetro << endl;
        if (area > 0) ss << "Area: " << fixed << setprecision(2) << area << endl;
        return ss.str();
    }

    // Metodo per impostare un parametro specifico 
    void setParametro(const string& nomeParametro, double valore) override {
        string paramLower = nomeParametro;
        transform(paramLower.begin(), paramLower.end(), paramLower.begin(), ::tolower); // Convert to lowercase
        if (paramLower == "lato") {
            lato = valore;
        } else if (paramLower == "diagonalemaggiore" || paramLower == "diag_maggiore") {
            diagonaleMaggiore = valore;
        } else if (paramLower == "diagonaleminore" || paramLower == "diag_minore") {
            diagonaleMinore = valore;
        } else if (paramLower == "perimetro") {
            perimetro = valore;
        } else if (paramLower == "area") {
            area = valore;
        } else {
            cerr << "Avviso: Parametro '" << nomeParametro << "' non riconosciuto per Rombo." << endl;
        }
    }
};


// Funzione per leggere il tipo di figura e i dati dal file.
// Restituisce un vettore di unique_ptr alle figure create.
std::vector<std::unique_ptr<FiguraGeometrica>> leggiFigureDaFile(const string& filename) {
    std::vector<std::unique_ptr<FiguraGeometrica>> figureLetta;
    ifstream fin(filename);
    if (!fin.is_open()) {
        cerr << "Errore: Impossibile aprire il file " << filename << endl;
        return figureLetta; // Restituisce un vettore vuoto
    }

    string content((istreambuf_iterator<char>(fin)), istreambuf_iterator<char>());
    fin.close();

    // Dividi il contenuto per il delimitatore ';'
    stringstream ss_content(content);
    string segment;

    while (getline(ss_content, segment, ';')) {
        // Rimuovi spazi extra o a capo all'inizio/fine del segmento
        segment.erase(0, segment.find_first_not_of(" \t\r\n"));
        segment.erase(segment.find_last_not_of(" \t\r\n") + 1);

        if (segment.empty()) continue; // Salta segmenti vuoti

        stringstream ss_segment(segment);
        string token;
        vector<string> tokens;

        // Estrai i token separati da virgola all'interno del segmento
        while (getline(ss_segment, token, ',')) {
            token.erase(0, token.find_first_not_of(" \t\r\n"));
            token.erase(token.find_last_not_of(" \t\r\n") + 1);
            tokens.push_back(token);
        }

        if (tokens.empty()) continue; // Salta se nessun token dopo il parsing del segmento

        string figuraTipoStr = tokens[0];
        transform(figuraTipoStr.begin(), figuraTipoStr.end(), figuraTipoStr.begin(), ::tolower);

        std::unique_ptr<FiguraGeometrica> figura;

        if (figuraTipoStr == "quadrato") {
            figura = std::make_unique<Quadrato>();
        } else if (figuraTipoStr == "rettangolo") {
            figura = std::make_unique<Rettangolo>();
        } else if (figuraTipoStr == "rombo") {
            figura = std::make_unique<Rombo>();
        } else if (figuraTipoStr == "triangolo isoscele") {
            figura = std::make_unique<TriangoloIsoscele>();
        } else if (figuraTipoStr == "triangolo rettangolo") {
            figura = std::make_unique<TriangoloRettangolo>();
        } else if (figuraTipoStr == "triangolo equilatero") {
            figura = std::make_unique<TriangoloEquilatero>();
        } else if (figuraTipoStr == "triangolo scaleno") {
            figura = std::make_unique<TriangoloScaleno>();
        } else {
            cerr << "Errore: Tipo di figura '" << figuraTipoStr << "' non riconosciuto in un segmento del file. Saltato." << endl;
            continue; // Salta questa figura e prova la successiva
        }

        // Imposta i parametri per la figura creata
        for (size_t i = 2; i < tokens.size(); i += 2) {
            if (i + 1 < tokens.size()) { // Assicurati che ci sia un valore per il parametro
                string nomeParametro = tokens[i];
                string valoreStr = tokens[i+1];

                double valore;
                if (valoreStr == "?") {
                    valore = -1.0; // Valore sentinella per sconosciuto
                } else {
                    try {
                        valore = stod(valoreStr);
                    } catch (const invalid_argument& e) {
                        cerr << "Errore di parsing: Valore non numerico per '" << nomeParametro << "': " << valoreStr << endl;
                        valore = 0.0; // Valore predefinito in caso di errore
                    } catch (const out_of_range& e) {
                        cerr << "Errore di parsing: Valore fuori intervallo per '" << nomeParametro << "': " << valoreStr << endl;
                        valore = 0.0;
                    }
                }
                if (figura) {
                    figura->setParametro(nomeParametro, valore);
                }
            }
        }
        figureLetta.push_back(std::move(figura)); // Aggiungi la figura al vettore
    }
    return figureLetta;
}

// Funzione per scrivere i risultati su un file
void scriviRisultatiSuFile(const string& filename, const std::vector<std::string>& risultati) {
    ofstream fout(filename);
    if (!fout.is_open()) {
        cerr << "Errore: Impossibile creare o aprire il file di output " << filename << endl;
        return;
    }

    for (const string& res : risultati) {
        fout << res << "\n"; // Scrivi ogni risultato e una nuova riga
    }
    fout.close();
    cout << "\nRisultati scritti nel file: " << filename << endl;
}


// --- Funzione Main ---
int main() {
    string tipoInput;
    cout << "Scegli il tipo di input ('tastiera' per la tastiera o 'file'): ";
    cin >> tipoInput;


    // Converti l'input in minuscolo per un confronto flessibile
    transform(tipoInput.begin(), tipoInput.end(), tipoInput.begin(), ::tolower);

    // Dopo aver letto tipoInput con cin, c'è un newline residuo nel buffer, puliamolo
    cin.ignore(numeric_limits<streamsize>::max(), '\n');


    if (tipoInput != INPUT_TASTIERA && tipoInput != INPUT_FILE) {
        cerr << "Errore: Tipo di input non valido. Scegli 'tastiera' o 'file'." << endl;
        // Aspetta un input prima di uscire in caso di errore iniziale
        cout << "\nPremere un tasto qualsiasi per continuare...";
        cin.get();
        return 1;
    }

    std::vector<std::unique_ptr<FiguraGeometrica>> figureDaElaborare;
    string nomeFileOutput = ""; // Inizializza il nome del file di output

    if (tipoInput == INPUT_TASTIERA) {
        string figuraScelta;
        cout << "Scegli la figura geometrica (Quadrato, Rettangolo, Rombo, Triangolo isoscele, Triangolo rettangolo, Triangolo Equilatero, Triangolo Scaleno): ";
        getline(cin, figuraScelta); // Usa getline per nomi di figure con più parole

        // Converti l'input in minuscolo
        transform(figuraScelta.begin(), figuraScelta.end(), figuraScelta.begin(), ::tolower);

        std::unique_ptr<FiguraGeometrica> figura; // Crea una singola figura

        // Crea l'oggetto figura appropriato in base alla scelta dell'utente
        if (figuraScelta == "quadrato") {
            figura = std::make_unique<Quadrato>();
        } else if (figuraScelta == "rettangolo") {
            figura = std::make_unique<Rettangolo>();
        } else if (figuraScelta == "rombo") {
            figura = std::make_unique<Rombo>();
        } else if (figuraScelta == "triangolo isoscele") {
            figura = std::make_unique<TriangoloIsoscele>();
        } else if (figuraScelta == "triangolo rettangolo") {
            figura = std::make_unique<TriangoloRettangolo>();
        } else if (figuraScelta == "triangolo equilatero") {
            figura = std::make_unique<TriangoloEquilatero>();
        } else if (figuraScelta == "triangolo scaleno") {
            figura = std::make_unique<TriangoloScaleno>();
        }

        if (figura == nullptr) { // Check if a valid figure was created
            cerr << "Errore: Figura geometrica non riconosciuta o supportata." << endl;
            // Aspetta un input prima di uscire in caso di errore
            cout << "\nPremere un tasto qualsiasi per continuare...";
            cin.get();
            return 1;
        }
        // Get data from user input
        figura->inserisciDati();
        figureDaElaborare.push_back(std::move(figura)); // Aggiungi la singola figura al vettore
        cout << "Inserisci il nome del file di output per i risultati (es. risultati.txt): ";
        getline(cin, nomeFileOutput);

    } else { // INPUT_FILE
        string nomeFile;
        cout << "Inserire il nome del file di input: ";
        getline(cin, nomeFile);
        // Chiamiamo la nuova funzione che legge il tipo di figura e i dati dal file
        figureDaElaborare = leggiFigureDaFile(nomeFile);
        if (figureDaElaborare.empty()) {
            cerr << "Nessuna figura valida trovata nel file. Uscita." << endl;
            // Aspetta un input prima di uscire in caso di errore
            cout << "\nPremere un tasto qualsiasi per continuare...";
            cin.get();
            return 1; // Exit if file reading or figure creation failed
        }
        cout << "Inserisci il nome del file di output per i risultati (es. risultati.txt): ";
        getline(cin, nomeFileOutput);
    }

    std::vector<std::string> risultatiComplessivi;

    // Processa tutte le figure lette/create
    for (const auto& figura : figureDaElaborare) {
        if (figura) { // Assicurati che la figura sia valida
            figura->calcola(); // Esegui i calcoli per la figura selezionata
            figura->stampaRisultato(); // Stampa i risultati a schermo
            risultatiComplessivi.push_back(figura->getRisultatoFormattato()); // Aggiungi il risultato formattato al vettore
        }
    }

    // Scrivi tutti i risultati nel file di output
    if (!nomeFileOutput.empty()) {
        scriviRisultatiSuFile(nomeFileOutput, risultatiComplessivi);
    }


    cout << "\nPremere un tasto qualsiasi e poi invio per uscire...";

    if (cin.peek() == '\n') { // Controlla se c'è un newline nel buffer senza rimuoverlo
        cin.ignore(numeric_limits<streamsize>::max(), '\n'); // Se c'è, puliscilo
    }
    cin.get(); // Aspetta un singolo carattere (o il newline se ancora presente e non pulito)
  

    return 0;
}
