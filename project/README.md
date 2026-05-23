# BiteCo — Arquitectura de Microservicios

## Estructura del proyecto

```
project/
├── docker-compose.yml          # Desarrollo local (servicios + Kong)
├── kong/
│   └── kong.yml                # Config declarativa de Kong (local)
├── services/
│   ├── proyecto/               # Svc Proyecto (Django)
│   ├── area/                   # Svc Area (Django)
│   └── empresa/                # Svc Empresa (Django)
└── terraform/
    ├── envs/dev/               # Ambiente de desarrollo en AWS
    └── modules/
        ├── service/            # Módulo reutilizable: EC2 + Aurora + Redis
        └── kong/               # Módulo Kong EC2
```

---

## Desarrollo local

### 1. Configurar variables de entorno

Cada servicio tiene un `.env`. Editá los 3 con tus endpoints de AWS:

```
services/proyecto/.env
services/area/.env
services/empresa/.env
```

Cambiá `<RDS_ENDPOINT>` y `<ELASTICACHE_ENDPOINT>` por los valores reales
que obtenés del `terraform output` (ver sección de Terraform más abajo).

### 2. Levantar todo

```bash
docker compose up --build
```

### 3. Correr migraciones (primera vez)

```bash
docker compose exec svc-proyecto python manage.py migrate
docker compose exec svc-area     python manage.py migrate
docker compose exec svc-empresa  python manage.py migrate
```

### 4. Probar los endpoints a través de Kong

```bash
# Kong escucha en :8000 y enruta a los servicios internos
curl http://localhost:8000/api/proyectos/
curl http://localhost:8000/api/areas/
curl http://localhost:8000/api/empresas/
```

---

## Infraestructura AWS (Terraform)

### Prerequisitos

- AWS CLI configurado (`aws configure`)
- Terraform >= 1.7
- Un key pair SSH creado en AWS

### Primer deploy

```bash
cd terraform/envs/dev

# Inicializar (descarga módulos y providers)
terraform init

# Ver qué va a crear
terraform plan -var="key_name=TU_KEY_PAIR" -var="db_password=TuPasswordSegura"

# Aplicar
terraform apply -var="key_name=TU_KEY_PAIR" -var="db_password=TuPasswordSegura"
```

### Obtener endpoints para el .env

```bash
terraform output rds_proyecto_endpoint   # → pegalo en services/proyecto/.env
terraform output rds_area_endpoint
terraform output rds_empresa_endpoint
terraform output redis_proyecto_endpoint
terraform output redis_area_endpoint
terraform output redis_empresa_endpoint
terraform output kong_public_ip          # → IP pública del gateway
```

### Destruir el ambiente

```bash
terraform destroy -var="key_name=TU_KEY_PAIR" -var="db_password=TuPasswordSegura"
```

---

## Flujo de rutas (Kong → Servicios)

```
Cliente
  └─▶ :8000/api/proyectos/*  ──▶  svc-proyecto:8000
  └─▶ :8000/api/areas/*      ──▶  svc-area:8000
  └─▶ :8000/api/empresas/*   ──▶  svc-empresa:8000
```

---

## Próximos pasos

1. **Implementar las views** — cada view tiene un `# TODO` claro
2. **Agregar Auth0** — añadir plugin `jwt` en kong.yml
3. **Rate limiting** — añadir plugin `rate-limiting` en kong.yml
4. **CI/CD** — GitHub Actions para build Docker + terraform apply
