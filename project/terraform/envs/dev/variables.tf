variable "project" {
  description = "Nombre del proyecto"
  type        = string
  default     = "biteco"
}

variable "env" {
  description = "Ambiente (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "Región AWS"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "Tipo de instancia EC2"
  type        = string
  default     = "t3.nano"
}

variable "ami_id" {
  description = "AMI Ubuntu 24.04 LTS para us-east-1"
  type        = string
  default     = "ami-0c7217cdde317cfec"  # Ubuntu 24.04 us-east-1 (actualizar si cambia)
}

variable "key_name" {
  description = "Nombre del key pair SSH en AWS"
  type        = string
}

variable "db_username" {
  description = "Usuario de Aurora PostgreSQL"
  type        = string
  default     = "biteco_admin"
}

variable "db_password" {
  description = "Contraseña de Aurora PostgreSQL"
  type        = string
  sensitive   = true
}
