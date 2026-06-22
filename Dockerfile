FROM python:3.12-slim

LABEL maintainer="arkanzasfeziii"
LABEL description="SecurityQuestAcademy — 700 cybersecurity challenges"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY securityquest/ securityquest/
COPY games/ games/
COPY standalone/ standalone/
COPY main.py .

ENTRYPOINT ["python", "-m", "securityquest"]
