
resource "google_secret_manager_secret" "secret" {
  for_each = toset(var.secrets)

  project   = var.project_id
  secret_id = each.value

  replication {
    auto {}
  }
}
