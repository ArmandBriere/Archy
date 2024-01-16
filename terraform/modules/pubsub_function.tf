
# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "pubsub_function_source" {
  for_each = { for pubsub_function in var.pubsub_functions : pubsub_function.name => pubsub_function }

  type        = "zip"
  source_dir  = "${var.src_dir}/functions/${each.key}"
  output_path = "/tmp/${each.key}.zip"
  excludes    = ["node_modules", "__pycache__", "cmd", "go.sum", "env"]
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "pubsub_function_zip" {
  for_each = { for pubsub_function in var.pubsub_functions : pubsub_function.name => pubsub_function }

  source       = "/tmp/${each.key}.zip"
  content_type = "application/zip"

  # Append to the MD5 checksum of the files's content
  # to force the zip to be updated as soon as a change occurs
  name   = "src-${data.archive_file.pubsub_function_source[each.key].output_sha}.zip"
  bucket = google_storage_bucket.function_bucket.name
}

# Create the Cloud function
resource "google_cloudfunctions_function" "pubsub_function" {
  for_each = { for pubsub_function in var.pubsub_functions : pubsub_function.name => pubsub_function }

  description = each.value.description

  name    = "${var.environment}_${each.key}"
  runtime = each.value.runtime

  # Get the source code of the cloud function as a Zip compression
  source_archive_bucket = google_storage_bucket.function_bucket.name
  source_archive_object = google_storage_bucket_object.pubsub_function_zip[each.key].name

  # Must match the function name in the cloud function `main.py` source code
  entry_point = try(each.value.entry_point, each.key)

  timeout             = coalesce(each.value.timeout, 15)
  available_memory_mb = coalesce(each.value.memory, 256)

  # Trigger
  event_trigger {
    event_type = "google.pubsub.topic.publish"
    resource   = "projects/${var.project_id}/topics/${var.environment}_${each.value.trigger_event}"
  }

  # Instances count
  min_instances = 0
  max_instances = 5

  # Secrets
  dynamic "secret_environment_variables" {
    for_each = each.value.secrets != null ? each.value.secrets : []
    content {
      key     = secret_environment_variables.value
      secret  = secret_environment_variables.value
      version = "latest"
    }
  }

  # Service account
  service_account_email = var.service_account_email
}
