FROM python:3.10.12

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x verify_on_startup.sh

ENTRYPOINT ["/bin/bash","/app/scraper/verify_on_startup.sh"]
