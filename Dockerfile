FROM python:3.11

VOLUME /telegram.json
VOLUME /Media

COPY Anthony_Fantanbot.py .
COPY requirements.txt .
COPY Objects/. ./Objects/
COPY Services/. ./Services/
COPY Utilities/. ./Utilities/

RUN pip install -r requirements.txt
CMD ["python", "./Anthony_Fantanbot.py"]