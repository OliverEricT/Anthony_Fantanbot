FROM python:3.11
COPY . .
RUN pip install #dependencies
CMD ["python", "./Anthony_Fantanbot.py"]