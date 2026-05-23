#!/bin/bash
set -e

# Instalar Docker
apt-get update -y
apt-get install -y docker.io
systemctl enable docker
systemctl start docker

# Escribir kong.yml con las IPs reales de los servicios
mkdir -p /etc/kong

cat > /etc/kong/kong.yml <<'KONG'
_format_version: "3.0"
_transform: true

services:
  - name: svc-proyecto
    url: http://${upstream_proyecto}:8000
    routes:
      - name: route-proyecto
        paths: [/api/proyectos]
        strip_path: false
        methods: [GET, POST, PUT, PATCH, DELETE]

  - name: svc-area
    url: http://${upstream_area}:8000
    routes:
      - name: route-area
        paths: [/api/areas]
        strip_path: false
        methods: [GET, POST, PUT, PATCH, DELETE]

  - name: svc-empresa
    url: http://${upstream_empresa}:8000
    routes:
      - name: route-empresa
        paths: [/api/empresas]
        strip_path: false
        methods: [GET, POST, PUT, PATCH, DELETE]

plugins:
  - name: correlation-id
    config:
      header_name: X-Request-ID
      generator: uuid
      echo_downstream: true
KONG

# Levantar Kong en modo DB-less
docker run -d \
  --name kong \
  --restart unless-stopped \
  -e KONG_DATABASE=off \
  -e KONG_DECLARATIVE_CONFIG=/kong/kong.yml \
  -e KONG_PROXY_ACCESS_LOG=/dev/stdout \
  -e KONG_ADMIN_ACCESS_LOG=/dev/stdout \
  -e KONG_PROXY_ERROR_LOG=/dev/stderr \
  -e KONG_ADMIN_LISTEN="0.0.0.0:8001" \
  -v /etc/kong:/kong \
  -p 8000:8000 \
  -p 8001:8001 \
  kong:3.6
