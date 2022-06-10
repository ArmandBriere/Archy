
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

variable "secrets" {
  type = list(any)
  default = [
    "DISCORD_TOKEN",
    "GOOGLE_APPLICATION_CREDENTIALS"
  ]
}

variable "python_functions" {
  type = map(any)
  default = {
    describe : {
      description = "Describe a user"
      runtime     = "python39"
      timeout     = 15
      memory      = 256
    },
    exp : {
      description = "Increase the experience of a user"
      runtime     = "python39"
      timeout     = 15
      memory      = 256
    },
    hello : {
      description = "Simple hello"
      runtime     = "python39"
      timeout     = 15
      memory      = 256
    },
    js : {
      description = "Template of a function in javascript"
      runtime     = "nodejs16"
      timeout     = 15
      memory      = 256
    },
    level : {
      description = "Return the level of a user"
      runtime     = "python39"
      timeout     = 15
      memory      = 256
    }
    froge : {
      description = "Return a random froge from the server"
      runtime     = "nodejs16"
      timeout     = 15
      memory      = 512
    }
    gif : {
      description = "Return the requested gif"
      runtime     = "python39"
      timeout     = 15
      memory      = 256
    }
  }
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
