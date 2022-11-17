terraform {
  backend "gcs" {
    bucket = "archy-tf-state-team-a"
    prefix = "terraform/state"
  }
}
