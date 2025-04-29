#!/bin/bash

# Set default values for environment variables if not provided
: "${PORT:=8000}"
: "${LOG_LEVEL:=info}"
: "${WORKERS:=1}"

echo "Starting FastAPI application with:"
echo "- Port: $PORT"
echo "- Log level: $LOG_LEVEL"
echo "- Workers: $WORKERS"

# Execute uvicorn with proper environment variables
# exec replaces the shell process with uvicorn, making it PID 1
# This allows proper signal handling (e.g., SIGTERM for graceful shutdown)
exec uvicorn cross_encoder_service:app \
    --host 0.0.0.0 \
    --port "$PORT" \
    --workers "$WORKERS" \
    --log-level "$LOG_LEVEL"
