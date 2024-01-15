
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
  type = list(object({
    name        = string
    description = string
    runtime     = string
    entry_point = string
    timeout     = optional(string)
    memory      = optional(string)
    secrets     = optional(list(string))
  }))
  default = [{
    name        = "describe"
    description = "Describe a user"
    runtime     = "python39"
    entry_point = "describe"
    }, {
    name        = "exam"
    description = "Get exam information"
    runtime     = "python39"
    entry_point = "exam"
    }, {
    name        = "hello"
    description = "Template of a function in Python"
    runtime     = "python39"
    entry_point = "hello"
    }, {
    name        = "java"
    description = "Template of a function in Java"
    runtime     = "java17"
    entry_point = "functions.Java"
    }, {
    name        = "js"
    description = "Template of a function in Javascript"
    runtime     = "nodejs18"
    entry_point = "js"
    secrets     = ["DISCORD_TOKEN"]
    }, {
    name        = "level"
    description = "Return the level of a user using the NextJS function"
    runtime     = "go121"
    entry_point = "Level"
    }, {
    name        = "froge"
    description = "Return a random froge from the server"
    runtime     = "go121"
    entry_point = "SendRandomFroge"
    secrets     = ["DISCORD_TOKEN"]
    }, {
    name        = "gif"
    description = "Return the requested gif"
    runtime     = "python39"
    entry_point = "gif"
    secrets     = ["DISCORD_TOKEN", "TENOR_API_TOKEN"]
    }, {
    name        = "http"
    description = "Return an image describing the given http code"
    runtime     = "python39"
    entry_point = "http"
    }, {
    name        = "video"
    description = "Return the requested youtube video"
    runtime     = "python39"
    entry_point = "video"
    secrets     = ["YOUTUBE_API_TOKEN"]
    }, {
    name        = "go"
    description = "Template of a function in Golang"
    runtime     = "go121"
    entry_point = "SendMessage"
    }, {
    name        = "ban"
    description = "Admin only: Ban a user"
    runtime     = "go121"
    entry_point = "BanUser"
    secrets     = ["DISCORD_TOKEN"]
    }, {
    name        = "help"
    description = "Describe all active commands"
    runtime     = "python39"
    entry_point = "help"
    }, {
    name        = "leaderboard"
    description = "Return the leaderboard of the server"
    runtime     = "go121"
    entry_point = "GetLeaderboardUrl"
    }, {
    name        = "warn"
    description = "Admin only: Warn a user and take action if needed"
    runtime     = "go121"
    entry_point = "WarnUser"
    secrets     = ["DISCORD_TOKEN"]
    }, {
    name        = "listwarn"
    description = "Admin only: List all warn of that server"
    runtime     = "go121"
    entry_point = "ListWarn"
    secrets     = ["DISCORD_TOKEN"]
    }, {
    name        = "answer"
    description = "Return a random answer based on the game '8 Ball'"
    runtime     = "go121"
    entry_point = "Answer"
    }, {
    name        = "flag"
    description = "Return a flag"
    runtime     = "python39"
    entry_point = "flag"
    }, {
    name        = "src"
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
  type = list(object({
    name          = string
    description   = string
    runtime       = string
    entry_point   = string
    trigger_event = string
    timeout       = optional(string)
    memory        = optional(string)
    secrets       = optional(list(string))
  }))
  default = [
    {
      name          = "exp"
      description   = "Increase the experience of a user"
      runtime       = "go121"
      entry_point   = "Exp"
      trigger_event = "exp_discord"
      }, {
      name          = "privateMessage"
      description   = "Send a private message to a user"
      runtime       = "go121"
      entry_point   = "PrivateMessage"
      trigger_event = "private_message_discord"
      secrets       = ["DISCORD_TOKEN"]
      }, {
      name          = "frogeOfTheDay"
      description   = "Publish the froge of the day"
      runtime       = "python39"
      entry_point   = "publish_froge_of_the_day"
      trigger_event = "froge_of_the_day"
      secrets       = ["DISCORD_TOKEN"]
      }, {
      name          = "channelMessage"
      description   = "Send a message to a channel"
      runtime       = "go121"
      entry_point   = "ChannelMessage"
      trigger_event = "channel_message_discord"
      secrets       = ["DISCORD_TOKEN"]
      }, {
      name          = "cloudDeploymentLog"
      description   = "Send the Google Cloud deployment log from pubsub to a specific channel"
      runtime       = "go121"
      entry_point   = "UnmarshalPubsubMessage"
      trigger_event = "cloud_function_crud_log"
      secrets       = ["DISCORD_TOKEN"]
      }, {
      name          = "cloudErrorLog"
      description   = "Send the Google Cloud error log from pubsub to a specific channel"
      runtime       = "go121"
      entry_point   = "UnmarshalPubsubMessage"
      trigger_event = "cloud_function_error_log"
      secrets       = ["DISCORD_TOKEN"]
      }, {
      name          = "updateUserRole"
      description   = "Add roles to a user based on his level"
      runtime       = "go121"
      entry_point   = "UserRole"
      trigger_event = "update_user_role"
      secrets       = ["DISCORD_TOKEN"]
      }, {
      name          = "generateWelcomeImage"
      description   = "Generate the Welcome image of a user"
      runtime       = "nodejs18"
      entry_point   = "generateWelcomeImage"
      timeout       = 15
      memory        = 1024
      trigger_event = "generate_welcome_image"
      }, {
      name          = "stm"
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
