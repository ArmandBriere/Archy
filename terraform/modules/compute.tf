locals {
  container_image = "cos-stable-97-16919-29-21"
  resource_name   = "e2-micro-archy"
}

resource "google_compute_instance" "default" {
  name         = local.resource_name
  machine_type = "e2-micro"
  zone         = "us-central1-a"

  metadata = {
    "google-logging-enabled"    = true
    "google-monitoring-enabled" = true
    "gce-container-declaration" = <<-EOT
        # DISCLAIMER:
        # This container declaration format is not a public API and may change without
        # notice. Please use gcloud command-line tool or Google Cloud Console to run
        # Containers on Google Compute Engine.

        spec:
          containers:
          - image: us.gcr.io/archy-f06ed/archy-prod
            name: archy-prod
            stdin: false
            tty: false
            volumeMounts: []
          restartPolicy: Always
          volumes: []
    EOT
  }

  boot_disk {
    auto_delete = true
    device_name = local.resource_name
    mode        = "READ_WRITE"

    initialize_params {
      image = "https://www.googleapis.com/compute/v1/projects/cos-cloud/global/images/${local.container_image}"
      size  = 10
      type  = "pd-standard"
    }
  }

  labels = {
    "container-vm" = local.container_image
  }

  network_interface {
    network = "default"
    access_config {
      network_tier = "PREMIUM"
    }
  }

  service_account {
    email = var.service_account_email
    scopes = [
      "cloud-platform"
    ]
  }

  allow_stopping_for_update = true
}
