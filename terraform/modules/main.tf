
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
  type    = string
  default = "../../../src"
}

variable "secrets" {
  type = list(string)
  default = [
    "DISCORD_TOKEN",
    "TENOR_API_TOKEN",
    "YOUTUBE_API_TOKEN",
    "STM_API_KEY"
  ]
}

variable "http_functions" {
  type = list(object())
  default = [{
    description = "Describe a user"
    runtime     = "python39"
    entry_point = "describe"
    }, {
    description = "Get exam information"
    runtime     = "python39"
    entry_point = "exam"
    }, {
    description = "Template of a function in Python"
    runtime     = "python39"
    entry_point = "hello"
    }, {
    description = "Template of a function in Java"
    runtime     = "java17"
    entry_point = "functions.Java"
    }, {
    description = "Template of a function in Javascript"
    runtime     = "nodejs18"
    entry_point = "js"
    secrets     = ["DISCORD_TOKEN"]
    }, {
    description = "Return the level of a user using the NextJS function"
    runtime     = "go121"
    entry_point = "Level"
    }, {
    description = "Return a random froge from the server"
    runtime     = "go121"
    entry_point = "SendRandomFroge"
    secrets     = ["DISCORD_TOKEN"]
    }, {
    description = "Return the requested gif"
    runtime     = "python39"
    entry_point = "gif"
    secrets     = ["DISCORD_TOKEN", "TENOR_API_TOKEN"]
    }, {
    description = "Return an image describing the given http code"
    runtime     = "python39"
    entry_point = "http"
    }, {
    description = "Return the requested youtube video"
    runtime     = "python39"
    entry_point = "video"
    secrets     = ["YOUTUBE_API_TOKEN"]
    }, {
    description = "Template of a function in Golang"
    runtime     = "go121"
    entry_point = "SendMessage"
    }, {
    description = "Admin only: Ban a user"
    runtime     = "go121"
    entry_point = "BanUser"
    secrets     = ["DISCORD_TOKEN"]
    }, {
    description = "Describe all active commands"
    runtime     = "python39"
    entry_point = "help"
    }, {
    description = "Return the leaderboard of the server"
    runtime     = "go121"
    entry_point = "GetLeaderboardUrl"
    }, {
    description = "Admin only: Warn a user and take action if needed"
    runtime     = "go121"
    entry_point = "WarnUser"
    secrets     = ["DISCORD_TOKEN"]
    }, {
    description = "Admin only: List all warn of that server"
    runtime     = "go121"
    entry_point = "ListWarn"
    secrets     = ["DISCORD_TOKEN"]
    }, {
    description = "Return a random answer based on the game '8 Ball'"
    runtime     = "go121"
    entry_point = "Answer"
    }, {
    description = "Return a flag"
    runtime     = "python39"
    entry_point = "flag"
    }, {
    description = "Return the github url of my source code"
    runtime     = "python39"
    entry_point = "sourcecode"
    },
  ]
}

variable "pubsub_topics" {
  type = list(string)
  default = [
    "channel_message_discord",
    "cloud_function_crud_log",
    "cloud_function_error_log",
    "froge_of_the_day",
    "private_message_discord",
    "update_user_role",
    "exp_discord",
    "generate_welcome_image",
    "stm_status"
  ]
}

variable "pubsub_functions" {
  type = list(object())
  default = [
    {
      description   = "Increase the experience of a user"
      runtime       = "go121"
      entry_point   = "Exp"
      trigger_event = "exp_discord"
      }, {
      description   = "Send a private message to a user"
      runtime       = "go121"
      entry_point   = "PrivateMessage"
      trigger_event = "private_message_discord"
      secrets       = ["DISCORD_TOKEN"]
      }, {
      description   = "Publish the froge of the day"
      runtime       = "python39"
      entry_point   = "publish_froge_of_the_day"
      trigger_event = "froge_of_the_day"
      secrets       = ["DISCORD_TOKEN"]
      }, {
      description   = "Send a message to a channel"
      runtime       = "go121"
      entry_point   = "ChannelMessage"
      trigger_event = "channel_message_discord"
      secrets       = ["DISCORD_TOKEN"]
      }, {
      description   = "Send the Google Cloud deployment log from pubsub to a specific channel"
      runtime       = "go121"
      entry_point   = "UnmarshalPubsubMessage"
      trigger_event = "cloud_function_crud_log"
      secrets       = ["DISCORD_TOKEN"]
      }, {
      description   = "Send the Google Cloud error log from pubsub to a specific channel"
      runtime       = "go121"
      entry_point   = "UnmarshalPubsubMessage"
      trigger_event = "cloud_function_error_log"
      secrets       = ["DISCORD_TOKEN"]
      }, {
      description   = "Add roles to a user based on his level"
      runtime       = "go121"
      entry_point   = "UserRole"
      trigger_event = "update_user_role"
      secrets       = ["DISCORD_TOKEN"]
      }, {
      description   = "Generate the Welcome image of a user"
      runtime       = "nodejs18"
      entry_point   = "generateWelcomeImage"
      timeout       = 15
      memory        = 1024
      trigger_event = "generate_welcome_image"
      }, {
      description   = "Check metro and bus line status with official STM api"
      runtime       = "go121"
      entry_point   = "CheckStmStatus"
      trigger_event = "stm_status"
      secrets       = ["STM_API_KEY"]
    },
  ]
}

# Provider to connect to Google
provider "google" {
  project = var.project_id
  region  = var.region
}
