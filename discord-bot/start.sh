#!/usr/bin/env bash
set -euo pipefail

BOT_DIR="$(cd "$(dirname "$0")" && pwd)"
PID_FILE="$BOT_DIR/.bot.pid"
LOG_FILE="$BOT_DIR/bot.log"

is_running() {
    [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

start() {
    if is_running; then
        echo "Bot 已在運行 (PID: $(cat "$PID_FILE"))"
        return 0
    fi
    echo "啟動 Discord Bot..."
    cd "$BOT_DIR"
    nohup uv run python bot.py >> "$LOG_FILE" 2>&1 &
    echo $! > "$PID_FILE"
    echo "Bot 已啟動 (PID: $!)"
    echo "日誌: $LOG_FILE"
}

stop() {
    if ! is_running; then
        echo "Bot 未在運行"
        rm -f "$PID_FILE"
        return 0
    fi
    local pid
    pid=$(cat "$PID_FILE")
    echo "停止 Bot (PID: $pid)..."
    kill "$pid"
    rm -f "$PID_FILE"
    echo "Bot 已停止"
}

status() {
    if is_running; then
        echo "Bot 運行中 (PID: $(cat "$PID_FILE"))"
    else
        echo "Bot 未在運行"
        rm -f "$PID_FILE"
    fi
}

logs() {
    tail -f "$LOG_FILE"
}

case "${1:-start}" in
    start)  start  ;;
    stop)   stop   ;;
    restart) stop; start ;;
    status) status ;;
    logs)   logs   ;;
    *)
        echo "用法: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
