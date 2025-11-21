#!/bin/bash
APP_DIR="/home/sahil/travel-website"
VENV="$APP_DIR/venv"
MANAGE="$APP_DIR/manage.py"
HOST="0.0.0.0"
PORT="8000"
SESSION="travel-app"
LOG="$APP_DIR/server.log"

tmux has-session -t $SESSION 2>/dev/null
if [ $? -eq 0 ]; then
  echo "tmux session $SESSION already running"
  exit 0
fi

tmux new -d -s $SESSION "cd $APP_DIR && $VENV/bin/python $MANAGE runserver $HOST:$PORT > $LOG 2>&1"
echo "Started tmux session: $SESSION (logging to $LOG)"
