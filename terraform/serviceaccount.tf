################################################################################################################################################
# Create a service account
################################################################################################################################################
resource "google_service_account" "de-zoomcamp-2023-project-sa-id" {
  project = var.project
  account_id   = "de-zoomcamp-2023-project-sa-id"
  display_name = "sa_terraform"

  depends_on = [
    google_project_service.enabled_apis,
  ]
}

################################################################################################################################################
# Create a service account key and save it to a file
################################################################################################################################################
resource "google_service_account_key" "de-zoomcamp-2023-project-sa-key" {
  service_account_id = google_service_account.de-zoomcamp-2023-project-sa-id.id
  private_key_type   = "TYPE_GOOGLE_CREDENTIALS_FILE"
  depends_on         = [google_service_account.de-zoomcamp-2023-project-sa-id]
}

resource "google_project_iam_member" "sa_iam" {
  for_each = toset(var.roles)

  project = var.project
  role    = each.value
  member  = "serviceAccount:${google_service_account.de-zoomcamp-2023-project-sa-id.email}" # notice: inner part has to fit the account_id above

  depends_on = [
    google_project_service.enabled_apis,
  ]
}