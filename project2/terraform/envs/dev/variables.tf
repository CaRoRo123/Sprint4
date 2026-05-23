variable "project"       { default = "biteco" }
variable "env"            { default = "dev" }
variable "aws_region"    { default = "us-east-1" }
variable "instance_type" { default = "t2.medium" }

# Ubuntu 24.04 LTS us-east-1 — verificar en https://cloud-images.ubuntu.com/locator/ec2/
variable "ami_id"        { default = "ami-0c7217cdde317cfec" }

variable "key_name" {
  default = "dac_key" 
}

variable "db_username" {
  default = "biteco_admin"
}

variable "db_password" {
  default = "12345678"
}
