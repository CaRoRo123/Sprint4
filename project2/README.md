# BiteCo — Microservicios con CQRS, Aurora, DynamoDB y Kong

## Arquitectura

```
Cliente
  └─▶ Kong :8000 (API Gateway)
        ├─▶ /api/proyectos  →  svc-proyecto  (EC2 Django)
        ├─▶ /api/areas      →  svc-area      (EC2 Django)
        └─▶ /api/empresas   →  svc-empresa   (EC2 Django)

Cada servicio:
  POST/PATCH/DELETE  →  Aurora PostgreSQL  (write side)
                              │
                         Django signal (post_save)
                              │
                              ▼
                        DynamoDB          (read side, sync automático)

  GET  →  DynamoDB (nunca toca Aurora en lectura)

  Reportes:
    POST /reportes/generar/  →  AWS Cost Explorer  →  Aurora + DynamoDB
    GET  /reportes/<mes>/    →  DynamoDB
```

## Estructura del proyecto

```
project/
├── docker-compose.yml
├── kong/kong.yml
├── services/
│   ├── proyecto/
│   │   └── app/
│   │       ├── cqrs/
│   │       │   ├── commands.py   # escribe en Aurora
│   │       │   ├── queries.py    # lee de DynamoDB
│   │       │   ├── sync.py       # proyecta Aurora → DynamoDB
│   │       │   └── dynamo.py     # cliente DynamoDB (single-table design)
│   │       ├── reports/
│   │       │   └── cost_explorer.py  # llama AWS Cost Explorer
│   │       ├── models/           # modelos Aurora + señales Django
│   │       ├── serializers/
│   │       └── views/
│   │           ├── commands.py   # POST/PATCH/DELETE
│   │           └── queries.py    # GET
│   ├── area/    (misma estructura)
│   └── empresa/ (misma estructura)
└── terraform/
    ├── modules/
    │   ├── service/  # EC2 + Aurora + Redis + DynamoDB + IAM
    │   └── kong/     # EC2 Kong
    └── envs/dev/
```

---

## Paso 1 — Infraestructura AWS (Terraform)

```bash
cd terraform/envs/dev

# Inicializar (descarga providers y módulo VPC)
terraform init

# Ver plan
terraform plan \
  -var="key_name=TU_KEY_PAIR" \
  -var="db_password=TuPasswordSegura123"

# Aplicar (~15 min, Aurora tarda)
terraform apply \
  -var="key_name=TU_KEY_PAIR" \
  -var="db_password=TuPasswordSegura123"
```

## Paso 2 — Pegar endpoints en los .env

```bash
# Copiá cada valor en su .env correspondiente
terraform output rds_proyecto_endpoint    # → services/proyecto/.env DATABASE_URL
terraform output rds_area_endpoint        # → services/area/.env
terraform output rds_empresa_endpoint     # → services/empresa/.env

terraform output redis_proyecto_endpoint  # → services/proyecto/.env REDIS_URL
terraform output redis_area_endpoint
terraform output redis_empresa_endpoint

terraform output dynamo_proyecto_table    # → services/proyecto/.env DYNAMODB_TABLE
terraform output dynamo_area_table
terraform output dynamo_empresa_table
```

## Paso 3 — Levantar servicios

```bash
docker compose up --build
```

## Paso 4 — Migraciones (primera vez)

```bash
docker compose exec svc-proyecto python manage.py migrate
docker compose exec svc-area     python manage.py migrate
docker compose exec svc-empresa  python manage.py migrate
```

---

## Endpoints disponibles (todos a través de Kong :8000)

### Empresas
| Método | URL | Descripción |
|--------|-----|-------------|
| GET    | /api/empresas/ | Lista empresas (DynamoDB) |
| GET    | /api/empresas/<id>/ | Detalle empresa (DynamoDB) |
| POST   | /api/empresas/crear/ | Crear empresa (Aurora → DynamoDB) |
| PATCH  | /api/empresas/<id>/actualizar/ | Actualizar |
| DELETE | /api/empresas/<id>/eliminar/ | Soft-delete |
| POST   | /api/empresas/<id>/reportes/generar/ | Generar reporte AWS |
| GET    | /api/empresas/<id>/reportes/ | Listar reportes (DynamoDB) |
| GET    | /api/empresas/<id>/reportes/2024-01/ | Reporte de un mes (DynamoDB) |

### Areas y Proyectos — mismos endpoints bajo /api/areas/ y /api/proyectos/

### Generar reporte — body esperado
```json
{ "mes": "2024-01" }
```

### Respuesta de reporte
```json
{
  "id": 1,
  "mes": "2024-01",
  "costo_total": "143.2700",
  "moneda": "USD",
  "mensaje": "Reporte generado correctamente"
}
```

---

## DynamoDB — single-table design

| PK | SK | Contiene |
|----|----|----------|
| PROYECTO#1 | METADATA | Datos del proyecto |
| PROYECTO#1 | REPORT#2024-01 | Reporte de costos enero |
| AREA#1 | METADATA | Datos del área |
| EMPRESA#1 | METADATA | Datos de la empresa |

GSI `entity_type-index` permite listar todos los ítems de un tipo.

---

## IAM — permisos del EC2

Cada EC2 tiene un role con:
- `dynamodb:GetItem/PutItem/DeleteItem/Query/Scan` sobre su tabla
- `ce:GetCostAndUsage` (Cost Explorer — recurso global)

No se necesitan access keys en el código, boto3 usa el role del EC2 automáticamente.

---

## Próximos pasos

- [ ] Auth0: agregar plugin `jwt` en kong.yml
- [ ] Rate limiting: agregar plugin `rate-limiting` en kong.yml
- [ ] Lambda para sync asíncrono Aurora → DynamoDB vía DynamoDB Streams
- [ ] GitHub Actions para CI/CD
- [ ] Cambiar `skip_final_snapshot = false` y `deletion_protection = true` para prod
