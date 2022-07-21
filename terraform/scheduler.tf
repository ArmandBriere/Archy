resource "google_cloud_scheduler_job" "froge_of_the_day_scheduler" {
  name        = "froge_of_the_day"
  description = "Trigger the Froge of the day"
  schedule    = "0 12 * * *"
  time_zone   = "America/Toronto"


  pubsub_target {
    topic_name = "froge_of_the_day"
  }
}
