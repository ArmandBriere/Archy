resource "google_secret_manager_secret" "secret-basic" {
    for_each = toset(var.secrets)
    
    secret_id = "${each.value}"
    project = var.project_id

    replication {
        automatic = true
    }
}