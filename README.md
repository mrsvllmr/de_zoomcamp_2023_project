# Data Engineering Zoomcamp 2023 - The harvest
This repository is an image of my first end-to-end data engineering project at the end of de-zoomcamp 2023. <br>

**Thank you very much to all who offer this well-structured and very practical and thus equally instructive course free of charge!** :raised_hands:

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
- **Batch processing**: Python/Pandas
- **Data warehouse**: Google Big Query
- **Data transformation**: dbt
- **Workflow orchestration**: Prefect
- **Data visualization**: Google Looker Studio

<br>
<br>

# My dashboard

<br>
<br>

# How to make it work

The following instructions are deliberately very detailed. This is not only to ensure functional/reproducibility, but also a comprehensive understanding through explanations and, in part, possible alternatives to individual steps.

1. Clone repository <span style="color:green"> (on your local machine)</span>
    - ```git clone https://github.com/mrsvllmr/de_zoomcamp_2023_project.git```

2. Create a GCP account and a project (via GCP UI) <br>
    -> GCP is used as it offers a 300$ 90 days trial; GCP will be used for storage/warehouse and visualization

3. Install Terraform (locally) (https://developer.hashicorp.com/terraform/downloads; download, unpack, set path variable) <span style="color:green"> (on your local machine)</span> <br>
    -> Terraform will be used to create resources on GCP via code (advantages are among others maintainability/versioning)

4. Install Google SDK (locally) (https://cloud.google.com/sdk/docs/install-sdk?hl=de#windows; see PowerShell command; set path variable to bin folder) <span style="color:green"> (on your local machine)</span> <br>
    -> Installs GC SDK and authenticates with gcloud CLI
    -> Google SDK will be used to communicate via cli
    -> Notice: Restart might be necessary before gcloud can be used via cli

5. Create SSH Key (which will be used to connect to the VM after its creation) <span style="color:green"> (on your local machine)</span>
    - Create a directory as follows: ```C:/Users/{your user}/.ssh``` on your local machine (if you do not follow the pattern/path, you have to adjust the Terraform script accordingly)
    - <span style="color:grey">When using PowerShell the following command might be necessary: ```Set-ExecutionPolicy RemoteSigned -Scope CurrentUser``` <br>
      (if I remember correctly not even necessary as this is already part of the GC SDK installation)</span>
    - <span style="color:grey">Run ```gcloud auth login # OAuth 2 to GCP``` <br>
      (if I remember correctly not even necessary as this is already part of the GC SDK installation)</span>
    - Run one of the following cli commands (depending on your os) to create a private and a public key file (adjust WINDOWS_USER, KEY_FILENAME and USERNAME as needed) and store them in the newly created folder
        - ```ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048``` (Linux)
        - ```ssh-keygen -t rsa -f C:\Users\WINDOWS_USER\.ssh\KEY_FILENAME -C USERNAME -b 2048``` (Windows) <br>
    (for details see [official GCP docs](https://cloud.google.com/compute/docs/connect/create-ssh-keys?hl=de))

6. Set variables as needed/wanted: <span style="color:green"> (on your local machine)</span>
    - Mandatory(!): 
        - "project" variable default in variables.tf (and description, so your resources won't be associated with me :stuck_out_tongue_winking_eye:) as this is the unique identifier of your personal GCP project
        - "gce_ssh_pub_key_file" variable default in variables.tf as this is your local path to the public key
    - It is of course possible to adjust the other variables, for example, to name resources differently. However, please note the dependencies between resources!

7. <span style="color:grey">Run ```gcloud auth application-default login``` to authenticate the cli tool using Application Default Credentials (ADC). <span style="color:green"> (on your local machine)</span> <br>
    (if I remember correctly not even necessary as this is already part of the GC SDK installation)</span>  

8. Initialize Terraform (within the directory where the tf files are saved): ```terraform init``` <span style="color:green"> (on your local machine)</span>

9. Generate execution plan: ```terraform plan``` <span style="color:green"> (on your local machine)</span>

10. Apply the changes and let Terraform perform the actions in GCP: ```terraform apply``` <span style="color:green"> (on your local machine)</span>
    - If asked, add GCP project ID again ([see this video of dezoomcamp course; corresponding timestamp is set, just follow the link](https://youtu.be/dNkEgO-CExg&t=15m20s))
    - Fyi: 
        - The command will 
            - Create a data lake bucket
            - Create a BigQuery dataset
            - Create a compute instance/virtual machine (incl. Ubuntu and SSH enabling)
            - Enable Google/IAM APIs
            - Create a service account
            - Create a IAM member (incl. roles assignments: Owner, BigQuery Admin, Storage Admin, Storage Object Admin)
        - All these steps can also be done via GCP GUI. I have chosen the code-based way to show this possibility. Moreover, this is exactly the use case of Terraform, to create infrastructure via code and thus also to make it versionable.


11. Create SSH connection to the newly created VM <span style="color:green"> (on your local machine)</span>
    - Create a file called ```.config``` within the .ssh directory and paste the following information (of course once again adjusted to your data):
    ```
    Host de-zoomcamp # name of virtual machine
        HostName 34.140.195.121 # add external IP of the newly created virtual machine (GCP > Compute Engine > VM instances)
        User gcp_user # if unchanged gcp_user, otherwise adjust accordingly (variable gce_ssh_user; name used to generate ssh keys)
        IdentityFile c:/users/mariu/.ssh/gcp # adjust accordingly (variable gce_ssh_pub_key_file; path to ssh keys)
        RemoteForward 52698 localhost:52698
        LocalForward 8080 localhost:8080 # pgAdmin
        LocalForward 5432 localhost:5432 # PostgreSQL
        LocalForward 8888 localhost:8888 # Jupyter Notebook
        LocalForward 4200 localhost:4200 # Prefect
        LocalForward 4040 localhost:404 # ?
    ```
    - Afterwards you can connect to the virtual machine via cmd/bash by using ```ssh de-zoomcamp``` <br>
    (instead of ```ssh -i ~/.ssh/gcp de-zoomcamp```)
    
12. Connect to VM (via VS Code and SSH) <span style="color:green"> (on your local machine)</span>
    - In VS Code: Extensions -> Look for "remote ssh" -> Install "Remote-SSH"
    - Click "Open a Remote Window" (bottom left corner) -> Select "Connect to Host…" -> Select "de-zoomcamp" (which is available due to the fact that we have already configured/created the config file)

13. Transfer your service account JSON file to the VM (to be able to connect to GCP via service account/CLI) <span style="color:green"> (local machine to VM)</span>
    - Create a folder /home/{your_user}/.gc/ (reminder: your_user is defined via gce_ssh_user variable in variables.tf)
    - Save your sa-key-file.json within that directory (do not change the name!)

14. Set an environment variable and activate the service account authentication <span style="color:green"> (on VM)</span><br>
    <span style="color:orange">Note: This step has to be repeated every time you open a new bash!</span><br>
    - Run ```cd de_zoomcamp_2023_project```
    - ```export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/sa-key-file.json```
    - ```gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS```

15. Start the Prefect server: <span style="color:green"> (on VM)</span>
    - Activate conda virtual environment: ```source /home/mrsvllmr/anaconda3/bin/activate conda_venv```
    - Start the Prefect server: ```prefect server start```
    - Start the Prefect work queue to be able to run flows via ```prefect agent start --pool default-agent-pool --work-queue default```

16. Configure Prefect to communicate with the server <span style="color:green"> (on VM)</span>
    - Open another bash and activate the virtual environment once again (to keep the "server bash" open)
    - Run ```prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api```

16. Register Prefect blocks via ```python /home/mrsvllmr/de_zoomcamp_2023_project/prefect/1_blocks/gcp_blocks.py``` <span style="color:green"> (on VM)</span>
    - Creates a GCP Credentials block called gcp-credentials (used to authenticate when interacting with GCP)
    - Creates a GCS block called gcp-deployments (used to save the deployments in GCP)
    - Creates a GCS Bucket block called gcs-bucket (used to save the data in GCS)

17. Deploy the processes<span style="color:green"> (on VM)</span>
    - From RKI API to GCS: Run ```python /home/mrsvllmr/de_zoomcamp_2023_project/prefect/2_ingestion/ingest.py```
    - From GCS to GBQ: Run ```python /home/mrsvllmr/de_zoomcamp_2023_project/prefect/3_gcs_to_gbq/gcs_to_gbq.py```

18. Run a flow based on the newly created deployment <span style="color:green"> (on VM)</span>
    - If you want to: Start a Quick Run via UI <br>
      -> Afterwards you will now find a data directory and the ingested json file within your GCS bucket :white_check_mark:

> wip - will be supplemented step by step; until then, this note remains in place

<br>
<br>

---------------------------------------------------------------------------
---------------------------------------------------------------------------

Following steps had been excluded as it should already be done via Terraform (see instance metadata)

6. Upload SSH key to GCP
    - this step ensures a convenient way to log in to the virtual machine
    - ```gcloud compute project-info add-metadata --metadata-from-file ssh-keys=C:\Users\WINDOWS_USER\.ssh\KEY_FILENAME```

7. Create Service Account key
    - ```gcloud iam service-accounts keys create ../.gc/sa-iam.json --iam-account=sa-iam@{your_project_id}.iam.gserviceaccount.com``` (Linux)
    - ```gcloud iam service-accounts keys create C:\Users\WINDOWS_USER\.gc\sa-iam.json --iam-account=sa-iam@{your_project_id}.iam.gserviceaccount.com``` (Windows)

8. Set GOOGLE_APPLICATION_CREDENTIALS environment variable:
    - Run one of the following commands (depending on your os)
        - ```export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"``` (Linux)
        - ```set GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"``` (Windows)

9. Activate Service Account Credentials: 
    - Run one of the following commands (depending on your os)
        - ```gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS``` (Linux)
        - ```gcloud auth activate-service-account --key-file %GOOGLE_APPLICATION_CREDENTIALS%``` (Windows)
        or
        - ```gcloud auth application-default login```

---------------------------------------------------------------------------
---------------------------------------------------------------------------

<br>
<br>

# Prerequisites

Since I actively followed the de-zoomcamp 2023, I already had a GCP Free Trial Account at the beginning of this project. In detail I beforehead
- Created the account
- Created a SSH key (to login to the VM instance)
- Added the SSH key to Google Cloud (hereinafter referred to as "GC")
- Created a VM instance
- Connected Visual Studio Code to the VM
- Configured the VM
    - Installed Anaconda
    - Created .config file to configure the SSH connection to the VM
    - Installed Docker and Docker compose and downloaded the Docker image
    - Installed PGCLI (Postgres command line tool)     
    - Installed Terraform and applied Terraform Plan

> This block is revised after it has been determined which steps are actually still carried out "manually". It is attempted to implement as much as possible code-based and thus easily reproducible. 

<br>
<br>

# Steps towards implementation

Signup Cloud Provider

1. Created a new GCP project called ```de-zoomcamp-2023-project```
2. Created a SSH key (will be used to connect to the virtual machine; for details see [GCP docs](https://cloud.google.com/compute/docs/connect/create-ssh-keys?hl=de))
    - Created ```C:\Users\{...}\.ssh``` directory and switched to it in Git Bash
    - Customized the command from the GC docs to create a private and a public key: ```ssh-keygen -t rsa -f ~/.ssh/gpc -C {...} -b 2048```
    - Added the SSH public key to GC (GC Console -> Compute Engine -> Metadata -> SSH Keys)
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

---------------------------------------------------------------------------
---------------------------------------------------------------------------

# Next Steps
    - Docker (Compose) setup (isolation/containerization of Prefect, dbt etc.)
    - Spark