
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
    "TENOR_API_TOKEN",
  ]
}

variable "http_functions" {
  type = map(any)
  default = {
    describe : {
      description = "Describe a user"
      runtime     = "python39"
      entry_point = "describe"
      timeout     = 15
      memory      = 256
      secrets     = []
    },
    exp : {
      description = "Increase the experience of a user"
      runtime     = "python39"
      entry_point = "exp"
      timeout     = 15
      memory      = 256
      secrets     = ["DISCORD_TOKEN"]
    },
    hello : {
      description = "Simple hello"
      runtime     = "python39"
      entry_point = "hello"
      timeout     = 15
      memory      = 256
      secrets     = []
    },
    js : {
      description = "Template of a function in javascript"
      runtime     = "nodejs16"
      entry_point = "js"
      timeout     = 15
      memory      = 256
      secrets     = ["DISCORD_TOKEN"]
    },
    level : {
      description = "Return the level of a user"
      runtime     = "python39"
      entry_point = "level"
      timeout     = 15
      memory      = 256
      secrets     = ["DISCORD_TOKEN"]
    }
    froge : {
      description = "Return a random froge from the server"
      runtime     = "go116"
      entry_point = "SendRandomFroge"
      timeout     = 15
      memory      = 256
      secrets     = ["DISCORD_TOKEN"]
    }
    gif : {
      description = "Return the requested gif"
      runtime     = "python39"
      entry_point = "gif"
      timeout     = 15
      memory      = 256
      secrets     = ["DISCORD_TOKEN", "TENOR_API_TOKEN"]
    }
    go : {
      description = "Template of a function in Golang"
      runtime     = "go116"
      entry_point = "SendMessageWithReaction"
      timeout     = 15
      memory      = 256
      secrets     = ["DISCORD_TOKEN"]
    },
    ban : {
      description = "Admin only: Ban a user"
      runtime     = "go116"
      entry_point = "BanUser"
      timeout     = 15
      memory      = 256
      secrets     = ["DISCORD_TOKEN"]
    }
    help : {
      description = "Describe all active command."
      runtime     = "python39"
      entry_point = "help"
      timeout     = 15
      memory      = 256
      secrets     = []
    },
    leaderboard : {
      description = "Return the current server leaderboard url."
      runtime     = "go116"
      entry_point = "SendLeaderboardUrl"
      timeout     = 15
      memory      = 256
      secrets     = []
    },
  }
}


variable "pubsub_topics" {
  type = list(any)
  default = [
    "channel_message_discord",
    "cloud_function_error_log",
    "froge_of_the_day",
    "private_message_discord",
  ]
}

variable "pubsub_functions" {
  type = map(any)
  default = {
    privateMessage : {
      description   = "Send a private message to a user"
      runtime       = "go116"
      entry_point   = "PrivateMessage"
      timeout       = 15
      memory        = 256
      trigger_event = "private_message_discord"
      secrets       = ["DISCORD_TOKEN"]
    },
    frogeOfTheDay : {
      description   = "Publish the froge of the day"
      runtime       = "python39"
      entry_point   = "publish_froge_of_the_day"
      timeout       = 15
      memory        = 256
      trigger_event = "froge_of_the_day"
      secrets       = ["DISCORD_TOKEN"]
    },
    channelMessage : {
      description   = "Send a message to a channel"
      runtime       = "go116"
      entry_point   = "ChannelMessage"
      timeout       = 15
      memory        = 256
      trigger_event = "channel_message_discord"
      secrets       = ["DISCORD_TOKEN"]
    },
    cloudErrorLog : {
      description   = "Send the Google Cloud error log from pubsub to a specific channel"
      runtime       = "go116"
      entry_point   = "UnmarshalPubsubMessage"
      timeout       = 15
      memory        = 256
      trigger_event = "cloud_function_error_log"
      secrets       = ["DISCORD_TOKEN"]
    },
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
