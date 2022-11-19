resource "google_logging_project_sink" "cloud_function_sink" {
  name        = "archy-cloud-error-${var.environment}"
  description = "Cloud sink for the ${var.environment} environment"

  destination = "pubsub.googleapis.com/projects/${var.project_id}/topics/${var.environment}_cloud_function_error_log"

  filter = "resource.type=\"cloud_function\" AND resource.labels.project_id=\"${var.project_id}\" AND severity=(ERROR OR CRITICAL OR ALERT OR EMERGENCY) AND resource.labels.function_name:\"${var.environment}_\""

  unique_writer_identity = false
}
