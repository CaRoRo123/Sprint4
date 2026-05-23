variable "project"          {}
variable "service_name"     {}
variable "env"               {}
variable "instance_type"    {}
variable "ami_id"            {}
variable "key_name"          {}
variable "vpc_id"            {}
variable "public_subnet_id" {}
variable "private_subnets"  { type = list(string) }
variable "db_username"      {}
variable "db_password"      { sensitive = true }
variable "tags"              { type = map(string) }

locals {
  prefix = "${var.project}-${var.env}-${var.service_name}"
}

# ─── SECURITY GROUPS ─────────────────────────────────────────────────────────
resource "aws_security_group" "ec2" {
  name        = "${local.prefix}-ec2-sg"
  description = "EC2 ${var.service_name}"
  vpc_id      = var.vpc_id

  ingress {
    description = "Django desde Kong (VPC interna)"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  ingress {
    description = "SSH administración"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]   # restricción recomendada en prod
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, { Name = "${local.prefix}-ec2-sg" })
}

resource "aws_security_group" "rds" {
  name        = "${local.prefix}-rds-sg"
  description = "Aurora ${var.service_name}"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.ec2.id]
  }

  tags = merge(var.tags, { Name = "${local.prefix}-rds-sg" })
}

resource "aws_security_group" "redis" {
  name        = "${local.prefix}-redis-sg"
  description = "ElastiCache ${var.service_name}"
  vpc_id      = var.vpc_id

  ingress {
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.ec2.id]
  }

  tags = merge(var.tags, { Name = "${local.prefix}-redis-sg" })
}

# ─── EC2 ──────────────────────────────────────────────────────────────────────
resource "aws_instance" "service" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = var.public_subnet_id
  vpc_security_group_ids = [aws_security_group.ec2.id]
  key_name               = var.key_name

  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io docker-compose git
    systemctl enable docker
    systemctl start docker
    usermod -aG docker ubuntu
  EOF

  tags = merge(var.tags, { Name = "${local.prefix}-ec2" })
}

# ─── RDS AURORA POSTGRESQL ───────────────────────────────────────────────────
resource "aws_db_subnet_group" "this" {
  name       = "${local.prefix}-db-subnet"
  subnet_ids = var.private_subnets
  tags       = var.tags
}

resource "aws_rds_cluster" "aurora" {
  cluster_identifier      = "${local.prefix}-aurora"
  engine                  = "aurora-postgresql"
  engine_version          = "15.4"
  database_name           = "${var.service_name}_db"
  master_username         = var.db_username
  master_password         = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.this.name
  vpc_security_group_ids  = [aws_security_group.rds.id]
  skip_final_snapshot     = true   # cambiar a false en prod
  deletion_protection     = false  # cambiar a true en prod

  tags = merge(var.tags, { Name = "${local.prefix}-aurora" })
}

resource "aws_rds_cluster_instance" "writer" {
  identifier         = "${local.prefix}-aurora-writer"
  cluster_identifier = aws_rds_cluster.aurora.id
  instance_class     = "db.t3.medium"
  engine             = aws_rds_cluster.aurora.engine
  engine_version     = aws_rds_cluster.aurora.engine_version

  tags = var.tags
}

# ─── ELASTICACHE REDIS ───────────────────────────────────────────────────────
resource "aws_elasticache_subnet_group" "this" {
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
  subnet_group_name    = aws_elasticache_subnet_group.this.name
  security_group_ids   = [aws_security_group.redis.id]

  tags = merge(var.tags, { Name = "${local.prefix}-redis" })
}

# ─── OUTPUTS ─────────────────────────────────────────────────────────────────
output "private_ip" {
  value = aws_instance.service.private_ip
}

output "rds_endpoint" {
  value = aws_rds_cluster.aurora.endpoint
}

output "redis_endpoint" {
  value = aws_elasticache_cluster.redis.cache_nodes[0].address
}
