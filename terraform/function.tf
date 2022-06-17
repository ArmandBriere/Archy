
# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "source" {
  for_each = var.python_functions

  type        = "zip"
  source_dir  = "../src/functions/${each.key}"
  output_path = "/tmp/${each.key}.zip"
  excludes    = ["node_modules", "__pycache__", "cmd", "go.sum"]
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "zip" {
  for_each = var.python_functions

  source       = "/tmp/${each.key}.zip"
  content_type = "application/zip"

  # Append to the MD5 checksum of the files's content
  # to force the zip to be updated as soon as a change occurs
  name   = "src-${data.archive_file.source[each.key].output_sha}.zip"
  bucket = google_storage_bucket.function_bucket.name
}

# Create the Cloud function
resource "google_cloudfunctions_function" "function" {
  for_each = var.python_functions

  description = each.value.description

  name    = each.key
  runtime = each.value.runtime

  # Get the source code of the cloud function as a Zip compression
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.zip[each.key].name

  # Must match the function name in the cloud function `main.py` source code
  entry_point = each.key

  # Timeout
  timeout = each.value.timeout

  # Memory
  available_memory_mb = each.value.memory

  # Trigger
  trigger_http = true

  # Instances count
  min_instances = 0
  max_instances = 5

  # Secrets
  dynamic "secret_environment_variables" {
    for_each = var.secrets
    content {
      key     = secret_environment_variables.value
      secret  = secret_environment_variables.value
      version = "latest"
    }
  }

  # Service account
  service_account_email = var.service_account_email
}
