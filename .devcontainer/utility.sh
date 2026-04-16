#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_status() {
    local status=$1
    local message=$2
    case $status in
        "info")
            echo -e "${BLUE}[INFO] $message${NC}"
            ;;
        "progress")
            echo -e "${YELLOW}[PROGRESS] $message${NC}"
            ;;
        "success")
            echo -e "${GREEN}[SUCCESS] $message${NC}"
            ;;
        "error")
            echo -e "${RED}[ERROR] $message${NC}"
            ;;
    esac
}
