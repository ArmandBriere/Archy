
# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "source" {
    type        = "zip"
    source_dir  = "../src/functions/hello"
    output_path = "/tmp/hello.zip"
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "zip" {
    source       = data.archive_file.source.output_path
    content_type = "application/zip"

    # Append to the MD5 checksum of the files's content
    # to force the zip to be updated as soon as a change occurs
    name         = "src-${data.archive_file.source.output_md5}.zip"
    bucket       = google_storage_bucket.function_bucket.name
}

# Create the Cloud function
resource "google_cloudfunctions_function" "function" {
    description = "Hello function deployed from Terraform"

    name    = "helloFromTf"
    runtime = "python39"

    # Get the source code of the cloud function as a Zip compression
    source_archive_bucket = google_storage_bucket.function_bucket.name
    source_archive_object = google_storage_bucket_object.zip.name

    # Must match the function name in the cloud function `main.py` source code
    entry_point = "hello"

    # Timeout
    timeout = 15
    
    # Trigger
    trigger_http = true

    # Instances count
    min_instances = 0
    max_instances = 5

    # Service account
    service_account_email = var.service_account_email
}