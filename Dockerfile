FROM python:3.11.7-slim

# Cài đặt libmagic và các phụ thuộc
RUN apt-get update && apt-get install -y libmagic1

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

# CMD để chạy ứng dụng khi container được khởi chạy
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
