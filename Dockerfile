FROM python:3.11-slim

# Set working directory
WORKDIR /app

ENV \
# Prevent Python from writing bytecode files (.pyc) to disk
PYTHONDONTWRITEBYTECODE=1 \
# Prevent Python from buffering stdout and stderr
PYTHONUNBUFFERED=1

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY cross_encoder_service.py .
COPY start.sh .
RUN chmod +x start.sh

# Expose port for the application
ENV PORT=8000 LOG_LEVEL=info
EXPOSE $PORT

# Run entrypoint shell script to support env vars
ENTRYPOINT ["./start.sh"]