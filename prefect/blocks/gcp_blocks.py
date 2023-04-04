from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import cloud_storage_create_bucket

# alternative to creating GCP blocks in the UI
# copy your own service_account_info dictionary from the json file you downloaded from google
# IMPORTANT - do not store credentials in a publicly available repository!

# def gcp_auth():
credentials_block = GcpCredentials(
    #service_account_info={}  # enter your credentials from the json file
    gcp_credentials = GcpCredentials(service_account_file="/home/mrsvllmr/.gc/sa_key_file.json")
    # bucket = cloud_storage_create_bucket("dezoomcamp-project-source-data", gcp_credentials)
)
credentials_block.save("gcp-creds", overwrite=True)


bucket_block = GcsBucket(
    gcp_credentials=GcpCredentials.load("gcp-creds"),
    bucket="de-zoomcamp-source-bucket",  # insert your GCS bucket name
)

bucket_block.save("gcs", overwrite=True)


# if __name__ == '__main__':
#     gcp_auth()