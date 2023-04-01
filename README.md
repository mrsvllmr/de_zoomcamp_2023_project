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

<br>
<br>

# My dashboard

<br>
<br>

# How to make it work

1. Clone repository
    - ```git clone https://github.com/mrsvllmr/de_zoomcamp_2023_project.git```

2. Create a GCP account and a project (via GCP UI) <br>
    -> GCP is used as it offers a 300$ 90 days trial; GCP will be used for storage/warehouse and visualization

3. Install Terraform (locally) (https://developer.hashicorp.com/terraform/downloads; download, unpack, set path variable) <br>
    -> Terraform will be used to create resources on GCP via code (advantages are among others maintainability/versioning)

4. Install Google SDK (locally) (https://cloud.google.com/sdk/docs/install-sdk?hl=de#windows; see PowerShell command; set path variable to bin folder) <br>
    -> Google SDK will be used to communicate via cli

5. Create SSH Key (which will be used to connect to the VM after its creation)
    - Create a directory as follows: ```C:/Users/{your user}/.ssh``` on your local machine (if you do not follow the pattern/path, you have to adjust the Terraform script accordingly)
    - Run ```gcloud auth login # OAuth 2 to GCP```
    - Run one of the following cli commands (depending on your os) to create a private and a public key file (adjust KEY_FILENAME and USERNAME as needed) and store them in the newly created folder
        - ```ssh-keygen -t rsa -f ~/.ssh/KEY_FILENAME -C USERNAME -b 2048``` (Linux)
        - ```ssh-keygen -t rsa -f C:\Users\WINDOWS_USER\.ssh\KEY_FILENAME -C USERNAME -b 2048``` (Windows) <br>
    (for details see [official GCP docs](https://cloud.google.com/compute/docs/connect/create-ssh-keys?hl=de))

6. Upload SSH key to GCP
    - this step ensures a convenient way to log in to the virtual machine
    - ```gcloud compute project-info add-metadata --metadata-from-file ssh-keys=C:\Users\WINDOWS_USER\.ssh\KEY_FILENAME```

7. Create Service Account key
    - ```gcloud iam service-accounts keys create ../.gc/sa-iam.json --iam-account=sa-iam@{your_project_id}.iam.gserviceaccount.com``` (Linux)
    - ```gcloud iam service-accounts keys create C:\Users\WINDOWS_USER\.gc\sa-iam.json --iam-account=sa-iam@{your_project_id}.iam.gserviceaccount.com``` (Windows)

7. Set GOOGLE_APPLICATION_CREDENTIALS environment variable:
    - Run one of the following commands (depending on your os)
        - ```export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"``` (Linux)
        - ```set GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"``` (Windows)

8. Activate Service Account Credentials: 
    - Run one of the following commands (depending on your os)
        - ```gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS``` (Linux)
        - ```gcloud auth activate-service-account --key-file %GOOGLE_APPLICATION_CREDENTIALS%``` (Windows)

9. Set variables as needed/wanted:
    - Mandatory(!): 
        - "project" variable default in variables.tf (and description, so your resources won't be associated with me :stuck_out_tongue_winking_eye:) as this is the unique identifier of your personal GCP project
        - "gce_ssh_pub_key_file" variable default in variables.tf as this is your local path to the public key
    - It is of course possible to adjust the other variables, for example, to name resources differently. However, please note the dependencies between resources!

10. Initialize Terraform (within the directory where the tf files are saved): ```terraform init```

11. Generate execution plan: ```terraform plan```

12. Apply the changes and let Terraform perform the actions in GCP: ```terraform apply```
    - If asked, add GCP project ID again ([see this video of dezoomcamp course; corresponding timestamp is set, just follow the link](https://youtu.be/dNkEgO-CExg&t=15m20s))
    - Fyi: 
        - The command will 
            - Create a data lake bucket
            - Create a BigQuery dataset
            - Create a compute instance/virtual machine (incl. Ubuntu and SSH enabling)
            - Enable Google/IAM APIs
            - Create a Service Account
            - Create a IAM Member (incl. roles assignments: Owner, BigQuery Admin, Storage Admin, Storage Object Admin)
        - All these steps can also be done via GCP GUI. I have chosen the code-based way to show this possibility. Moreover, this is exactly the use case of Terraform, to create infrastructure via code and thus also to make it versionable.


13. Create SSH connection to the newly created VM
    - Create a file called ```.config``` within the same directory and paste the following information (of course once again adjusted to your data):
    ```
    Host de-zoomcamp # name of virtual machine
        HostName 34.140.195.121 # add external IP of the newly created virtual machine (GCP > Compute Engine > VM instances)
        User gcp_user # if unchanged gcp_user, otherwise adjust accordingly (variable gce_ssh_user; name used to generate ssh keys)
        IdentityFile c:/users/mariu/.ssh/gcp # adjust accordingly (variable gce_ssh_pub_key_file; path to ssh keys)
    ```
    - Afterwards you can connect to the virtual machine via cmd/bash by using ```ssh de-zoomcamp``` <br>
    (instead of ```ssh -i ~/.ssh/gcp de-zoomcamp```)
    
14. (In case you use VS code and like to connect comfortably)
    - In VS Code: Extensions -> Look for "remote ssh" -> Install "Remote-SSH"
    - Clock "Open a Remote Window" (bottom left corner) -> Select "Connect to Host…" -> Select "de-zoomcamp" (which is available due to the fact that we have already configured/created the config file)

15. Configure the instance
    - Docker / Docker Compose with Anaconda, dbt, Prefect, packages needed (via requirements.txt)

> wip - will be supplemented step by step; until then, this note remains in place

<br>
<br>