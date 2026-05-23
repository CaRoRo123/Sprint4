terraform {
  required_version = ">= 1.7"
  required_providers {
    aws = { source = "hashicorp/aws", version = "~> 5.50" }
  }

  # Descomentá cuando tengas el bucket de estado remoto listo
  # backend "s3" {
  #   bucket = "biteco-terraform-state"
  #   key    = "dev/terraform.tfstate"
  #   region = "us-east-1"
  # }
}

provider "aws" { region = var.aws_region }

# ── VPC ───────────────────────────────────────────────────────────────────────
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.8"

  name             = "${var.project}-${var.env}-vpc"
  cidr             = "10.0.0.0/16"
  azs              = ["${var.aws_region}a", "${var.aws_region}b"]
  private_subnets  = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets   = ["10.0.101.0/24", "10.0.102.0/24"]
  enable_nat_gateway = true
  single_nat_gateway = true   # dev: 1 NAT para ahorrar costos

  tags = local.tags
}

# ── SERVICIO PROYECTO ─────────────────────────────────────────────────────────
module "svc_proyecto" {
  source           = "../../modules/service"
  project          = var.project
  env              = var.env
  service_name     = "proyecto"
  instance_type    = var.instance_type
  ami_id           = var.ami_id
  key_name         = var.key_name
  vpc_id           = module.vpc.vpc_id
  public_subnet_id = module.vpc.public_subnets[0]
  private_subnets  = module.vpc.private_subnets
  db_username      = var.db_username
  db_password      = var.db_password
  tags             = local.tags
}

# ── SERVICIO AREA ─────────────────────────────────────────────────────────────
module "svc_area" {
  source           = "../../modules/service"
  project          = var.project
  env              = var.env
  service_name     = "area"
  instance_type    = var.instance_type
  ami_id           = var.ami_id
  key_name         = var.key_name
  vpc_id           = module.vpc.vpc_id
  public_subnet_id = module.vpc.public_subnets[0]
  private_subnets  = module.vpc.private_subnets
  db_username      = var.db_username
  db_password      = var.db_password
  tags             = local.tags
}

# ── SERVICIO EMPRESA ──────────────────────────────────────────────────────────
module "svc_empresa" {
  source           = "../../modules/service"
  project          = var.project
  env              = var.env
  service_name     = "empresa"
  instance_type    = var.instance_type
  ami_id           = var.ami_id
  key_name         = var.key_name
  vpc_id           = module.vpc.vpc_id
  public_subnet_id = module.vpc.public_subnets[0]
  private_subnets  = module.vpc.private_subnets
  db_username      = var.db_username
  db_password      = var.db_password
  tags             = local.tags
}

# ── KONG API GATEWAY ──────────────────────────────────────────────────────────
module "kong" {
  source            = "../../modules/kong"
  project           = var.project
  env               = var.env
  instance_type     = var.instance_type
  ami_id            = var.ami_id
  key_name          = var.key_name
  vpc_id            = module.vpc.vpc_id
  public_subnet_id  = module.vpc.public_subnets[0]
  upstream_proyecto = module.svc_proyecto.private_ip
  upstream_area     = module.svc_area.private_ip
  upstream_empresa  = module.svc_empresa.private_ip
  tags              = local.tags
}

locals {
  tags = {
    Project     = var.project
    Environment = var.env
    ManagedBy   = "terraform"
  }
}
