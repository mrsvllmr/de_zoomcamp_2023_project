import os
import sys
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket
from prefect.filesystems import GCS
from prefect.deployments import Deployment
from prefect import flow, task, get_run_logger
from prefect_dbt.cli.commands import trigger_dbt_cli_command
from prefect_dbt.cli.commands import DbtCoreOperation, DbtCliProfile
from prefect.server.schemas.schedules import CronSchedule

home_dir = os.path.expanduser("~")
project_dir = os.path.join(home_dir, "de_zoomcamp_2023_project", "prefect")
sys.path.append(project_dir)
import config as cfg

@flow(name="stg_districts", retries=3)
def stg_districts() -> None:
    # result = trigger_dbt_cli_command("dbt run --select stg_districts")

    dbt_cli_profile = DbtCliProfile.load("dez-dbt-cli-profile")

    result = DbtCoreOperation(
        commands=["dbt run --select stg_districts"],
        project_dir="~/de_zoomcamp_2023_project/dez_dbt/",
        profiles_dir="~/de_zoomcamp_2023_project/",
    ).run()

@flow(name="br_districts", retries=3)
def br_districts() -> None:
    # result = trigger_dbt_cli_command("dbt snapshot --select br_districts")

    dbt_cli_profile = DbtCliProfile.load("dez-dbt-cli-profile")

    result = DbtCoreOperation(
        commands=["dbt snapshot --select br_districts"],
        project_dir="~/de_zoomcamp_2023_project/dez_dbt/",
        profiles_dir="~/de_zoomcamp_2023_project/",
    ).run()

@flow(name="go_districts", retries=3)
def go_districts() -> None:
    # result = trigger_dbt_cli_command("dbt run --select go_district")
    
    dbt_cli_profile = DbtCliProfile.load("dez-dbt-cli-profile")

    result = DbtCoreOperation(
        commands=["dbt run --select go_districts"],
        project_dir="~/de_zoomcamp_2023_project/dez_dbt/",
        profiles_dir="~/de_zoomcamp_2023_project/",
    ).run()


###########################################################################################################################################
@flow(name="within-gbq", retries=3)
def run_dbt() -> None:
    """Updates defined dbt models and snapshots"""
    run_1 = stg_districts()
    run_2 = br_districts(wait_for=run_1)
    run_3 = go_districts(wait_for=run_2)

    
###########################################################################################################################################


###########################################################################################################################################
def deploy_flow():
    # DEPLOY_STORE_NAME = "gcs-deployments"
    DEPLOY_STORE_NAME = cfg.configs["DEPLOY_STORE_NAME"]
    storage = GCS.load(DEPLOY_STORE_NAME)
    deployment = Deployment.build_from_flow(
        flow=run_dbt,
        name='dbt',
        description='Runs the defined dbt models',
        version='zoomcamp',
        work_queue_name='default',
        storage=storage,
        tags=["dbt"],
        schedule=(CronSchedule(cron="0 0 12 * * *", timezone="Europe/Berlin")),
    )
    deployment.apply()
###########################################################################################################################################


if __name__ == "__main__":
    #run_dbt()
    deploy_flow()
