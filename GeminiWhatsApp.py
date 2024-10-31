from twilio.rest import Client
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
USER_WHATSAPP_TO = os.getenv("USER_WHATSAPP_TO")

genai.configure(api_key=API_KEY)

def fetch_logs():
    """Read and return the contents of the stress test log file."""
    try:
        with open('stressTestLogs.log', 'r') as file:
            logs = file.read()
        return logs
    except Exception as e:
        error_message = f"Failed to read logs: {e}"
        print(error_message)
        send_whatsapp_message("Error: Unable to read the logs for analysis.")
        return None

def send_logs_to_api(logs):
    try:
        model = genai.GenerativeModel("gemini-1.0-pro")
        response = model.generate_content(
            f"Provide suggestions to counter the problems/errors based on these logs:\n{logs} in strictly less than 1500 characters in response"
        )
        print("AI Response:", response.text)
        return response.text
    except Exception as e:
        error_message = f"Failed to generate analysis: {e}"
        print(error_message)
        send_whatsapp_message("Error: Unable to generate analysis from the logs.")
        return None

def send_whatsapp_message(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
        sent_message = client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_FROM,
            to=USER_WHATSAPP_TO
        )
        print("WhatsApp message sent with SID:", sent_message.sid)
        return sent_message.sid
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
        return None

def main():
    logs = fetch_logs()
    if logs is None:
        return

    analysis_result = send_logs_to_api(logs)
    if analysis_result:
        send_whatsapp_message(analysis_result)
    else:
        send_whatsapp_message("Error: Analysis could not be completed due to an internal issue.")

if __name__ == "__main__":
    main()
