terraform {
  backend "gcs" {
    bucket = "archy-tf-state-prod"
    prefix = "terraform/state"
  }
}