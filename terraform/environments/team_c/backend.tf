terraform {
  backend "gcs" {
    bucket = "archy-tf-state-team-c"
    prefix = "terraform/state"
  }
}
