FROM python:3.13.3-slim

WORKDIR /app

COPY . .

# Install dependencies with no cache
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8888

# Command to run the application
CMD ["python", "main.py"]
