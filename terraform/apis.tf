locals {
  all_project_services = concat(var.gcp_service_list, [
    "serviceusage.googleapis.com",
    "iam.googleapis.com",
  ])
}

resource "google_project_service" "enabled_apis" {
  project  = var.project
  for_each = toset(local.all_project_services)
  service  = each.key

  disable_on_destroy = false
}