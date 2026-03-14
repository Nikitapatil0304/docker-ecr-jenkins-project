FROM python:3.9-slim

WORKDIR /app

# Copy the app directory only if it exists
COPY app/ /app/

# Upgrade pip and install Flask
RUN pip install --upgrade pip && pip install flask

EXPOSE 5000

CMD ["python", "app.py"]
