FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt readme.txt /app
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY stressTest.py GeminiWhatsApp.py /app
EXPOSE 9104 9100
CMD echo "Read readme.txt first!";

