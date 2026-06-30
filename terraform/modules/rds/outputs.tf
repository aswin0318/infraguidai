output "endpoint" {
  description = "RDS instance endpoint (host:port)"
  value       = aws_db_instance.this.endpoint
}

output "address" {
  description = "RDS instance address (hostname only)"
  value       = aws_db_instance.this.address
}

output "db_name" {
  description = "Database name"
  value       = aws_db_instance.this.db_name
}

output "username" {
  description = "Database master username"
  value       = aws_db_instance.this.username
}

output "password" {
  description = "Database master password"
  value       = random_password.db.result
  sensitive   = true
}

output "port" {
  description = "Database port"
  value       = aws_db_instance.this.port
}
