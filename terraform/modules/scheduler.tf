resource "google_cloud_scheduler_job" "froge_of_the_day_scheduler" {
  count = var.environment == "prod" ? 1 : 0

  name        = "froge_of_the_day"
  description = "Trigger the Froge of the day"
  schedule    = "0 12 * * *"
  time_zone   = "America/Toronto"


  pubsub_target {
    topic_name = "projects/${var.project_id}/topics/prod_froge_of_the_day"
    data       = base64encode("froge_of_the_day")
  }
}


resource "google_cloud_scheduler_job" "stm_status_scheduler" {
  count = var.environment == "prod" ? 1 : 0

  name        = "stm_status"
  description = "Trigger the stm status check"
  schedule    = "*/5 * * * *"
  time_zone   = "America/Toronto"


  pubsub_target {
    topic_name = "projects/${var.project_id}/topics/prod_stm_status"
    data       = base64encode("prod_stm_status")
  }
}
