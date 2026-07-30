variable "aws_region" {
  description = "Regiao AWS utilizada pelo Learner Lab."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nome-base utilizado nos recursos."
  type        = string
  default     = "ingestao-lab"
}

variable "instance_type" {
  description = "Tipo da instancia EC2."
  type        = string
  default     = "t3.small"
}

variable "db_instance_class" {
  description = "Classe da instancia RDS PostgreSQL."
  type        = string
  default     = "db.t3.micro"
}

variable "db_name" {
  description = "Nome do banco de dados."
  type        = string
  default     = "ecommerce"
}

variable "db_username" {
  description = "Usuario administrador do PostgreSQL."
  type        = string
  default     = "ecommerce"
}

variable "db_password" {
  description = "Senha do PostgreSQL. Deve ser informada no terraform.tfvars."
  type        = string
  sensitive   = true

  validation {
    condition     = length(var.db_password) >= 12
    error_message = "A senha deve possuir pelo menos 12 caracteres."
  }
}

variable "key_name" {
  description = "Nome do par de chaves criado pelo AWS Academy."
  type        = string
  default     = "vockey"
}

variable "lab_instance_profile" {
  description = "Instance profile pre-criado pelo AWS Academy."
  type        = string
  default     = "LabInstanceProfile"
}

variable "ssh_cidr" {
  description = "Endereco IPv4 autorizado a acessar a EC2 por SSH."
  type        = string
  default     = "127.0.0.1/32"

  validation {
    condition     = can(cidrnetmask(var.ssh_cidr))
    error_message = "ssh_cidr deve ser um bloco CIDR valido, como 203.0.113.10/32."
  }
}

variable "ec2_availability_zones" {
  description = "Zonas de disponibilidade consideradas para a EC2."
  type        = list(string)

  default = [
    "us-east-1a",
    "us-east-1b",
    "us-east-1c",
    "us-east-1d",
    "us-east-1f"
  ]
}