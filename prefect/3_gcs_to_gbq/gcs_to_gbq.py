import io
import json
import re
import os
import sys
import datetime
import pandas as pd
import pandas_gbq
from pathlib import Path
from prefect import flow, task, get_run_logger
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from prefect.filesystems import GCS
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from google.cloud import storage
from google.cloud import bigquery

home_dir = os.path.expanduser("~")
project_dir = os.path.join(home_dir, "de_zoomcamp_2023_project", "prefect")
sys.path.append(project_dir)
import config as cfg

# project_id = "bright-aloe-381618"


###########################################################################################################################################
@task(name="extractFromGCS", retries=3)
def extract_from_gcs(blob):
    """Download data from GCS"""

    logger = get_run_logger()

    # Extract table name
    input_str = blob.name

    logger.info(
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        f"Extracted {input_str}\n"
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    )

    match = re.search(r'_([^_]+)_', input_str)
    table_name = match.group(1)
    logger.info(
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        f"Table name {table_name}\n"
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    )

    return table_name
###########################################################################################################################################


###########################################################################################################################################
@flow(name="transform", retries=3)
def transform(bucket_name, blob_name, table_name) -> pd.DataFrame:

    logger = get_run_logger()

    logger.info(
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        f"Starting flatten for {blob_name}\n"
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    )

    """Data cleaning example"""
    # Set up the GCS client
    client = storage.Client()

    # Get a handle to the GCS bucket and file
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Download the file contents to a BytesIO object
    bytes_io = io.BytesIO()
    blob.download_to_file(bytes_io)

    # Reset the BytesIO object to the beginning of the stream
    bytes_io.seek(0)

    # Open the BytesIO object in binary mode
    binary_io = io.BufferedReader(bytes_io)

    if table_name == 'districts':

        # Load the contents of the file into a dictionary
        data = json.loads(bytes_io.read().decode())['data']

        # Create a list of DataFrames, one for each ags
        dfs = []
        for ags, values in data.items():
            df = pd.json_normalize(values)
            df['ags'] = ags
            dfs.append(df)

        # Concatenate the DataFrames into a single one
        df = pd.concat(dfs, ignore_index=True)

    else:

        # Load the contents of the file into a Pandas DataFrame
        df = pd.json_normalize(json.loads(bytes_io.read().decode()))

    # Create a mapping dictionary for renaming the columns
    mapping = {col: col.replace('.', '_') for col in df.columns if '.' in col}

    # Use the mapping dictionary to rename the columns
    df = df.rename(columns=mapping)

    logger.info(
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        f"End of transform: DataFrame\n{df}\n"
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    )

    write_bq(df, table_name)
    #return df
###########################################################################################################################################


###########################################################################################################################################
@task(name="writeToBQ", retries=3)
def write_bq(df, table_name) -> None:
    """Write DataFrame to BiqQuery"""

    logger = get_run_logger()

    logger.info(
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        f"Starting to write {table_name} to Google Big Query\n"
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    )

    logger.info(
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        f"DataFrame\n{df}\n transferred\n"
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    )

    # Add column _inserted_at which is filled with the current timestamp
    df["_inserted_at"] = pd.Timestamp.now(tz="Europe/Berlin")

    dataset_id = cfg.configs["dataset_id"] #'de_zoomcamp_2023_project_dataset'
    destination_table = f"{dataset_id}.{table_name}"
    gcp_credentials_block = GcpCredentials.load(cfg.configs["prefect_gcp_credentials_block"])

    # Set up the BigQuery client
    bq_client = bigquery.Client()

    # Check if the table exists
    try:

        table_ref = bq_client.dataset(dataset_id).table(table_name)

        # Check if rows in the DataFrame already exist in the target table
        query = f"SELECT * FROM {destination_table}"
        existing_rows = pandas_gbq.read_gbq(query, project_id=cfg.configs["project_id"], credentials=gcp_credentials_block.get_credentials_from_service_account())

        logger.info(
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            f"Query \n{query}\nreturns\n{existing_rows}\n"
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        )

        logger.info(
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            f"DataFrame\n{df}\n before dropna\n"
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        )

        # Keep only rows in the DataFrame that do not already exist in the target table
        merged_df = pd.merge(df, existing_rows, how='left', indicator=True)
        new_rows_df = merged_df[merged_df['_merge']=='left_only'].drop(['_merge'], axis=1)
        df = new_rows_df.drop_duplicates()

        logger.info(
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            f"DataFrame\n{df}\n after dropna\n"
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        )

        # Remaining rows
        remaining_rows = df.shape[0]

        if remaining_rows == 0:
            logger.info(
                "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
                "No new rows available\n"
                "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            )
        else:
            logger.info(
                "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
                f"{remaining_rows} written\n"
                "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            )

    except:

        logger.info(
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            f"The table {table_name} wasn't existing so far. It's been created.\n"
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        )

    df.to_gbq(
        destination_table=destination_table,
        project_id=cfg.configs["project_id"],
        credentials=gcp_credentials_block.get_credentials_from_service_account(),
        chunksize=500_000,
        if_exists="append",
    )    
###########################################################################################################################################


###########################################################################################################################################
@flow(name="gcs-to-gbq", retries=3)
def etl_gcs_to_bq() -> None:
    """Main ETL flow to load data into Big Query"""

    logger = get_run_logger()

    gcs_bucket = GcsBucket.load(cfg.configs["prefect_gcs_bucket_block"])

    available_blobs = gcs_bucket.list_blobs("")

    logger.info(
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        f"{available_blobs} written\n"
        "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    )

    # Loop through all the files in the bucket
    for blob in gcs_bucket.list_blobs(""):
        table_name = extract_from_gcs(blob)
        df = transform(gcs_bucket.bucket, blob.name, table_name, wait_for=table_name)
###########################################################################################################################################


###########################################################################################################################################
def deploy_flow():
    # DEPLOY_STORE_NAME = "gcs-deployments"
    DEPLOY_STORE_NAME = cfg.configs["DEPLOY_STORE_NAME"]
    storage = GCS.load(DEPLOY_STORE_NAME)
    deployment = Deployment.build_from_flow(
        flow=etl_gcs_to_bq,
        name='gcs2gbq',
        description='Extracts data from GCS bucket in JSON format and writes it to GBQ table',
        version='zoomcamp',
        work_queue_name='default',
        storage=storage,
        tags=["flattenntransfer"],
        schedule=(CronSchedule(cron="0 0 11 * * *", timezone="Europe/Berlin")),
    )
    deployment.apply()
###########################################################################################################################################


if __name__ == "__main__":
    # etl_gcs_to_bq()
    deploy_flow()