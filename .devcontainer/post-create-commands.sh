#!/bin/bash
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
WORKSPACE_ROOT="${SCRIPT_DIR}/.."

source "${SCRIPT_DIR}/utility.sh"

# ------------------------
# 1️⃣ Upgrade pip
# ------------------------
log_status "progress" "Upgrading pip..."
python -m pip install --upgrade pip

# ------------------------
# 2️⃣ Install runtime dependencies
# ------------------------
REQ_FILE="${WORKSPACE_ROOT}/requirements.txt"
if [ -f "$REQ_FILE" ]; then
    log_status "progress" "Installing runtime dependencies from requirements.txt..."
    python -m pip install -r "$REQ_FILE"
else
    log_status "error" "requirements.txt not found"
fi

# ------------------------
# 3️⃣ Install dev/test dependencies
# ------------------------
REQ_TEST_FILE="${WORKSPACE_ROOT}/requirements_test.txt"
if [ -f "$REQ_TEST_FILE" ]; then
    log_status "progress" "Installing dev/test dependencies..."
    python -m pip install -r "$REQ_TEST_FILE"
else
    log_status "info" "No test requirements file found, skipping"
fi

# ------------------------
# 4️⃣ Home Assistant config directory
# ------------------------
HA_CONFIG_DIR="/config"
if [ ! -d "$HA_CONFIG_DIR" ]; then
    log_status "progress" "Creating Home Assistant configuration directory..."
    mkdir -p "$HA_CONFIG_DIR"
fi

# ------------------------
# 5️⃣ Download go2rtc
# ------------------------
GO2RTC_BIN="/usr/local/bin/go2rtc"

if [ ! -f "$GO2RTC_BIN" ]; then
    log_status "progress" "Downloading go2rtc binary..."

    # Detect architecture
    ARCH="$(uname -m)"
    OS="$(uname -s | tr '[:upper:]' '[:lower:]')"

    case "$ARCH" in
        x86_64) ARCH="amd64" ;;
        aarch64 | arm64) ARCH="arm64" ;;
        *) log_status "error" "Unsupported architecture: $ARCH" ;;
    esac

    # URL for latest release (plain binary)
    GO2RTC_URL="https://github.com/AlexxIT/go2rtc/releases/latest/download/go2rtc_${OS}_${ARCH}"
    TMP_FILE="/tmp/go2rtc"

    echo "Downloading go2rtc for $ARCH..."
    curl -sL -o "$TMP_FILE" "$GO2RTC_URL" || { echo "Download failed"; exit 1; }

    # Make executable
    chmod +x "$TMP_FILE"

    # Move to /usr/local/bin (needs sudo)
    sudo mv "$TMP_FILE" "$GO2RTC_BIN"
    # Validate command
    if command -v go2rtc >/dev/null 2>&1; then
        log_status "success" "go2rtc installed at $GO2RTC_BIN and available in PATH"
    else
        log_status "progress" "go2rtc installation failed"
        exit 1
    fi
else
    log_status "info" "go2rtc already exists at $GO2RTC_BIN, skipping download"
fi


log_status "success" "Devcontainer setup complete. Ready for development!"
