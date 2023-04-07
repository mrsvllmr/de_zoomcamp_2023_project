from prefect_gcp import GcpCredentials
from prefect_dbt.cli import BigQueryTargetConfigs, DbtCliProfile
from prefect_gcp.credentials import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp.cloud_storage import cloud_storage_create_bucket
from prefect.filesystems import GCS
import json
import os

# alternative to creating GCP blocks in the UI
# copy your own service_account_info dictionary from the json file you downloaded from google
# IMPORTANT - do not store credentials in a publicly available repository!

########################################################################################################
# GcpCredentials block
########################################################################################################
credentials_block = GcpCredentials(
    service_account_file = "/home/mrsvllmr/.gc/sa-key-file.json"
    #gcp_credentials = GcpCredentials(service_account_file=service_account_file)
    #gcp_credentials = GcpCredentials(service_account_info=service_account_info)
    #bucket = cloud_storage_create_bucket("dezoomcamp-project-source-data", gcp_credentials)
)

credentials_block.save("gcp-credentials", overwrite=True)

########################################################################################################
# GcsBucket block
########################################################################################################
bucket_block = GcsBucket(
    bucket="de-zoomcamp-2023-project-datalake-bucket_bright-aloe-381618",  # insert your GCS bucket name
    gcp_credentials=GcpCredentials.load("gcp-credentials"),
    bucket_folder="data"
)

bucket_block.save("gcs-bucket", overwrite=True)

########################################################################################################
# Gcs block (for saving the deployments)
########################################################################################################
gcs_block = GCS(
    bucket_path="de-zoomcamp-2023-project-datalake-bucket_bright-aloe-381618/deployments/",
    # service_account_info=str(json.load(open(os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))))
)

gcs_block.save("gcs-deployments", overwrite=True)

########################################################################################################
# BigQueryTargetConfigs block
########################################################################################################
credentials = GcpCredentials.load("gcp-credentials")
target_configs = BigQueryTargetConfigs(
    schema="de_zoomcamp_2023_project_dataset",
    credentials=credentials,
)

target_configs.save("bgtc", overwrite=True)

########################################################################################################
# DbtCliProfile block
########################################################################################################
dbt_cli_profile = DbtCliProfile(
    name="dez-dbt-cli-profile",
    target="dev",
    target_configs=target_configs,
)
dbt_cli_profile.save("dez-dbt-cli-profile", overwrite=True)


# if __name__ == '__main__':
#     gcp_auth()