# MajorProjectC400
Setting Up Your Environment

In A Different VM(Remote VM) with MySQL Server
1. MySQL Database Configuration:
Create a MySQL User:
CREATE USER 'remote'@'%' IDENTIFIED BY 'YourStrongPassword';

Replace YourStrongPassword with a strong, unique password.
Grant Privileges with command:
GRANT ALL PRIVILEGES ON stressTest.* TO 'remote'@'%';
FLUSH PRIVILEGES;

Create a Database with command:
CREATE DATABASE stressTest;
GRANT ALL PRIVILEGES ON stressTest.* TO 'remote'@'%';
FLUSH PRIVILEGES;


2. API Key and Token Setup:

Generate API Keys:
Gemini API Key: Obtain a new API key from the Gemini API platform.
Twilio Account SID and Auth Token: Create a Twilio account and retrieve your Account SID and Auth Token.

In VM in which you are intending to run the python file
3. Environment Variable Configuration:
Create a .env File: Create a .env file in the same directory as your Python script.
Add Sensitive Information: Add the following lines to the .env file, replacing the placeholders with your actual credentials:
sqlpass=YourSQLDBPassword
TWILIO_ACCOUNT_SID=YourTwilioAccountSID
TWILIO_AUTH_TOKEN=YourTwilioAuthToken
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
USER_WHATSAPP_TO=whatsapp:CountryCodeYourWhatsAppNumber
API_KEY=YourGeminiAPIKey/Token

4. Don't forget to update your SQL database details in the stressTest.py file as well. 

Important: Ensure that the .env file is not committed to your version control system to protect your sensitive information.
Running the Application


Execute the Script with the command:
python stressTest.py
python GeminiWhatsApp.py


Security Considerations:
Strong Passwords: Use strong, unique passwords for your database and API keys.
Environment Variables: Always use environment variables to store sensitive information.
Secure API Key Storage: Protect your API keys and tokens. Consider using a secrets management tool.
By following these steps and prioritizing security, you can effectively set up and run your Python application.
