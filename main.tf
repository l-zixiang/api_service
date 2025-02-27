provider "google" {
  project = var.project_id
  region  = var.region
}

# Create a Redis instance in Google Cloud
resource "google_redis_instance" "my_redis_instance" {
  name             = var.redis_instance_name
  tier             = "STANDARD_HA"
  memory_size_gb   = var.redis_memory_size_gb
  location_id      = var.region
  redis_version    = "REDIS_4_X"
  display_name     = var.redis_instance_name
}

# Create a Cloud Run service
resource "google_cloud_run_service" "my_cloud_run_service" {
  name     = var.cloud_run_service_name
  location = var.region

  template {
    spec {
      containers {
        image = var.container_image
        ports {
          container_port = 8080
        }
        env {
          name  = "COINMARKETCAP_API_KEY"
          value = var.coinmarketcap_api_key  # Set the CoinMarketCap API key as an environment variable
        }
      }
    }
  }

  traffic {
    latest_revision = true
    percent         = 100
  }
}

# Allow public access to the Cloud Run service
resource "google_cloud_run_service_iam_member" "allow_public" {
  service = google_cloud_run_service.my_cloud_run_service.name
  location = var.region
  role     = "roles/run.invoker"
  member   = "allUsers"  # Make the Cloud Run service public
}

# Optionally, create a service account to access Cloud Run and Redis
resource "google_service_account" "cloud_run_service_account" {
  account_id = "cloud-run-service-account"
  display_name = "Cloud Run Service Account"
}

# Grant the service account permissions to access the Redis instance
resource "google_project_iam_member" "redis_access" {
  role   = "roles/redis.viewer"
  member = "serviceAccount:${google_service_account.cloud_run_service_account.email}"
}
