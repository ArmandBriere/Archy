terraform {
  backend "gcs" {
    bucket = "archy-tf-state-team-b"
    prefix = "terraform/state"
  }
}
