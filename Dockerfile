FROM lunacircle4/python:3.8.1

WORKDIR /app

RUN apt update \
    && apt install -y postgresql postgresql-contrib libpq-dev supervisor zlib1g-dev libjpeg-dev \         
    && rm -rf /var/lib/apt/lists/* 

COPY requirements.txt ./
RUN pip3 -v --no-cache-dir install -r requirements.txt && rm -rf requirements.txt

ENTRYPOINT ["sh", "./service.sh"]
