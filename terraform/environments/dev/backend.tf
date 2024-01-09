terraform {
  required_version = ">= 0.12"
  backend "gcs" {
    bucket = "archy-tf-state-dev"
    prefix = "terraform/state"
  }
}
