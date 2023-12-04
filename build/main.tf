#File Zip for the Cloud Function
data "archive_file" "my_function_zip" {
    type = "zip"
    source_dir = "${path.module}/../cloud_function"
    output_path = "${path.module}/../cloud_function.zip"
}

#Cloud Storage Create a Bucket
resource "google_storage_bucket" "function_source_bucket" {
  name = "dbt-function"
  location = var.region
}

#Cloud Storage create a bucket_object
resource "google_storage_bucket_object" "function_source_bucket_object" {
  name   = "dbt-function-bucket-object"
  bucket = google_storage_bucket.function_source_bucket.name
  source = data.archive_file.my_function_zip.output_path
}

#Google Cloud Function  
resource "google_cloudfunctions2_function" "my_function" {
    name = "dbt-function-terraform"
    description = "dbt function to deploy"
    location = var.region

    build_config {
    runtime     = "python310"
    entry_point = "main" 
    
      source {
        storage_source {
          bucket = google_storage_bucket.function_source_bucket.name
          object = google_storage_bucket_object.function_source_bucket_object.name
        }
      }
    }
    service_config {
    max_instance_count  = 1
    min_instance_count = 0
    available_memory    = "512M"
    timeout_seconds     = 180
    all_traffic_on_latest_revision = true
    service_account_email = "brasil-api-cloud-storage@apt-theme-402300.iam.gserviceaccount.com"

      secret_volumes {
        project_id = var.project_id
        mount_path = "/secrets"
        secret = "dbt_creds"
      }
    }

    }

#Cloud Scheduler
resource "google_cloud_scheduler_job" "dbt-job" {
  name        = "dbt-job-scheduler"
  description = "scheduler to run dbt datawarehouse"
  time_zone   = "America/Sao_Paulo"
  schedule    = "0 9 * * *"
  attempt_deadline = "320s"

    http_target {
    http_method = "GET"
    uri         = google_cloudfunctions2_function.my_function.service_config[0].uri

    oidc_token {
      service_account_email = "brasil-api-cloud-storage@apt-theme-402300.iam.gserviceaccount.com"
    }
}
}
