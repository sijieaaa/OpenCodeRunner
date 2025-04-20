#!/bin/bash

# Ensure OEPNCODERUNNER_HOME is set
if [ -z "$OEPNCODERUNNER_HOME" ]; then
    echo "❌ OEPNCODERUNNER_HOME is not set. Please source ~/.bashrc or set it manually."
    exit 1
fi

cd "$OEPNCODERUNNER_HOME" || {
    echo "❌ Failed to cd into \$OEPNCODERUNNER_HOME: $OEPNCODERUNNER_HOME"
    exit 1
}

# Default values
HOST="0.0.0.0"
PORT="8000"
RELOAD=true

# Parse CLI arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --host)
            HOST="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --reload)
            RELOAD=true
            shift
            ;;
        *)
            echo "⚠️ Unknown argument: $1"
            shift
            ;;
    esac
done

# Build the uvicorn command
CMD="uvicorn opencoderunner.server:app --host $HOST --port $PORT"
if [ "$RELOAD" = true ]; then
    CMD="$CMD --reload"
fi

echo "🔍 Starting OpenCodeRunner server on $HOST:$PORT..."
if [ "$RELOAD" = true ]; then
    echo "🌀 Reload mode enabled"
fi

# Check if firejail exists
if command -v firejail >/dev/null 2>&1; then
    echo "✅ firejail found. Launching with sandbox..."
    exec firejail -- $CMD
else
    echo "⚠️ firejail not found. Running without sandbox..."
    exec $CMD
fi
