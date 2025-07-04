import random # Used for picking random characters and shuffling the password
import string # Provides handy sets of characters like all lowercase letters, all digits, etc.
import argparse # This is what allows us to create easy-to-use commands
import sys # Helps us exit the program nicely if something goes wrong
import os # Used to check if your custom dictionary file actually exists

# --- Default Symbol Set ---
# Defines the standard set of special characters used by the generator unless a custom set is provided.
DEFAULT_SYMBOLS = string.punctuation

# --- Function to load words from a file ---
def load_words_from_file(filepath):
    """
    This function attempts to load a list of words from a specified file path.
    It expects words within the file to be comma-separated.
    In case of file not found errors, empty files, or invalid formatting,
    it will issue a warning and return an empty list, prompting the use of internal word lists.
    """
    # Verifies the existence of the provided file path.
    if not os.path.exists(filepath):
        print(f"Error: Dictionary file not found at '{filepath}'. Using internal word lists.", file=sys.stderr)
        return [] # Returns an empty list if the file does not exist.
    
    try:
        # Opens and reads the file content.
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip() # Reads all content and removes leading/trailing whitespace.
            if not content:
                print(f"Warning: Dictionary file '{filepath}' is empty. Using internal word lists.", file=sys.stderr)
                return [] # Returns an empty list if the file is empty.
            
            # Splits the content by commas and strips whitespace from each word.
            words = [word.strip() for word in content.split(',') if word.strip()]
            if not words:
                print(f"Warning: No valid words found in '{filepath}'. Expected comma-separated words. Using internal word lists.", file=sys.stderr)
            return words # Returns the processed list of words.
    except Exception as e:
        # Catches and reports any errors encountered during file reading.
        print(f"Error reading dictionary file '{filepath}': {e}. Using internal word lists.", file=sys.stderr)
        return [] # Returns an empty list upon an error.

# --- Internal Word Lists (Fallback mechanism) ---
# These predefined lists of common Italian and English words serve as a fallback
# if no custom dictionary file is provided or if its loading fails.
ITALIAN_WORDS = [
    "essere", "avere", "dire", "potere", "volere", "sapere", "stare", "dovere",
    "vedere", "andare", "venire", "dare", "parlare", "trovare", "sentire", "lasciare",
    "prendere", "pensare", "passare", "portare", "sembrare", "usare", "pagare", "camminare",
    "iniziare", "tornare", "chiamare", "morire", "vivere", "amare", "conoscere", "lavorare",
    "mangiare", "bere", "dormire", "studiare", "scrivere", "leggere", "guardare", "ascoltare",
    "comprare", "vendere", "aprire", "chiudere", "mettere", "tenere", "cercare", "mostrare",
    "chiedere", "giocare", "entrare", "uscire", "salire", "scendere", "finire", "aspettare",
    "aiutare", "cadere", "correre", "credere", "decidere", "diventare", "dimenticare", "divertirsi",
    "disegnare", "distruggere", "dividere", "dubitare", "educare", "eleggere", "eliminare", "emettere",
    "enfatizzare", "entrare", "esprimere", "estendere", "evitare", "fabbricare", "fallire", "far",
    "fermare", "fidarsi", "figurare", "firmare", "fissare", "fornire", "formare", "frequentare",
    "fumare", "funzionare", "gestire", "gettare", "girare", "godere", "governare", "garantire",
    "guidare", "illuminare", "immaginare", "imparare", "impedire", "importare", "includere", "incontrare",
    "indicare", "influenzare", "informare", "insegnare", "intendere", "interessare", "interpretare", "interrompere",
    "intervenire", "introdurre", "invitare", "lanciare", "lavare", "liberare", "limitare", "lottare",
    "mantenere", "meritare", "mescolare", "misurare", "modificare", "mordere", "muovere", "nascere",
    "nascondere", "notare", "nutrire", "obbligare", "ottenere", "occupare", "offrire", "operare",
    "organizzare", "orientare", "osservare", "partire", "partecipare", "perdere", "permettere", "piacere",
    "piangere", "praticare", "preferire", "preparare", "presentare", "premere", "prestare", "prevedere",
    "prevenire", "produrre", "programmare", "proibire", "promettere", "promuovere", "proporre", "proteggere",
    "provare", "pubblicare", "pulire", "punire", "raccogliere", "raggiungere", "reagire", "realizzare",
    "ricevere", "riconoscere", "ricordare", "registrare", "regolare", "relazionare", "rendere", "ripetere",
    "replicare", "rappresentare", "richiedere", "risolvere", "rispondere", "restare", "restituire", "ritirare",
    "rivedere", "rivelare", "rompere", "sacrificare", "salvare", "scaldare", "scegliere", "scoppiare",
    "scoprire", "scusare", "sedere", "seguire", "selezionare", "significare", "simboleggiare", "simulare",
    "smettere", "sognare", "sopportare", "sorprendere", "sostenere", "sottomettere", "sostituire", "succedere",
    "suggerire", "suonare", "superare", "sviluppare", "tagliare", "toccare", "tollerare", "tradurre",
    "trasferire", "trasformare", "trattare", "udire", "unire", "urlare", "usare", "utilizzare",
    "valere", "variare", "verificare", "vestire", "viaggiare", "vincere", "visitare", "votare",
    "abbattere", "abbinare", "abilitare", "abitare", "abolire", "abrogare", "accelerare", "accettare",
    "accompagnare", "accordare", "accumulare", "accusare", "acquistare", "addestrare", "addizionare",
    "adoperare", "adottare", "adorare", "affrontare", "afferrare", "affittare", "agevolare", "agganciare",
    "aggiustare", "allargare", "alloggiare", "allontanare", "alterare", "analizzare", "animare", "annunciare",
    "anticipare", "applicare", "appoggiare", "apprezzare", "approvare", "approfittare", "argomentare", "arredare",
    "arrestare", "articolare", "associare", "assicurare", "attaccare", "attivare", "attribuire", "aumentare",
    "autorizzare", "avanzare", "avvertire", "avviare", "avvolgere", "ballare", "basare", "battere",
    "beneficiare", "bloccare", "calcolare", "catturare", "celebrare", "circolare", "combinare", "commentare",
    "commettere", "comunicare", "concentrare", "concludere", "concordare", "condurre", "confermare", "confessare",
    "configurare", "congiungere", "conquistare", "considerare", "consigliare", "costruire", "consumare", "consultare",
    "contenere", "contribuire", "controllare", "convalidare", "convincere", "coprire", "correggere", "corrispondere",
    "creare", "crescere", "criticare", "curare", "danneggiare", "decorare", "definire", "delegare",
    "delimitare", "denunciare", "dipendere", "depositare", "derivare", "desiderare", "designare", "dettare",
    "difendere", "differenziare", "diffondere", "dirigere", "disporre", "distinguere", "distribuire", "documentare",
    "dominare", "donare", "elaborare", "elevare", "emanare", "emergere", "equipaggiare", "esercitare",
    "esistere", "escludere", "eseguire", "esporre", "evidenziare", "esaminare", "festeggiare", "fissare",
    "fondare", "formulare", "fronteggiare", "generare", "glorificare", "illustrare", "implementare", "implicare",
    "imporre", "migliorare", "incollare", "incrementare", "innalzare", "innovare", "inserire", "ispezionare",
    "ispirare", "istituire", "istruire", "interrogare", "inventare", "investigare", "iscrivere", "giudicare",
    "giustificare", "levare", "licenziare", "lodare", "localizzare", "manipolare", "marciare", "mascherare",
    "mediare", "memorizzare", "menzionare", "minacciare", "montare", "moltiplicare", "motivare", "navigare",
    "negare", "negoziare", "nominare", "notificare", "occuparsi", "omettere", "opporsi", "ospitare",
    "ottenere", "paragonare", "partorire", "percepire", "percorrere", "perfezionare", "persistere", "persuadere",
    "pesare", "pianificare", "piantare", "pilotare", "presidiare", "proiettare", "promuovere", "proporre",
    "proteggere", "provocare", "qualificare", "quantificare", "raccomandare", "radunare", "rafforzare", "rallentare",
    "rammaricarsi", "rapire", "rapportare", "ricercare", "reclamare", "recuperare", "registrare", "regolare",
    "relazionarsi", "rimuovere", "rinnovare", "restaurare", "riunire", "rivolgere", "ruotare", "saltare",
    "salutare", "sanzionare", "scandire", "scartare", "sconfiggere", "scorrere", "scuotere", "segnare",
    "seguitare", "seminare", "segnalare", "separare", "servire", "sfilare", "sfogliare", "smontare",
    "sollevare", "sottoscrivere", "sottolineare", "spazzare", "spegnere", "spingere", "sposare", "stampare",
    "stringere", "subire", "supplicare", "supportare", "suscitare", "svuotare", "tentare", "terminare",
    "testare", "tossire", "tracciare", "trasmettere", "trasportare", "uccidere", "utile", "valutare",
    "versare", "vibrare", "violaren", "vulcanizzare", "vuotare"
]

ENGLISH_WORDS = [
    "the", "be", "to", "of", "and", "a", "in", "that", "have", "I",
    "it", "for", "not", "on", "with", "he", "as", "you", "do", "at",
    "this", "but", "his", "by", "from", "they", "we", "say", "her", "she",
    "or", "an", "will", "my", "one", "all", "would", "there", "their", "what",
    "so", "up", "out", "if", "about", "who", "get", "which", "go", "me",
    "when", "make", "can", "like", "time", "no", "just", "him", "know", "take",
    "person", "into", "year", "your", "good", "some", "could", "them", "see", "other",
    "than", "then", "now", "look", "only", "come", "its", "over", "think", "also",
    "back", "after", "use", "two", "how", "our", "work", "first", "well", "way",
    "even", "new", "want", "because", "any", "these", "give", "day", "most", "us",
    "love", "through", "long", "where", "both", "feel", "much", "such", "high", "every",
    "big", "little", "though", "too", "many", "more", "find", "here", "down", "than",
    "may", "side", "own", "make", "should", "world", "last", "very", "often", "each",
    "same", "still", "tell", "must", "never", "did", "why", "let", "set", "run",
    "help", "put", "start", "show", "hear", "play", "read", "write", "move", "live",
    "believe", "bring", "happen", "next", "against", "below", "between", "face", "grow", "light",
    "open", "walk", "meet", "keep", "turn", "begin", "call", "head", "hold", "cut",
    "add", "change", "fall", "send", "speak", "talk", "try", "understand", "watch", "win",
    "ask", "buy", "build", "carry", "catch", "close", "come", "cover", "cross", "cut",
    "deal", "dream", "drive", "eat", "end", "enjoy", "enter", "escape", "explain", "fight",
    "fill", "finish", "follow", "forget", "get", "give", "go", "grow", "hang", "have",
    "hear", "help", "hide", "hit", "hold", "hope", "hurry", "imagine", "improve", "include",
    "increase", "indicate", "influence", "inform", "intend", "introduce", "join", "jump", "keep", "kill",
    "know", "laugh", "lead", "learn", "leave", "lend", "let", "lie", "lift", "like",
    "listen", "lose", "love", "manage", "mark", "marry", "mean", "measure", "meet", "mention",
    "mind", "miss", "move", "name", "need", "notice", "obtain", "offer", "open", "order",
    "organize", "owe", "own", "pass", "pay", "perform", "pick", "place", "plan", "play",
    "point", "prefer", "prepare", "present", "prevent", "produce", "promise", "protect", "prove", "provide",
    "pull", "push", "put", "reach", "read", "realize", "receive", "recognize", "reflect", "refuse",
    "regret", "remain", "remember", "remove", "repair", "repeat", "replace", "reply", "report", "represent",
    "require", "resist", "resolve", "respond", "rest", "return", "reveal", "rid", "ride", "ring",
    "rise", "roll", "run", "rush", "sail", "save", "say", "see", "seek", "seem",
    "sell", "send", "set", "shake", "share", "shine", "shoot", "shop", "show", "shut",
    "sing", "sit", "sleep", "slide", "slip", "smell", "smile", "smoke", "snow", "solve",
    "sound", "speak", "spend", "stand", "start", "state", "stay", "steal", "step", "stick",
    "stir", "stop", "store", "strike", "study", "succeed", "suggest", "suit", "supply", "support",
    "suppose", "surprise", "surround", "survive", "suspect", "swear", "sweep", "swell", "swim", "swing",
    "take", "talk", "teach", "tear", "tell", "think", "throw", "tie", "touch", "train",
    "travel", "treat", "try", "turn", "understand", "undo", "unfold", "unite", "unpack", "unzip",
    "use", "vanish", "vary", "view", "visit", "wait", "wake", "walk", "want", "warn",
    "wash", "waste", "watch", "wear", "weigh", "welcome", "win", "wish", "withdraw", "wonder",
    "worry", "wrap", "write", "yell", "yield", "zip", "zoom"
]


# --- Core Password Generation Logic ---
def generate_password(length, use_lowercase, use_uppercase, use_digits, use_symbols, custom_symbols_set, use_spaces, use_dictionary, dictionary_words):
    """
    This function constitutes the core logic for password generation. It processes all
    specified parameters (e.g., desired length, character types, dictionary mode)
    to construct a secure and random password conforming to the defined criteria.

    Parameters:
        length (int): The target length of the generated password.
        use_lowercase (bool): Flag to include lowercase letters.
        use_uppercase (bool): Flag to include uppercase letters.
        use_digits (bool): Flag to include digits.
        use_symbols (bool): Flag to include symbols.
        custom_symbols_set (str): Optional string of custom symbols to use.
        use_spaces (bool): Flag to include spaces.
        use_dictionary (bool): Flag to enable dictionary-based password generation (passphrase).
        dictionary_words (list): List of words to use in dictionary mode.

    Returns:
        str: The generated password or an error message if generation fails.
    """
    password_parts = [] # A list to accumulate characters and word segments.
    available_chars_for_random = [] # The pool of characters from which random fillers are drawn.
    guaranteed_chars = [] # Characters that must be present (e.g., at least one digit if requested).
    
    # Determines the set of symbols to be used.
    final_symbols_to_use = DEFAULT_SYMBOLS
    if use_symbols and custom_symbols_set:
        final_symbols_to_use = custom_symbols_set
    elif not use_symbols and custom_symbols_set:
        # Warns if custom symbols are provided but symbol inclusion is disabled.
        print("Warning: Custom symbols were provided, but symbol inclusion was disabled. Symbols will be excluded.", file=sys.stderr)
        use_symbols = False # Ensures symbols are not used.

    # --- Dictionary Mode Password Generation ---
    if use_dictionary:
        # Selects the word source: custom file words or internal default lists.
        all_words_for_dictionary = dictionary_words if dictionary_words else (ITALIAN_WORDS + ENGLISH_WORDS)
        if not all_words_for_dictionary:
            return "Error: No words available for dictionary password generation. Verify dictionary file or internal lists."

        # Validates that at least one letter case is enabled for dictionary mode.
        if not use_lowercase and not use_uppercase:
            return "Error: Dictionary mode inherently requires letters. Cannot exclude both lowercase and uppercase."

        # Calculates the minimum length required for non-word characters.
        min_non_word_chars_len = 0
        if use_digits: min_non_word_chars_len += 1
        if use_symbols: min_non_word_chars_len += 1
        if use_spaces: min_non_word_chars_len += 1

        # Determines the maximum allowable length for dictionary words, reserving space for other character types.
        max_word_length_allowed = length - min_non_word_chars_len
        if max_word_length_allowed < 1:
             return f"Error: Password length ({length}) is insufficient to accommodate dictionary words and required character types. Minimum for dictionary mode: {min_non_word_chars_len + 1}."

        chosen_words = []
        current_words_len = 0

        # Iteratively selects words, aiming for a total word length within the allowed limit
        # and a reasonable number of words (e.g., up to 5).
        attempts = 0
        while current_words_len < max_word_length_allowed * 0.8 and len(chosen_words) < 5 and attempts < 10:
            word_candidate = random.choice(all_words_for_dictionary)
            if current_words_len + len(word_candidate) <= max_word_length_allowed:
                chosen_words.append(word_candidate)
                current_words_len += len(word_candidate)
            attempts += 1
        
        # Ensures at least one word is included if possible.
        if not chosen_words and all_words_for_dictionary:
            word = random.choice(all_words_for_dictionary)
            if len(word) > max_word_length_allowed:
                 return f"Error: A single dictionary word '{word}' exceeds the desired password length ({length}) when accounting for other required characters."
            chosen_words.append(word)
            current_words_len += len(word)

        # Processes each chosen word, applying random casing to letters.
        for word in chosen_words:
            processed_word = ""
            for char in word:
                if char.isalpha():
                    if use_lowercase and use_uppercase:
                        processed_word += random.choice([char.lower(), char.upper()])
                    elif use_lowercase:
                        processed_word += char.lower()
                    elif use_uppercase:
                        processed_word += char.upper()
                else:
                    processed_word += char
            password_parts.append(processed_word)

        # Populates the general character pool and identifies characters that must be guaranteed.
        if use_digits:
            available_chars_for_random.extend(list(string.digits))
            guaranteed_chars.append(random.choice(string.digits))
        if use_symbols:
            available_chars_for_random.extend(list(final_symbols_to_use))
            guaranteed_chars.append(random.choice(list(final_symbols_to_use)))
        if use_spaces:
            available_chars_for_random.append(' ')
            guaranteed_chars.append(' ')
        
        if use_lowercase:
            available_chars_for_random.extend(list(string.ascii_lowercase))
        if use_uppercase:
            available_chars_for_random.extend(list(string.ascii_uppercase))

        # Distributes guaranteed characters among the password segments.
        temp_password_string_parts = []
        for i, part in enumerate(password_parts):
            temp_password_string_parts.append(part)
            if guaranteed_chars and i < len(password_parts) - 1:
                temp_password_string_parts.append(guaranteed_chars.pop(0))
        password_parts = temp_password_string_parts
        password_parts.extend(guaranteed_chars) # Appends any remaining guaranteed characters.

    else: # --- Standard Random Password Generation (Non-Dictionary Mode) ---
        # Populates the character pool and identifies characters that must be guaranteed.
        if use_lowercase:
            available_chars_for_random.extend(list(string.ascii_lowercase))
            guaranteed_chars.append(random.choice(string.ascii_lowercase))
        if use_uppercase:
            available_chars_for_random.extend(list(string.ascii_uppercase))
            guaranteed_chars.append(random.choice(string.ascii_uppercase))
        if use_digits:
            available_chars_for_random.extend(list(string.digits))
            guaranteed_chars.append(random.choice(string.digits))
        if use_symbols:
            available_chars_for_random.extend(list(final_symbols_to_use))
            guaranteed_chars.append(random.choice(list(final_symbols_to_use)))
        if use_spaces:
            available_chars_for_random.append(' ')
            guaranteed_chars.append(' ')
        
        # Initializes password parts with guaranteed characters.
        password_parts.extend(guaranteed_chars)

    # --- Final Password Assembly and Validation ---
    if not available_chars_for_random:
        return "Error: No character types selected. Cannot generate password."
    
    # Calculates the current length of the assembled password components.
    current_length_so_far = sum(len(part) for part in password_parts)

    # Fills the remaining length of the password with random characters.
    remaining_slots = length - current_length_so_far
    
    if remaining_slots > 0:
        for _ in range(remaining_slots):
            password_parts.append(random.choice(available_chars_for_random))

    # Shuffles the entire list of password components to ensure high randomness and prevent patterns.
    random.shuffle(password_parts)

    # Joins all components into a single string and truncates it to the exact desired length.
    final_password = ''.join(password_parts)[:length]
    return final_password


# --- Main Program Execution Block ---
def main():
    """
    This is the entry point of the script, executed when the program is run from the command line.
    It parses command-line arguments, configures password generation parameters based on user input,
    invokes the password generation function, and prints the resulting password.
    """
    # Initializes the argument parser with a description of the script's purpose.
    parser = argparse.ArgumentParser(
        description="Generate a secure, random password.",
        formatter_class=argparse.RawTextHelpFormatter # Ensures proper formatting of help messages.
    )

    # --- Definition of Command-Line Arguments ---

    # -l or --length: Specifies the desired password length.
    parser.add_argument(
        "-l", "--length",
        type=int, # Expects an integer value.
        default=16, # Default length if not specified.
        help="The desired length of the password (default: 16). For dictionary mode, this is a minimum target."
    )
    # --no-lowercase: Excludes lowercase letters.
    parser.add_argument(
        "--no-lowercase",
        action="store_true", # Flag that becomes True if present.
        help="Exclude lowercase letters (a-z) from the password."
    )
    # --no-uppercase: Excludes uppercase letters.
    parser.add_argument(
        "--no-uppercase",
        action="store_true",
        help="Exclude uppercase letters (A-Z) from the password."
    )
    # --no-digits: Excludes digits.
    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Exclude digits (0-9) from the password."
    )
    # --no-symbols: Excludes common symbols.
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Exclude common symbols (!@#$%^&*()_+-=[]{}|;:,.<>?) from the password."
    )
    # --custom-symbols: Specifies a custom set of symbols.
    parser.add_argument(
        "--custom-symbols",
        type=str, # Expects a string value.
        help="Provide a custom set of symbols (e.g., '#@$!') to use instead of default symbols. \n(Cannot be used in conjunction with --no-symbols.)"
    )
    # --include-spaces: Includes spaces.
    parser.add_argument(
        "--include-spaces",
        action="store_true",
        help="Include spaces in the password (disabled by default for broader compatibility)."
    )
    # --dictionary: Enables dictionary-based password generation (passphrase).
    parser.add_argument(
        "--dictionary",
        action="store_true",
        help="Constructs the password using dictionary words, optionally mixed with numbers/symbols. \n(This mode can yield longer, more memorable passwords.)"
    )
    # --dictionary-file: Specifies a custom dictionary file.
    parser.add_argument(
        "--dictionary-file",
        type=str, # Expects a file path string.
        help="Path to a custom dictionary file (words within should be comma-separated). \n(Requires the --dictionary flag to be active.)"
    )

    # Parses the command-line arguments provided by the user.
    args = parser.parse_args()

    # --- Argument Processing and Validation ---
    
    # Handles potential conflicts between --custom-symbols and --no-symbols.
    final_custom_symbols = None
    if args.custom_symbols:
        if args.no_symbols:
            print("Error: Conflicting arguments detected. Cannot specify --custom-symbols while simultaneously excluding all symbols with --no-symbols. Please choose one option.", file=sys.stderr)
            sys.exit(1) # Terminates execution.
        final_custom_symbols = args.custom_symbols

    # Attempts to load words from a custom dictionary file if specified.
    dict_words_for_use = []
    if args.dictionary_file:
        if not args.dictionary:
            print("Error: The --dictionary-file argument requires the --dictionary flag to be enabled.", file=sys.stderr)
            sys.exit(1)
        dict_words_for_use = load_words_from_file(args.dictionary_file)
        if not dict_words_for_use: # If loading fails or no words are found.
            print("Warning: Issue encountered with the custom dictionary file. Falling back to internal dictionary words.", file=sys.stderr)
    
    # Determines the final character type settings, with special consideration for dictionary mode.
    if args.dictionary:
        # In dictionary mode, letters are fundamental. Disabling both cases is an invalid configuration.
        if args.no_lowercase and args.no_uppercase:
            print("Error: When operating in --dictionary mode, words inherently contain letters. Excluding both lowercase and uppercase letters is not permissible.", file=sys.stderr)
            sys.exit(1)
        use_lowercase = not args.no_lowercase
        use_uppercase = not args.no_uppercase
    else:
        use_lowercase = not args.no_lowercase
        use_uppercase = not args.no_uppercase

    # Assigns boolean flags based on command-line arguments.
    use_digits = not args.no_digits
    use_symbols = not args.no_symbols
    use_spaces = args.include_spaces
    use_dictionary = args.dictionary

    # Validates the specified password length.
    if args.length <= 0:
        print("Error: Password length must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    # Invokes the password generation function with the determined parameters.
    password = generate_password(
        args.length,
        use_lowercase,
        use_uppercase,
        use_digits,
        use_symbols,
        final_custom_symbols,
        use_spaces,
        use_dictionary,
        dict_words_for_use
    )

    # Displays the generated password to the user.
    print(f"Generated Password: {password}")

# Ensures that the 'main()' function is executed only when the script is run directly.
if __name__ == "__main__":
    main()
