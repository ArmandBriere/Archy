resource "google_cloud_scheduler_job" "froge_of_the_day_scheduler" {
  name        = "${var.environment}_froge_of_the_day"
  description = "Trigger the Froge of the day"
  schedule    = "0 12 * * *"
  time_zone   = "America/Toronto"


  pubsub_target {
    topic_name = "projects/${var.project_id}/topics/${var.environment}_froge_of_the_day"
    data       = base64encode("froge_of_the_day")
  }
}
