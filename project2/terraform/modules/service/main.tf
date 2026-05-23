# ─────────────────────────────────────────────────────────────────────────────
# Modulo: service
# Crea todo lo necesario para UN microservicio:
#   EC2 (Django)  ·  Aurora PostgreSQL (write side)
#   ElastiCache Redis (cache)  ·  DynamoDB (read side)
#   IAM role con permisos minimos
# ─────────────────────────────────────────────────────────────────────────────

variable "project"          { type = string }
variable "service_name"     { type = string }
variable "env"               { type = string }
variable "instance_type"    { type = string }
variable "ami_id"            { type = string }
variable "key_name"          { type = string }
variable "vpc_id"            { type = string }
variable "public_subnet_id" { type = string }
variable "private_subnets"  { type = list(string) }
variable "db_username"      { type = string }
variable "db_password"      { 
                              type = string
                              sensitive = true
                                 }
variable "tags"              { type = map(string) }

locals {
  prefix = "${var.project}-${var.env}-${var.service_name}"
}

# ── SECURITY GROUPS ───────────────────────────────────────────────────────────
resource "aws_security_group" "ec2" {
  name        = "${local.prefix}-ec2-sg"
  description = "EC2 ${var.service_name} - permite trafico desde Kong (interno)"
  vpc_id      = var.vpc_id

  ingress {
    description = "Django desde Kong"
    from_port   = 8000
    to_port = 8000
    protocol = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  ingress {
    description = "SSH administracion"
    from_port   = 22
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # restringir a tu IP en prod
  }
  egress {
    from_port   = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, { Name = "${local.prefix}-ec2-sg" })
}

resource "aws_security_group" "rds" {
  name        = "${local.prefix}-rds-sg"
  description = "Aurora - solo desde EC2 del servicio"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 5432
    to_port = 5432
    protocol = "tcp"
    security_groups = [aws_security_group.ec2.id]
  }
  tags = merge(var.tags, { Name = "${local.prefix}-rds-sg" })
}

resource "aws_security_group" "redis" {
  name        = "${local.prefix}-redis-sg"
  description = "ElastiCache - solo desde EC2 del servicio"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 6379
    to_port = 6379
    protocol = "tcp"
    security_groups = [aws_security_group.ec2.id]
  }
  tags = merge(var.tags, { Name = "${local.prefix}-redis-sg" })
}


# ── EC2 ───────────────────────────────────────────────────────────────────────
resource "aws_instance" "service" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = var.public_subnet_id
  vpc_security_group_ids = [aws_security_group.ec2.id]
  key_name               = var.key_name
  iam_instance_profile   = "LabInstanceProfile"

  user_data = <<-EOF
    #!/bin/bash
    set -e
    apt-get update -y
    apt-get install -y docker.io git
    systemctl enable docker
    systemctl start docker
    usermod -aG docker ubuntu
  EOF

  tags = merge(var.tags, { Name = "${local.prefix}-ec2" })
}

# ── AURORA POSTGRESQL (write side) ────────────────────────────────────────────
resource "aws_db_subnet_group" "aurora" {
  name       = "${local.prefix}-aurora-subnet"
  subnet_ids = var.private_subnets
  tags       = var.tags
}

resource "aws_rds_cluster" "aurora" {
  cluster_identifier     = "${local.prefix}-aurora"
  engine                 = "aurora-postgresql"
  engine_version         = "15.4"
  database_name          = "${var.service_name}_db"
  master_username        = var.db_username
  master_password        = var.db_password
  db_subnet_group_name   = aws_db_subnet_group.aurora.name
  vpc_security_group_ids = [aws_security_group.rds.id]
  skip_final_snapshot    = true   # cambiar a false en prod
  deletion_protection    = false  # cambiar a true en prod

  tags = merge(var.tags, { Name = "${local.prefix}-aurora" })
}

resource "aws_rds_cluster_instance" "writer" {
  identifier         = "${local.prefix}-aurora-writer"
  cluster_identifier = aws_rds_cluster.aurora.id
  instance_class     = "db.t3.medium"
  engine             = aws_rds_cluster.aurora.engine
  engine_version     = aws_rds_cluster.aurora.engine_version
  tags               = var.tags
}

# ── ELASTICACHE REDIS (cache) ─────────────────────────────────────────────────
resource "aws_elasticache_subnet_group" "redis" {
  name       = "${local.prefix}-redis-subnet"
  subnet_ids = var.private_subnets
  tags       = var.tags
}

resource "aws_elasticache_cluster" "redis" {
  cluster_id           = "${local.prefix}-redis"
  engine               = "redis"
  engine_version       = "7.1"
  node_type            = "cache.t3.micro"
  num_cache_nodes      = 1
  parameter_group_name = "default.redis7"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.redis.name
  security_group_ids   = [aws_security_group.redis.id]

  tags = merge(var.tags, { Name = "${local.prefix}-redis" })
}

# ── DYNAMODB (read side) ──────────────────────────────────────────────────────
# Single-table design con GSI para listar por tipo de entidad
resource "aws_dynamodb_table" "read_side" {
  name         = "${local.prefix}-table"
  billing_mode = "PAY_PER_REQUEST"   # sin capacidad provisionada - escala solo
  hash_key     = "PK"
  range_key    = "SK"

  attribute {
    name = "PK"
    type = "S"
  }
  attribute {
    name = "SK"
    type = "S"
  }
  attribute {
    name = "entity_type"
    type = "S"
  }
  attribute {
    name = "created_at"
    type = "S"
  }

  # GSI para listar todos los items de un tipo (ej: todos los PROYECTO)
  global_secondary_index {
    name               = "entity_type-index"
    hash_key           = "entity_type"
    range_key          = "created_at"
    projection_type    = "ALL"
  }

  point_in_time_recovery {
    enabled = true
  }

  tags = merge(var.tags, { Name = "${local.prefix}-dynamo" })
}

# ── OUTPUTS ───────────────────────────────────────────────────────────────────
output "private_ip"      { value = aws_instance.service.private_ip }
output "rds_endpoint"    { value = aws_rds_cluster.aurora.endpoint }
output "redis_endpoint"  { value = aws_elasticache_cluster.redis.cache_nodes[0].address }
output "dynamo_table"    { value = aws_dynamodb_table.read_side.name }
output "dynamo_arn"      { value = aws_dynamodb_table.read_side.arn }
