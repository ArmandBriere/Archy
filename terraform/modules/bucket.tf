resource "google_storage_bucket" "froge" {
  name                     = "froge-bucket-${var.environment}"
  location                 = var.region
  storage_class            = "STANDARD"
  public_access_prevention = "enforced"
}

resource "google_storage_bucket" "function_bucket" {
  name          = "${var.project_id}-function-${var.environment}"
  location      = var.region
  storage_class = "STANDARD"
}
