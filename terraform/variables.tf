locals {
  data_lake_bucket = "de-zoomcamp-2023-project-datalake-bucket"
}

variable "project" {
  description = "Final dezoomcamp project, cohort 2023, by mrsvllmr" # adjust accordingly!
  default = "bright-aloe-381618" # adjust accordingly!
  type = string
}

variable "gce_ssh_user" {
  default = "mrsvllmr"
}

variable "gce_ssh_pub_key_file" {
  default = "C:/Users/mariu/.ssh/ssh_key.pub" # adjust accordingly!
}

variable "gce_ssh_priv_key_file" {
  default = "C:/Users/mariu/.ssh/ssh_key" # adjust accordingly!
}

variable "region" {
  description = "Region for GCP resources"
  default="EUROPE-WEST1" 
  type = string
}

variable "storage_class" {
  description = "Storage class type for your bucket"
  default = "STANDARD"
}

variable "BQ_DATASET" {
  description = "BigQuery Dataset that raw data (from GCS) will be written to"
  type = string
  default = "de_zoomcamp_2023_project_dataset"
}

variable "instance" {
  type = string
  default = "de-zoomcamp-2023-project-vm-sshtest"
}

variable "machine_type" {
  type = string
  default = "e2-standard-4"
}

variable "zone" {
  description = "Region for VM"
  type = string
  default = "europe-west1-b"
}

variable "gcp_service_list" {
  type        = list(string)
  description = "The list of apis necessary for the project"
  default     = ["iam.googleapis.com","iamcredentials.googleapis.com"]
}

variable "roles" {
  type        = list(string)
  description = "The roles that will be granted to the service account."
  default     = ["roles/owner","roles/storage.admin","roles/storage.objectAdmin","roles/bigquery.admin"]
}

variable "github_pat" {
  type        = string
  default     = "C:/Users/mariu/.github/pat" # adjust accordingly!
}