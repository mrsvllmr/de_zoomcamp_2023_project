#!/bin/bash

if [ -z "$PROJECT_ID" ]
  then
    echo "Project ID environment variable missing"
    exit 1
fi


# create service account for Terraform in GCP
gcloud iam service-accounts create sa-terraform-iam --display-name "sa-terraform-iam" 

# create roles for service account (as set in the project, but with owner role to get full control)
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:sa-terraform-iam@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/owner"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:sa-terraform-iam@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/storage.admin"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:sa-terraform-iam@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/storage.objectAdmin"
gcloud projects add-iam-policy-binding $PROJECT_ID --member="serviceAccount:sa-terraform-iam@$PROJECT_ID.iam.gserviceaccount.com" --role="roles/bigquery.admin"

# save json key
mkdir .gc
gcloud iam service-accounts keys create ../.gc/sa-terraform-iam.json --iam-account=sa-terraform-iam@$PROJECT_ID.iam.gserviceaccount.com

# set the path to json to interact with GCP from local machine
export GOOGLE_APPLICATION_CREDENTIALS="../.gc/sa-terraform-iam.json"