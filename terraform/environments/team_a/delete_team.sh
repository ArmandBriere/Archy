#!/bin/bash
team_letter=$1

terraform init

terraform state rm module.team_${team_letter}.google_compute_instance.default projects/archy-f06ed/zones/us-central1-a/instances/e2-micro-archy
terraform state rm module.team_${team_letter}.google_secret_manager_secret.secret-basic\[\"TENOR_API_TOKEN\"\] projects/archy-f06ed/secrets/TENOR_API_TOKEN
terraform state rm module.team_${team_letter}.google_secret_manager_secret.secret-basic\[\"DISCORD_TOKEN\"\] projects/archy-f06ed/secrets/DISCORD_TOKEN
terraform state rm module.team_${team_letter}.google_secret_manager_secret.secret-basic\[\"YOUTUBE_API_TOKEN\"\] projects/archy-f06ed/secrets/YOUTUBE_API_TOKEN

terraform destroy
