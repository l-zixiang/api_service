# variables.tf

# Google Cloud Project ID
variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

# GCP region
variable "region" {
  description = "The GCP region for the deployment"
  default     = "us-central1"
}

# Redis instance memory size in GB
variable "redis_memory_size_gb" {
  description = "The memory size of the Redis instance in GB"
  type        = number
  default     = 1
}

# Redis instance name
variable "redis_instance_name" {
  description = "The name of the Redis instance"
  type        = string
  default     = "my-redis-instance"
}

# Cloud Run service name
variable "cloud_run_service_name" {
  description = "The name of the Cloud Run service"
  type        = string
  default     = "my-cloud-run-service"
}

# Docker container image URL
variable "container_image" {
  description = "The URL of the Docker container image"
  type        = string
}

# CoinMarketCap API Key
variable "coinmarketcap_api_key" {
  description = "The CoinMarketCap API key"
  type        = string
}
