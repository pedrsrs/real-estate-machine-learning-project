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

start_time=$(date +%s)

#echo -n > olx_links.csv
echo -n > unfiltered_links.txt

python3 regions.py
python3 link_scraper.py

while true; do
    if check_csv_status; then
        python3 property_scraper.py
    else
        echo "All rows have status 'finished'. No action required."
        break
    fi
    sleep 
done

end_time=$(date +%s)
elapsed_time_minutes=$(echo "scale=2; ($end_time - $start_time) / 60" | bc)

echo "Elapsed time: $elapsed_time minutes"