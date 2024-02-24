#!/bin/bash

CSV_FILE="data/olx_links.csv"

check_csv_status() {
    while IFS=, read -r url qtd status; do
        if [ "$status" != "finished" ]; then
            return 0  
        fi
    done < "$CSV_FILE"
    return 1  
}

start_time=$(date +%s)

if [ ! -e "$CSV_FILE" ] || ([ -e "$CSV_FILE" ] && ! check_csv_status) || ([ -e "$CSV_FILE" ] && [ ! -s "$CSV_FILE" ]); then
    echo -n > data/olx_links.csv
    echo -n > unfiltered_links.txt
    echo -n > data/scraping_start_date.txt

    python3 scrape_regions.py
    python3 scrape_links.py

    date=$(TZ="GMT-3" date +'%Y-%m-%d')
    echo $date > data/scraping_start_date.txt
fi

while true; do
    if ([ -e "$CSV_FILE" ] && check_csv_status); then
        python3 property_scraper.py
    else
        echo "All rows have status 'finished'. No action required."
        break
    fi
    sleep 600
done

end_time=$(date +%s)
elapsed_time_minutes=$(echo "scale=2; ($end_time - $start_time) / 60" | bc)

echo "Elapsed time: $elapsed_time minutes"