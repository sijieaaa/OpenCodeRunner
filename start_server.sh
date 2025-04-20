

# Ensure OEPNCODERUNNER_HOME is set
if [ -z "$OEPNCODERUNNER_HOME" ]; then
    echo "❌ OEPNCODERUNNER_HOME is not set. Please source ~/.bashrc or set it manually."
    exit 1
fi

cd "$OEPNCODERUNNER_HOME" || {
    echo "❌ Failed to cd into \$OEPNCODERUNNER_HOME: $OEPNCODERUNNER_HOME"
    exit 1
}

# Command to run the server
CMD="uvicorn opencoderunner.server:app"

echo "🔍 Starting OpenCodeRunner server..."
if command -v firejail >/dev/null 2>&1; then
    echo "✅ firejail found. Launching with sandbox..."
    exec firejail -- $CMD
else
    echo "⚠️ firejail not found. Running without sandbox..."
    exec $CMD
fi
