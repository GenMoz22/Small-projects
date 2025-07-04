La scansione delle porte è una tecnica utilizzata per determinare quali porte sono "aperte" (cioè, in ascolto di connessioni) su un host di rete. È uno strumento fondamentale nella network security.

### Come Funziona
Ogni servizio di rete (come un server web, un server FTP, un server SSH) è in ascolto su una porta specifica. Quando un client vuole comunicare con quel servizio, tenta di connettersi a quella porta sull'indirizzo IP del server.

Lo script implementa un tipo di scansione chiamato **"TCP Connect Scan"**:
1.  **Tentativo di Connessione:** Il programma tenta di stabilire una connessione TCP completa (`SYN`, `SYN-ACK`, `ACK`) a una porta specifica sul target.
2.  **Risposta del Target:**
    * Se la porta è **aperta**, il target risponde con un `SYN-ACK` e lo script completa il handshake con un `ACK`. Questo indica che un servizio è in ascolto su quella porta.
    * Se la porta è **chiusa**, il target risponde con un pacchetto `RST` (Reset), indicando che non c'è nessun servizio in ascolto e la connessione è stata rifiutata.
    * Se non c'è **alcuna risposta** (o un timeout), la porta potrebbe essere filtrata da un firewall, o l'host non è raggiungibile.

### Identificazione dei Servizi
Le porte sono categorizzate in base al loro utilizzo. Lo script include una mappatura per le **porte ben note** (generalmente da 0 a 1023) che sono assegnate a servizi di rete standard (es. porta 80 per HTTP, porta 22 per SSH) e alcune **porte registrate** (generalmente da 1024 a 49151) spesso utilizzate da applicazioni specifiche (es. porta 3306 per MySQL, porta 3389 per RDP). Questa mappatura aiuta a identificare il tipo di servizio potenzialmente in ascolto sulla porta aperta.





