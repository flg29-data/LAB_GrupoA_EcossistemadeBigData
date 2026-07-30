output "account_id" {
  description = "Identificador da conta AWS do Learner Lab."
  value       = data.aws_caller_identity.current.account_id
}

output "aws_region" {
  description = "Regiao utilizada."
  value       = var.aws_region
}

output "ec2_instance_id" {
  description = "Identificador da instancia EC2."
  value       = aws_instance.runner.id
}

output "ec2_public_ip" {
  description = "Endereco IPv4 publico da EC2."
  value       = aws_instance.runner.public_ip
}

output "rds_endpoint" {
  description = "Endpoint DNS do RDS PostgreSQL."
  value       = aws_db_instance.postgres.address
}

output "rds_port" {
  description = "Porta do PostgreSQL."
  value       = aws_db_instance.postgres.port
}

output "db_name" {
  description = "Nome do banco de dados."
  value       = var.db_name
}

output "db_username" {
  description = "Usuario do banco de dados."
  value       = var.db_username
}

output "s3_bucket" {
  description = "Nome do bucket S3."
  value       = aws_s3_bucket.datalake.bucket
}

output "ssh_command" {
  description = "Comando sugerido para acessar a EC2."
  value       = "ssh -i $HOME/.ssh/labsuser.pem ec2-user@${aws_instance.runner.public_ip}"
}