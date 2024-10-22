FROM ubuntu:20.04

RUN apt-get update && apt-get install -y \
    opensc \
    openssl \
    libengine-pkcs11-openssl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]