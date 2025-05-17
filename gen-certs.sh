#!/bin/bash

APP_NAME="MASS"
CERT_DIR="./nginx/certs"
CA_KEY="$CERT_DIR/rootCA.key"
CA_CERT="$CERT_DIR/rootCA.pem"
DAYS_VALID=825

mkdir -p "$CERT_DIR"

green="\033[0;32m"
red="\033[0;31m"
reset="\033[0m"

generate_root_ca() {
    echo -e "${green}[+] Generating root CA...${reset}"
    openssl genrsa -out "$CA_KEY" 4096
    openssl req -x509 -new -nodes -key "$CA_KEY" -sha256 -days 3650 \
        -out "$CA_CERT" \
        -subj "/L=PR/O=$APP_NAME/OU=$APP_NAME"
}

issue_cert() {
    local name="$1"
    local key="$CERT_DIR/${name}.key"
    local csr="$CERT_DIR/${name}.csr"
    local cert="$CERT_DIR/${name}.pem"

    echo -e "${green}[+] Issuing cert for $name...${reset}"
    openssl genrsa -out "$key" 2048

    openssl req -new -key "$key" -out "$csr" \
        -subj "/C=US/ST=PR/O=$APP_NAME/OU=$APP_NAME/CN=$name"

    openssl x509 -req -in "$csr" -CA "$CA_CERT" -CAkey "$CA_KEY" -CAcreateserial \
        -out "$cert" -days "$DAYS_VALID" -sha256

    rm "$csr"
}


if [ ! -f "$CA_CERT" ] || [ ! -f "$CA_KEY" ]; then
    generate_root_ca
else
    echo -e "${green}[+] Root CA already exists.${reset}"
fi

issue_cert "mass-server"
