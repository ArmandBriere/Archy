resource "google_pubsub_topic" "pubsub_topic" {
  for_each = toset(var.pubsub_topics)

  name    = each.value
  project = var.project_id
}
