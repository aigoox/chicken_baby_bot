FROM python:3.10-slim
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 80
CMD ["python3", "main.py"]