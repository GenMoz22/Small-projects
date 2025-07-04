import socket
import sys
from datetime import datetime

# --- Function to Get Local IP Address ---
def get_local_ip():
    """
    This function tries to figure out your computer's local IP address.
    It does this by making a temporary, silent "connection" to a public internet server (like Google's DNS).
    This trick helps your computer choose which network interface to use, and then we just read its IP.
    If it can't find your local IP (e.g., no internet connection), it will use '127.0.0.1' (localhost).
    """
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # We don't actually send data, just use this to find our local IP
        s.connect(("8.8.8.8", 80)) # Google DNS server
        IP = s.getsockname()[0]
    except socket.error:
        IP = "127.0.0.1" # Fallback to localhost if we can't get the network IP
    finally:
        if s:
            s.close()
    return IP

# --- Configuration Section ---
# This is where you can tell the script what to scan.

# By default, the script will scan your own computer's local IP address.
# This is usually a safe way to test it out.
TARGET_HOST = get_local_ip()

# If you want to scan a different computer, uncomment the line below and change the IP address or hostname.
# Remember: Only scan computers you own or have explicit permission to scan!
# TARGET_HOST = "192.168.1.1" # Example: your home router
# TARGET_HOST = "example.com" # Example: a website (if you have permission)

# These are the specific network ports that the script will check.
# Each port is commonly used by a specific service or application.
PORTS_TO_SCAN = [
    20,  # FTP-DATA (File Transfer Protocol Data)
    21,  # FTP (File Transfer Protocol)
    22,  # SSH (Secure Shell)
    23,  # Telnet
    25,  # SMTP (Simple Mail Transfer Protocol)
    53,  # DNS (Domain Name System)
    69,  # TFTP (Trivial File Transfer Protocol)
    80,  # HTTP (Hypertext Transfer Protocol - standard web)
    110, # POP3 (Post Office Protocol version 3 - for email)
    143, # IMAP (Internet Message Access Protocol - for email)
    161, # SNMP (Simple Network Management Protocol - for network device management)
    443, # HTTPS (Hypertext Transfer Protocol Secure - secure web)
    3306, # MySQL (Commonly used for MySQL database communication)
    8080, # HTTP Proxy / Web Server (alternative port for web services)
    3389  # RDP (Remote Desktop Protocol - for remote desktop access)
]

# This dictionary helps the script give you a readable name for each port.
# If a port is open, it tells you what service usually runs on it.
COMMON_SERVICES = {
    20: "FTP-DATA (File Transfer Protocol Data)",
    21: "FTP (File Transfer Protocol)",
    22: "SSH (Secure Shell)",
    23: "Telnet",
    25: "SMTP (Simple Mail Transfer Protocol)",
    53: "DNS (Domain Name System)",
    69: "TFTP (Trivial File Transfer Protocol)",
    80: "HTTP (Hypertext Transfer Protocol)",
    110: "POP3 (Post Office Protocol version 3)",
    143: "IMAP (Internet Message Access Protocol)",
    161: "SNMP (Simple Network Management Protocol)",
    443: "HTTPS (Hypertext Transfer Protocol Secure)",
    3306: "MySQL Database Communication",
    8080: "HTTP Proxy / Web Server (alternative)",
    3389: "RDP (Remote Desktop Protocol)"
}

# --- Port Scanning Logic ---
def scan_port(host, port):
    """
    This function checks if a single network "door" (port) is open on a specific computer (host).
    It tries to connect to the port.
    If the connection is successful, it means the port is "open" and a service is likely listening there.
    """
    try:
        # Create a special connection object (socket) to try and connect
        # It's like dialing a phone number for a specific service.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Wait for only 1 second before giving up on a connection attempt

        # Try to connect to the port on the target computer
        result = s.connect_ex((host, port))

        # If 'result' is 0, it means the connection was successful, so the port is open!
        if result == 0:
            # Look up the common service name for this open port
            service = COMMON_SERVICES.get(port, "Unknown Service")
            print(f"Port {port} is OPEN: {service}")
        s.close() # Always close the connection attempt, whether it was open or not
    except socket.gaierror:
        # This error means the computer name or IP address you gave wasn't recognized.
        print(f"Error: Couldn't resolve hostname for {host}. Please check the address.")
        sys.exit() # Stop the script if the host can't be found
    except socket.error as e:
        # This catches other general connection errors.
        # We only print them if they're not a common "Connection refused" error on localhost,
        # which just means the port is closed.
        if host != "127.0.0.1" or "Connection refused" not in str(e):
             print(f"Connection Error on port {port} on {host}: {e}")

# --- Main Program Execution ---
def main():
    """
    This is the main part of the script that runs everything.
    It prepares the scan, then goes through each specified port and checks its status.
    """
    print("-" * 50)
    print(f"Starting port scan on: {TARGET_HOST}")
    print(f"Scan started at: {datetime.now()}")
    print("-" * 50)

    try:
        # Get the actual numerical IP address from the hostname (if one was provided)
        target_ip = socket.gethostbyname(TARGET_HOST)
    except socket.gaierror:
        print(f"Error: Cannot resolve the target host '{TARGET_HOST}'. Please check the name or IP address.")
        sys.exit(1) # Exit if the target host isn't valid

    # Loop through each port in our list and scan it
    for port in PORTS_TO_SCAN:
        scan_port(target_ip, port)

    print("-" * 50)
    print("Port scan completed.")
    print("-" * 50)

# This line makes sure that the 'main()' function runs when you execute the script.
if __name__ == "__main__":
    main()
