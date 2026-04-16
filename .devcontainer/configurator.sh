#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "${SCRIPT_DIR}/utility.sh"

CONFIG_FILE="/config"
CONTENT_FILE="${SCRIPT_DIR}/dev_conf.yaml"
TASK_COMMAND="python -m homeassistant --config $CONFIG_FILE"
FLAG=0

log_status "progress" "Starting configuration file modification..."

if [ ! -f "$CONTENT_FILE" ]; then
    log_status "error" "Content file not found at $CONTENT_FILE"
    exit 1
fi

if [ ! -f "$CONFIG_FILE" ]; then
    log_status "info" "$CONFIG_FILE not found, starting Home Assistant..."
    $TASK_COMMAND &
    TASK_PID=$!
    FLAG=1

    while [ ! -f "$CONFIG_FILE" ]; do
        sleep 1
    done
fi

if ! grep -q "^default_config:" "$CONFIG_FILE"; then
    log_status "error" "'default_config:' line not found"
    exit 1
fi

log_status "progress" "Backing up configuration file..."
cp "$CONFIG_FILE" "${CONFIG_FILE}.backup"

INSERT_LINE=$(($(grep -n "^default_config:" "$CONFIG_FILE" | cut -d: -f1) + 2))
temp_file=$(mktemp)

head -n $INSERT_LINE "$CONFIG_FILE" > "$temp_file"
cat "$CONTENT_FILE" >> "$temp_file"
tail -n +$((INSERT_LINE + 1)) "$CONFIG_FILE" >> "$temp_file"
mv "$temp_file" "$CONFIG_FILE"

log_status "success" "Configuration updated successfully"

if [ $FLAG -eq 1 ]; then
    log_status "info" "Stopping Home Assistant task..."
    kill $TASK_PID
fi
