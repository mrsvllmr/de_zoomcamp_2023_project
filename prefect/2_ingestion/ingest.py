import requests
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import json
import os
import io
import sys
import datetime
import logging
import gcsfs
from google.cloud import storage
from prefect import flow, task, get_run_logger
from prefect_gcp.cloud_storage import GcsBucket
from prefect.filesystems import GCS
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule

home_dir = os.path.expanduser("~")
project_dir = os.path.join(home_dir, "de_zoomcamp_2023_project", "prefect")
sys.path.append(project_dir)
import config as cfg


###########################################################################################################################################
@task(retries=3)
def fetch(url: str) -> dict:
    """Extract RKI data"""
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data

    else:
        raise ValueError("Error retrieving data from API")
###########################################################################################################################################


###########################################################################################################################################
@task(retries=3)
def write_json_to_gcs(data: dict, topic: str) -> None:
    """Save data to GCS in JSON format"""
    # Convert the data to a JSON string
    json_data = json.dumps(data)

    # Define file/object name
    filename = f"ingest_{topic}_{datetime.datetime.now().strftime('%Y%m%d')}.json"
    object_name = f'{filename}'

    # Create a file-like object that contains the JSON string
    # shoutout to https://www.skytowner.com/explore/how_to_solve_the_error_attributeerror_str_object_has_no_attribute_tell_when_uploading_files_on_google_cloud_storage_in_python
    file_obj = io.StringIO(json_data)

    # Upload the file to GCS
    gcs_block = GcsBucket.load(cfg.configs["prefect_gcs_bucket_block"])
    gcs_block.upload_from_file_object(file_obj, object_name, content_type='application/json')
    return
###########################################################################################################################################


###########################################################################################################################################
@flow()
def rki_to_gcs() -> None:
    """Main flow responsible for extracting the data from the RKI api and writing them to GCS bucket"""

    # activate logger in order to print manual/custom logs to Prefect flow logs
    logger = get_run_logger()

    # API endpoints
    endpoints = {
        "germany": "https://api.corona-zahlen.org/germany",
        "districts": "https://api.corona-zahlen.org/districts",
        "hochsauerlandkreis": "https://api.corona-zahlen.org/districts/05958"
    }

    for key, value in endpoints.items():

        # Extract data from API
        logger.info(
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            f"Starting to extract the data from {value}\n"
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            )
        data_dict = fetch(value)
        logger.info(
            f"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            "Extracting of data completed\n"
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            )

        # Write data to GCS
        logger.info(
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            f"Starting to write json data to GCS bucket {value}\n"
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        )
        write_json_to_gcs(data_dict, key, wait_for=data_dict)
        logger.info(
            f"+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
            "Writing to GCS bucket completed\n"
            "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
    )
###########################################################################################################################################


###########################################################################################################################################
def deploy_flow():
    DEPLOY_STORE_NAME = cfg.configs["DEPLOY_STORE_NAME"]
    storage = GCS.load(DEPLOY_STORE_NAME)
    deployment = Deployment.build_from_flow(
        flow=rki_to_gcs,
        name='rki2gcs',
        description='Extracts data from RKI API in JSON format and writes them to the GCS bucket in JSON format',
        version='zoomcamp',
        work_queue_name='default',
        storage=storage,
        tags=["ingest"],
        schedule=(CronSchedule(cron="0 0 10 * * *", timezone="Europe/Berlin")),
    )
    deployment.apply()
###########################################################################################################################################


if __name__ == "__main__":
    # rki_to_gcs()
    deploy_flow()