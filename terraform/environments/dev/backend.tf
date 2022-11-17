terraform {
  backend "gcs" {
    bucket = "archy-tf-state-dev"
    prefix = "terraform/state"
  }
}
