output "kong_public_ip" {
  description = "IP pública del API Gateway (Kong) — apuntá tu DNS aquí"
  value       = module.kong.public_ip
}

output "svc_proyecto_private_ip" {
  value = module.svc_proyecto.private_ip
}

output "svc_area_private_ip" {
  value = module.svc_area.private_ip
}

output "svc_empresa_private_ip" {
  value = module.svc_empresa.private_ip
}

output "rds_proyecto_endpoint" {
  value = module.svc_proyecto.rds_endpoint
}

output "rds_area_endpoint" {
  value = module.svc_area.rds_endpoint
}

output "rds_empresa_endpoint" {
  value = module.svc_empresa.rds_endpoint
}

output "redis_proyecto_endpoint" {
  value = module.svc_proyecto.redis_endpoint
}

output "redis_area_endpoint" {
  value = module.svc_area.redis_endpoint
}

output "redis_empresa_endpoint" {
  value = module.svc_empresa.redis_endpoint
}
