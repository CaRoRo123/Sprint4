# ── Kong ──────────────────────────────────────────────────────────────────────
output "kong_public_ip" {
  description = "IP pública del API Gateway — apuntá tu DNS aquí"
  value       = module.kong.public_ip
}

# ── Endpoints para los .env de cada servicio ──────────────────────────────────
output "rds_proyecto_endpoint"   { value = module.svc_proyecto.rds_endpoint }
output "rds_area_endpoint"       { value = module.svc_area.rds_endpoint }
output "rds_empresa_endpoint"    { value = module.svc_empresa.rds_endpoint }

output "redis_proyecto_endpoint" { value = module.svc_proyecto.redis_endpoint }
output "redis_area_endpoint"     { value = module.svc_area.redis_endpoint }
output "redis_empresa_endpoint"  { value = module.svc_empresa.redis_endpoint }

output "dynamo_proyecto_table"   { value = module.svc_proyecto.dynamo_table }
output "dynamo_area_table"       { value = module.svc_area.dynamo_table }
output "dynamo_empresa_table"    { value = module.svc_empresa.dynamo_table }

output "ec2_proyecto_ip"         { value = module.svc_proyecto.private_ip }
output "ec2_area_ip"             { value = module.svc_area.private_ip }
output "ec2_empresa_ip"          { value = module.svc_empresa.private_ip }
