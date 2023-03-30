locals {
  data_lake_bucket = "de-zoomcamp-2023-project-datalake-bucket"
}

variable "project" {
  description = "Final dezoomcamp project, cohort 2023, by Marius Vollmer"
  default = "bright-aloe-381618"
  type = string
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
  default = "de-zoomcamp-2023-project-vm"
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