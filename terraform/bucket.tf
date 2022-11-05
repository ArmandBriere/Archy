resource "google_storage_bucket_access_control" "public_rule" {
  bucket = google_storage_bucket.froge.name
  role   = "READER"
  entity = "allUsers"
}

resource "google_storage_bucket" "froge" {
  name          = "froge-public-bucket"
  location      = var.region
  storage_class = "STANDARD"
}
