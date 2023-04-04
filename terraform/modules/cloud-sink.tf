resource "google_logging_project_sink" "cloud_function_error_sink" {
  name        = "archy-cloud-function-error-${var.environment}"
  description = "Cloud sink for function error in ${var.environment}"

  destination = "pubsub.googleapis.com/projects/${var.project_id}/topics/${var.environment}_cloud_function_error_log"

  filter = "resource.type=\"cloud_function\" AND resource.labels.project_id=\"${var.project_id}\" AND severity=(ERROR OR CRITICAL OR ALERT OR EMERGENCY) AND resource.labels.function_name:\"${var.environment}_\""

  unique_writer_identity = false
}

resource "google_logging_project_sink" "cloud_function_crud_sing" {
  name        = "archy-cloud-function-crud-${var.environment}"
  description = "Cloud sink for function deployment in ${var.environment}"

  destination = "pubsub.googleapis.com/projects/${var.project_id}/topics/${var.environment}_cloud_function_crud_log"

  filter = "resource.type=\"cloud_function\" AND resource.labels.project_id=\"${var.project_id}\" AND protoPayload.methodName=\"google.cloud.functions.v1.CloudFunctionsService.CreateFunction\" OR protoPayload.methodName=\"google.cloud.functions.v1.CloudFunctionsService.UpdateFunction\""

  unique_writer_identity = false
}
