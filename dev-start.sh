#!/bin/bash
# dev-start.sh - start Django dev server in a tmux session
APP_DIR="/home/sahil/travel-website"
VENV="$APP_DIR/venv"
MANAGE="$APP_DIR/manage.py"
HOST="0.0.0.0"
PORT="8000"
SESSION="travel-app"

# Activate venv and start server in detached tmux session
# If session exists, just print a message
tmux has-session -t $SESSION 2>/dev/null
if [ $? -eq 0 ]; then
  echo "tmux session $SESSION already running"
  exit 0
fi

# start the session with the server command
tmux new -d -s $SESSION "cd $APP_DIR && $VENV/bin/python $MANAGE runserver $HOST:$PORT"
echo "Started tmux session: $SESSION"
