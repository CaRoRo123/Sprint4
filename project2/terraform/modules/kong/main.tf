variable "project"           { type = string }
variable "env"                { type = string }
variable "instance_type"     { type = string }
variable "ami_id"             { type = string }
variable "key_name"           { type = string }
variable "vpc_id"             { type = string }
variable "public_subnet_id"  { type = string }
variable "upstream_proyecto" { type = string }
variable "upstream_area"     { type = string }
variable "upstream_empresa"  { type = string }
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
    to_port = 8000
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "Admin API — solo VPC interna"
    from_port   = 8001
    to_port = 8001
    protocol = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
  ingress {
    from_port   = 22 
    to_port = 22
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port = 0
    protocol = "-1"
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

  user_data = templatefile("${path.module}/kong-init.sh.tpl", {
    upstream_proyecto = var.upstream_proyecto
    upstream_area     = var.upstream_area
    upstream_empresa  = var.upstream_empresa
  })

  tags = merge(var.tags, { Name = "${local.prefix}-ec2" })
}

output "public_ip"  { value = aws_instance.kong.public_ip }
output "private_ip" { value = aws_instance.kong.private_ip }
