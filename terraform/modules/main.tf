
variable "project_id" {
  default = "archy-f06ed"
}

variable "project_name" {
  default = "archy"
}

variable "region" {
  default = "us-central1"
}

variable "service_account_email" {
  default = "archyapi@archy-f06ed.iam.gserviceaccount.com"
}

variable "environment" {
}

variable "src_dir" {
}

variable "secrets" {
}

variable "http_functions" {
  type = map(any)
}

variable "pubsub_topics" {
  type = list(any)
}

variable "pubsub_functions" {
  type = map(any)
}

# Provider to connect to Google
provider "google" {
  project = var.project_id
  region  = var.region
}
