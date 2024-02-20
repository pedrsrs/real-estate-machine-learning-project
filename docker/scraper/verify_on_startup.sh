#!/bin/bash

CSV_FILE="olx_links.csv"

check_csv_status() {
    while IFS=, read -r url qtd status; do
        if [ "$status" != "finished" ]; then
            return 0  
        fi
    done < "$CSV_FILE"
    return 1  
}

if ([ -e "$CSV_FILE" ] && check_csv_status); then
        ./start_process.sh
    fi
