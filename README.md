# Data Engineering Zoomcamp 2023<br>
# (Hopefully) The harvest :blush:

This repository is an image of my first end-to-end data engineering project at the end of de-zoomcamp 2023. <br>

**Thank you very much to all who offer this well-structured and very practical and thus equally instructive course free of charge!** :raised_hands:

[Shoutout to DataTalksClub](https://www.youtube.com/@DataTalksClub) <br>
[de-zoomcamp 2023](https://www.youtube.com/watch?v=-zpVha7bw5A&list=PL3MmuxUbc_hJjEePXIdE-LVUx_1ZZjYGW) <br>
[de-zoomcamp videos](https://www.youtube.com/watch?v=-zpVha7bw5A&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb)

<br>

# Problem statement

Since this is not done enough nowadays, this project refers to Covid-19 data :stuck_out_tongue_winking_eye: Data source is the RKI (more precisely the API provided by Marlon Rückert here https://api.corona-zahlen.org/ - thanks again! :raised_hands:). <br>
Finally, the following questions are answered:<br>
:grey_question: In which areas is the proportion of corona-related deaths higher than the population proportion of the same region?<br>
:grey_question: How does it differ with respect to the states?<br>
:grey_question: Where is the proportion of deaths strikingly high?<br><br>

<p align="left">
<img src="images/corona.gif" width="200">
</p>

Specifically, the current state of the project regularly polls three endpoints of the API. Due to time constraints, the final dashboard does not refer to all three, however, adding more endpoints would be an easy task as the processing is already quite dynamic/parameterized.

Roughly summarized, the project maps the following steps:
- Setting up the infrastructure largely automated via Terraform
- Daily API retrieval of data in JSON format and saving in GCS/Datalake (Python/Pandas orchestrated by Prefect)
- Daily flatten and transfer from GCS to BigQuery (Python/Pandas orchestrated by Prefect)
- Daily processing/preparation of data (staging/bronze/silver/gold layer via dbt orchestrated by Prefect)
- visualization of data in dashboard (Looker Studio)


<br>
<br>

# Technologies

The project is based on the following technologies (which are also used in the de-zoomcamp 2023, in case you happen to find out about it here and would like to take a look at the extensive material):
- **Cloud platform** (Service Account/IAM, Virtual Machine, Storage/Datalake, Warehouse, Visualization): GCP
- **Infrastructure as code (IaC)**: Terraform
- **Batch processing**: Python/Pandas
- **Data warehouse**: Google Big Query
- **Data transformation**: dbt
- **Workflow orchestration**: Prefect
- **Data visualization**: Google Looker Studio

<br>
<br>

# My dashboard

<p align="left">
<img src="images/dez_2023_dashboard.gif" width="800">
</p>

<br>
<br>

# How to make it work

The following instructions are deliberately very detailed. This is not only to ensure functional/reproducibility, but also a comprehensive understanding through explanations and, in part, possible alternatives to individual steps.

1. Clone repository <span style="color:green"> (on your local machine)</span>
    - ```git clone https://github.com/mrsvllmr/de_zoomcamp_2023_project.git```

2. Create a GCP account and a project (via GCP UI) <br>
    -> GCP is used as it offers a 300$ 90 days trial and, as already touched upon, provides an entire platform

3. Install Terraform (locally) (https://developer.hashicorp.com/terraform/downloads; download, unpack, set path variable) <span style="color:green"> (on your local machine)</span> <br>
    -> Terraform will be used to create resources on GCP via code (advantages are among others maintainability/versioning)

4. Install Google SDK (locally) (https://cloud.google.com/sdk/docs/install-sdk?hl=de#windows; see PowerShell command; set path variable to bin folder) <span style="color:green"> (on your local machine)</span> <br>
    -> Installs GC SDK and authenticates with gcloud CLI
    -> Google SDK will be used to communicate via cli
    -> Notice: Restart might be necessary before gcloud can be used via cli - you can check if everything has been installed correctly via ```gcloud -v```

5. Create SSH Key (which will be used to connect to the VM after its creation) <span style="color:green"> (on your local machine)</span>
    - Create a directory as follows: ```C:/Users/{your user}/.ssh``` on your local machine (if you do not follow the pattern/path, you have to adjust the Terraform script accordingly)
    - <span style="color:grey">When using PowerShell the following command might be necessary: ```Set-ExecutionPolicy RemoteSigned -Scope CurrentUser``` <br>
    - <span style="color:grey">Run ```gcloud auth login # OAuth 2 to GCP``` <br>
    - Run one of the following cli commands (depending on your os) to create a private and a public key file (adjust WINDOWS_USER, KEY_FILENAME and USERNAME as needed) and store them in the newly created folder
        - ```ssh-keygen -t rsa -f ~/.ssh/ssh-key -C USERNAME -b 2048``` (Linux)
        - ```ssh-keygen -t rsa -f C:\Users\WINDOWS_USER\.ssh\KEY_FILENAME -C USERNAME -b 2048``` (Windows) <br>
    (for details see [official GCP docs](https://cloud.google.com/compute/docs/connect/create-ssh-keys?hl=de))
        - fyi in my case 
            - ```ssh-keygen -t rsa -f C:\Users\mariu\.ssh\ssh_key -C mrsvllmr -b 2048```
            - I did not enter a passphrase (so you could also leave it empty as I assume you will only be working on your local machine; otherwise you should of course enter a passphrase)

6. Set variables as needed/wanted: <span style="color:green"> (on your local machine)</span>
    - Mandatory(!): 
        - "project" variable default in variables.tf (and description, so your resources won't be associated with me :stuck_out_tongue_winking_eye:) as this is the unique identifier of your personal GCP project
        - In case you used another user while creating the SSH key files, adjust the "gce_ssh_user" variable accordingly
        - Adjust the "gce_ssh_pub_key_file" variable default in variables.tf (regarding your user) as this is your local path to the public key
        - Adjust the "gce_ssh_priv_key_file" variable default in variables.tf (regarding your user) as this is your local path to the private key
    - It is of course possible to adjust the other variables, for example, to name resources differently. However, please note the dependencies between resources!

7. <span style="color:grey">Run ```gcloud auth application-default login``` to authenticate the cli tool using Application Default Credentials (ADC). <span style="color:green"> (on your local machine)</span> <br>

8. Initialize Terraform (within the directory where the tf files are saved): 
    - ```cd C:\Users\{your_user}\source\repos\de_zoomcamp_2023_project\terraform```
    - ```terraform init``` <span style="color:green"> (on your local machine)</span>

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
        HostName 146.148.113.167 # add external IP of the newly created virtual machine (GCP > Compute Engine > VM instances)
        User mrsvllmr # adjust accordingly (variable gce_ssh_user; name used to generate ssh keys)
        IdentityFile c:/users/mariu/.ssh/ssh_key # adjust accordingly (variable gce_ssh_pub_key_file; path to ssh keys)
        RemoteForward 52698 localhost:52698
        LocalForward 5432 localhost:5432 # PostgreSQL
        LocalForward 8888 localhost:8888 # Jupyter Notebook
        LocalForward 4200 localhost:4200 # Prefect
    ```
    - Afterwards you can connect to the virtual machine via cmd/bash by using ```ssh de-zoomcamp``` <br>
    (instead of ```ssh -i ~/.ssh/gcp de-zoomcamp```)
    
12. Connect to VM (via VS Code and SSH) <span style="color:green"> (on your local machine)</span>
    - In VS Code: Extensions -> Look for "remote ssh" -> Install "Remote-SSH"
    - Click "Open a Remote Window" (bottom left corner) -> Select "Connect to Host…" -> Select "de-zoomcamp" (which is available due to the fact that we have already configured/created the config file)
    - Open the VM directory via "File -> Open Folder..." to be able to transfer files between the local computer and the VM in a simple way via drag & drop

13. Transfer your service account JSON file to the VM (to be able to connect to GCP via service account/CLI) <span style="color:green"> (local machine to VM)</span>
    - Create a folder /home/{your_user}/.gc/ (reminder: your_user is defined via gce_ssh_user variable in variables.tf)
    - Get your Service Account JSON credential file via GCP GUI: IAM and Admin -> Service accounts -> Click on the service account which has already been created via the Terraform script -> KEYS -> ADD KEY -> Create new key -> JSON -> CREATE (this will automatically download the file to your Downloads diretory)
    - Rename the file to ```sa-key-file.json``` and transfer it to the newly created .gc folder on the VM

    - This step could also be done via CLI. Notice: The general service account email address format is ```{service-account-name}@{project-id}.iam.gserviceaccount.com```.
        - ```gcloud iam service-accounts keys create ../.gc/sa-key-file.json --iam-account=de-zoomcamp-2023-project-sa-id@{your_project_id}.iam.gserviceaccount.com``` (Linux)
        - ```gcloud iam service-accounts keys create C:\Users\WINDOWS_USER\.gc\sa-key-file.json --iam-account=de-zoomcamp-2023-project-sa-id@{your_project_id}.iam.gserviceaccount.com``` (Windows)

14. Set an environment variable and activate the service account authentication <span style="color:green"> (on VM)</span><br>
    <span style="color:orange">Note: This step has to be repeated every time you open a new bash!</span><br>
    - Change directory to ```de_zoomcamp_2023_project```
    - ```export GOOGLE_APPLICATION_CREDENTIALS=~/.gc/sa-key-file.json``` (Linux)
    - ```gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS``` (Linux)

15. Start the Prefect server: <span style="color:green"> (on VM)</span>
    - Activate conda virtual environment: ```source /home/mrsvllmr/anaconda3/bin/activate conda_venv```
    - Start the Prefect server: ```prefect server start```

16. Start the Prefect work queue to be able to run flows:
    - Open a new terminal (due to the fact that you need to keep the Prefect Server opened)
    - Activate conda virtual environment: ```source /home/mrsvllmr/anaconda3/bin/activate conda_venv```
    - ```prefect agent start --pool default-agent-pool --work-queue default```

16. Configure Prefect to communicate with the server <span style="color:green"> (on VM)</span>
    - Open another terminal and activate the virtual environment once again (to keep the "server bash" open) via ```source /home/mrsvllmr/anaconda3/bin/activate conda_venv```
    - Run ```prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api```

16. Register Prefect blocks via ```python /home/mrsvllmr/de_zoomcamp_2023_project/prefect/1_blocks/gcp_blocks.py``` <span style="color:green"> (on VM)</span>
    - Creates a GCP Credentials block called gcp-credentials (used to authenticate when interacting with GCP)
    - Creates a GCS block called gcp-deployments (used to save the deployments in GCP)
    - Creates a GCS Bucket block called gcs-bucket (used to save the data in GCS)

17. Deploy the processes<span style="color:green"> (on VM)</span>
    - ```cd C:\Users\mariu\source\repos\de_zoomcamp_2023_project```
    - From RKI API to GCS: Run ```python /home/mrsvllmr/de_zoomcamp_2023_project/prefect/2_ingestion/ingest.py```
    - From GCS to GBQ: Run ```python /home/mrsvllmr/de_zoomcamp_2023_project/prefect/3_gcs_to_gbq/gcs_to_gbq.py```

18. Initialize dbt project
    - When I ran ```dbt init``` I used the service-account method by referencing the json file in the .gc folder. The result of the configuration via CLI is the profiles.yml file. I saved it within the dez_dbt project folder. This facilitates the accessibility of the file and is not critical, since the credentials are still not visible in plain text via the keyfile reference.<br>
    - Fyi, my profiles.yml looks like this:
      ```yml
      dez_dbt:
        outputs:
            dev:
            dataset: de_zoomcamp_2023_project_dataset
            job_execution_timeout_seconds: 300
            job_retries: 1
            keyfile: /home/mrsvllmr/.gc/sa-key-file.json
            location: europe-west1
            method: service-account
            priority: interactive
            project: bright-aloe-381618
            threads: 1
            type: bigquery
        target: dev
      ```
      <span style="color:red">When reproducing, this file must therefore be adjusted accordingly with regards to the keyfile/user within the path and the project!</span>

19. Deploy the dbt jobs/flows via ```python /home/mrsvllmr/de_zoomcamp_2023_project/prefect/4_dbt/dbt_jobs.py```
    - Details regarding the dbt implementations can be of course found within the models and snapshots and in "more_insights/dbt_screenshots.md".

20. Install the dbt packages
    - ```cd /home/mrsvllmr/de_zoomcamp_2023_project/dez_dbt```
    - ```dbt deps```

:white_check_mark: That's it! :white_check_mark:

Now everything should be ready. The processes and their deployments are now ready in Prefect. If you haven't done it yet, feel free to open the Prefect dashboard via http://127.0.0.1:4200 and get an overview of the available blocks and deployments yourself. The latter are automatically scheduled and can of course now be started manually without having to wait for the time. Please pay attention to the sequence according to the scheduling, so that the time-controlled worklfow control is started adhoc in a sensible sequence.

<br>
<br>

# Possible next steps
    - Further optimization/simplification of reproducibility
    - Docker (Compose) setup (isolation/containerization of Prefect, dbt etc.)
    - Use Spark
    - Use multiple BigQuery datasets
    - CI/CD Pipeline
    - Test mechanisms during the individual steps
    - Use make

<br>
<br>

# If you are interested, the following screenshots and descriptions will give you more insights:

- [GCP](more_insights/gcp_screenshots.md)
- [dbt](more_insights/dbt_screenshots.md)
- [Prefect](more_insights/prefect_screenshots.md)