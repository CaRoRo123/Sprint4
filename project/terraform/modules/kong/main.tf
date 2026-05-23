variable "project"           {}
variable "env"                {}
variable "instance_type"     {}
variable "ami_id"             {}
variable "key_name"           {}
variable "vpc_id"             {}
variable "public_subnet_id"  {}
variable "upstream_proyecto" {}
variable "upstream_area"     {}
variable "upstream_empresa"  {}
variable "tags"               { type = map(string) }

locals {
  prefix = "${var.project}-${var.env}-kong"
}

resource "aws_security_group" "kong" {
  name        = "${local.prefix}-sg"
  description = "Kong API Gateway"
  vpc_id      = var.vpc_id

  ingress {
    description = "HTTP proxy público"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Admin API (solo VPC en prod)"
    from_port   = 8001
    to_port     = 8001
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = merge(var.tags, { Name = "${local.prefix}-sg" })
}

resource "aws_instance" "kong" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  subnet_id              = var.public_subnet_id
  vpc_security_group_ids = [aws_security_group.kong.id]
  key_name               = var.key_name

  # Genera el kong.yml con las IPs reales de los servicios al hacer apply
  user_data = templatefile("${path.module}/kong-init.sh.tpl", {
    upstream_proyecto = var.upstream_proyecto
    upstream_area     = var.upstream_area
    upstream_empresa  = var.upstream_empresa
  })

  tags = merge(var.tags, { Name = "${local.prefix}-ec2" })
}

output "public_ip" {
  value = aws_instance.kong.public_ip
}
