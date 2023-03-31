resource "google_service_account" "de-zoomcamp-2023-project-sa-id" {
  project = var.project
  account_id   = "de-zoomcamp-2023-project-sa-id"
  display_name = "sa_terraform"

  depends_on = [
    google_project_service.enabled_apis,
  ]
}

resource "google_project_iam_member" "sa_iam" {
  for_each = toset(var.roles)

  project = var.project
  role    = each.value
  member  = "serviceAccount:${google_service_account.de-zoomcamp-2023-project-sa-id.email}"

  depends_on = [
    google_project_service.enabled_apis,
  ]
}