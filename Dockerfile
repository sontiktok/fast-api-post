FROM python:3.11.7-slim

RUN apt-get update && apt-get install -y libmagic1

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt


EXPOSE 8000

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
