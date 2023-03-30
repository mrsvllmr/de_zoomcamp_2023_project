# Data Engineering Zoomcamp 2023 - The End and Harvest
This repository is an image of my first end-to-end data engineering project at the end of de-zoomcamp 2023. <br>

**Thank you very much to all who offer this well-structured and very practical and thus equally instructive course free of charge!**

[Shoutout to DataTalksClub](https://www.youtube.com/@DataTalksClub) <br>
[de-zoomcamp 2023](https://www.youtube.com/watch?v=-zpVha7bw5A&list=PL3MmuxUbc_hJjEePXIdE-LVUx_1ZZjYGW) <br>
[de-zoomcamp videos](https://www.youtube.com/watch?v=-zpVha7bw5A&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

<br>

![](images\BallJames-overview-1920.jpg)

<br>

# Problem statement

This project combines my lifelong hobby and professional goal by sourcing, processing and visualising data from the world of football. Therefore I will make use of ```football-data.org```, the dev-friendly football API, which will provide me with the data needed to answer the following questions:

- to be specified
- ...
- 
- 
- 

<br>
<br>

# Technologies

The project is based on the following technologies (which are also used in the de-zoomcamp 2023, in case you happen to find out about it here and would like to take a look at the extensive material):
- **Cloud platform** (Virtual Machine, Storage/Datalake, Warehouse, Visualization): GCP
- **Infrastructure as code (IaC)**: Terraform
- **Batch processing**: to be specified
- **Data warehouse**: Google Big Query
- **Data transformation**: dbt
- **Workflow orchestration**: Prefect
- **Data visualization**: Google Looker Studio

<br>
<br>

---------------------------------------------------------------------------
---------------------------------------------------------------------------

<br>
<br>

# Prerequisites

Since I actively followed the de-zoomcamp 2023, I already had a GCP Free Trial Account at the beginning of this project. In detail I beforehead
- created the account
- created a SSH key (to login to the VM instance)
- added the SSH key to Google Cloud (hereinafter referred to as "GC")
- created a VM instance
- connected Visual Studio Code to the VM
- configured the VM
    - installed Anaconda
    - created .config file to configure the SSH connection to the VM
    - installed Docker and Docker compose and downloaded the Docker image
    - installed PGCLI (Postgres command line tool)     
    - installed Terraform and applied Terraform Plan

> This block is revised after it has been determined which steps are actually still carried out "manually". It is attempted to implement as much as possible code-based and thus easily reproducible. 

<br>
<br>

# Steps towards implementation

Signup Cloud Provider

1. Created a new GCP project called ```de-zoomcamp-2023-project```
2. Created a SSH key (will be used to connect to the virtual machine; for details see [GCP docs](https://cloud.google.com/compute/docs/connect/create-ssh-keys?hl=de))
    - created ```C:\Users\{...}\.ssh``` directory and switched to it in Git Bash
    - customized the command from the GC docs to create a private and a public key: ```ssh-keygen -t rsa -f ~/.ssh/gpc -C {...} -b 2048```
    - added the SSH public key to GC (GC Console -> Compute Engine -> Metadata -> SSH Keys)
3. Connected to the VM via SSH and configured an easier access via config file and finally via Visual Studio Code directly

Cloud Infrastructure

4. Created a new VM instance (Linux/Ubuntu) called ```de-zoomcamp-2023-project-vm```
5. Created GCP service account (for Terraform) and configured the VM to be able to connect (via GOOGLE_APPLICATION_CREDENTIALS environment variable)
6. Enabled the GC APIs needed (Identity and Access Management (IAM), IAM Service Account Credentials)
7. Configured IAM (for BigQuery Admin, Storage Admin and Storage Object Admin)

'Inner' environment

8. Installed Anaconda on the VM (/home/mrsvllmr/anaconda3)
9. Installed docker.io and configured it with the needed permissions (by using [this](https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md))
10. Installed Docker Compose
11. Installed the modules needed (requests, dbt, prefect etc.)
12. Installed Terraform (withinin Docker Compose)
13. Configured the Terraform plan (for Cloud Storage Bucket and BiqQuery Dataset)
14. Cloned my github repository to the VM

> Final structure/representation of the steps not yet found - will be revised

<br>
<br>

# My dashboard

<br>
<br>

# How to make it work

1. Create a GCP Account and a Project <br>
    -> GCP is used as it offers a 300$ 90 days trial; GCP will be used for storage/warehouse and visualization

2. Install Terraform (locally) (https://developer.hashicorp.com/terraform/downloads; download, unpack, set path variable) <br>
    -> Terraform will be used to create resources on GCP via code (advantages are among others maintainability/versioning)

3. Install Google SDK (locally) (https://cloud.google.com/sdk/docs/install-sdk?hl=de#windows; see PowerShell command; set path variable to bin folder) <br>
    -> Google SDK will be used to communicate via cli

4. Set GOOGLE_APPLICATION_CREDENTIALS environment variable: 
    - ```export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"``` (Linux)
    - ```set GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"``` (Windows)

5. Activate Service Account Credentials: 
    - ```gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS``` (Linux)
    - ```gcloud auth activate-service-account --key-file %GOOGLE_APPLICATION_CREDENTIALS%``` (Windows)

6. Set variables as needed/wanted:
    - mandatory(!): "project" variable default in variables.tf (and description, so your resources won't be associated with me ;))

7. Initialize Terraform (within the directory where the tf files are saved): ```terraform init```

8. Generate execution plan: ```terraform plan```

9. Apply the changes and let Terraform perform the actions in GCP: ```terraform apply```

> wip - will be supplemented step by step; until then, this note remains in place

<br>
<br>