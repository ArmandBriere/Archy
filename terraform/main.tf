
variable "project_id" {
    default = "archy-f06ed"
}

variable "region" {
    default = "us-central1"
}

variable "service_account_email" {
    default = "archy-f06ed@appspot.gserviceaccount.com"
}

# Provider to connect to Google
provider "google" {
    project = var.project_id
    region  = var.region
}

# Bucket to store the function code
resource "google_storage_bucket" "function_bucket" {
    name     = "${var.project_id}-function"
    location = var.region
}

resource "google_storage_bucket" "input_bucket" {
    name     = "${var.project_id}-input"
    location = var.region
}