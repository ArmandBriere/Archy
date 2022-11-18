resource "google_storage_bucket_access_control" "public_rule" {
  bucket = google_storage_bucket.froge.name
  role   = "READER"
  entity = "allUsers"
}

resource "google_storage_bucket" "froge" {
  name          = "froge-public-bucket-${var.environment}"
  location      = var.region
  storage_class = "STANDARD"
}

resource "google_storage_bucket" "function_bucket" {
  name     = "${var.project_id}-function-${var.environment}"
  location = var.region
  storage_class = "STANDARD"
}
