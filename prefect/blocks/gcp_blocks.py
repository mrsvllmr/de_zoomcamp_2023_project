from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from prefect_gcp.cloud_storage import cloud_storage_create_bucket
from prefect.filesystems import GCS
from prefect.blocks.system import JSON

# alternative to creating GCP blocks in the UI
# copy your own service_account_info dictionary from the json file you downloaded from google
# IMPORTANT - do not store credentials in a publicly available repository!

########################################################################################################
# GcpCredentials block
########################################################################################################
credentials_block = GcpCredentials(
    #service_account_info={}  # enter your credentials from the json file
    gcp_credentials = GcpCredentials(service_account_file="/home/mrsvllmr/.gc/sa-key-file.json")
    # bucket = cloud_storage_create_bucket("dezoomcamp-project-source-data", gcp_credentials)
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
json_block = JSON.load("sa-json")

gcs_block = GCS(
    bucket_path="de-zoomcamp-2023-project-datalake-bucket_bright-aloe-381618/deployments/",
    service_account_info=str(json_block)
)

gcs_block.save("gcs-deployments", overwrite=True)


# if __name__ == '__main__':
#     gcp_auth()