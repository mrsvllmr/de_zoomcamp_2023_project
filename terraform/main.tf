################################################################################################################################################
# Virtual machine (incl. SSH and GC CLI authentication)
################################################################################################################################################
resource "google_compute_instance" "instance" {
  name         = var.instance
  machine_type = var.machine_type
  zone         = var.zone
  project      = var.project

  boot_disk {
    initialize_params {
      image = "ubuntu-os-cloud/ubuntu-2004-lts"
      size = 25
    }
  }

  network_interface {
    network    = "default"
    subnetwork = "default"
    access_config {
      network_tier = "PREMIUM"
    }
  }

  metadata = {
    sshKeys = "${var.gce_ssh_user}:${file(var.gce_ssh_pub_key_file)}"
  }

  # Use the service account to authenticate the GC cli
  #metadata_startup_script = <<-SCRIPT
  #  # Create the directory for the service account key file
  #  mkdir -p /home/mrsvllmr/.gc && touch /home/mrsvllmr/.gc/sa_key_file.json
  #  
  #  # Write the service account key file
  #  echo "${google_service_account_key.de-zoomcamp-2023-project-sa-key}" > /home/mrsvllmr/.gc/sa_key_file.json
  #  
  #  # make files visible
  #  ls -a
  #
  #  # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
  #  export GOOGLE_APPLICATION_CREDENTIALS=/home/mrsvllmr/.gc/sa_key_file.json
  #  
  #  # Authenticate the GC cli
  #  gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
  #SCRIPT

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = var.gce_ssh_user
      host        = google_compute_instance.instance.network_interface[0].access_config[0].nat_ip
      private_key = file(var.gce_ssh_priv_key_file)
    }
    inline = [
      # "sudo apt-add-repository -r ppa:gnome3-team/gnome3",
      # "sudo apt-add-repository -r ppa:philip.scott/spice-up-daily",
      # "sudo apt-get install -y docker.io",
      # "sudo groupadd docker",
      # "sudo gpasswd -a $USER docker",
      # "sudo service docker restart",
      # "sudo systemctl start docker",
      # "sudo systemctl enable docker",
      # "cd ~",
      # "mkdir bin",
      # "cd ~/bin",
      # "wget https://github.com/docker/compose/releases/download/v2.2.3/docker-compose-linux-x86_64 -O docker-compose",
      # # "sudo apt-get install -y docker-compose"
      # "chmod +x docker-compose",
      # "docker-compose up -d"

      # "sudo apt-get update",
      # "sudo apt-get install git",
      # # "git clone https://github.com/mrsvllmr/de_zoomcamp_2023_project.git",
      # "git clone https://mrsvllmr:${file(var.github_pat)}@github.com/mrsvllmr/de_zoomcamp_2023_project.git",
      # "sudo apt-get install wget",
      # "wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh",
      # "cd /home/mrsvllmr/de_zoomcamp_2023_project",
      # "conda create -n conda_venv",
      # "conda activate conda-env",
      # "conda install pip",
      # "pip install -r requirements.txt"

      # "git clone https://mrsvllmr:${file(var.github_pat)}@github.com/mrsvllmr/de_zoomcamp_2023_project.git",
      # "sudo apt-get install wget",
      # "wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh",
      # "bash Anaconda3-2022.10-Linux-x86_64.sh -b -p /home/mrsvllmr/anaconda3",
      # "export PATH=/home/mrsvllmr/anaconda3/bin:$PATH",
      # "source /home/mrsvllmr/anaconda3/etc/profile.d/conda.sh",
      # "conda create -y -n conda_venv python=3.9",
      # "conda deactivate",
      # "source /home/mrsvllmr/anaconda3/bin/activate conda_venv",
      # "cd /home/mrsvllmr/de_zoomcamp_2023_project",
      # "pip install -r requirements.txt"

      #"git clone https://mrsvllmr:${file(var.github_pat)}@github.com/mrsvllmr/de_zoomcamp_2023_project.git", # temporarily used when repo was private
      "git clone https://github.com/mrsvllmr/de_zoomcamp_2023_project.git",
      "sudo apt-get install wget",
      #"sudo apt-get install git",
      "wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh",
      "bash Anaconda3-2022.10-Linux-x86_64.sh -b -p /home/mrsvllmr/anaconda3",
      "export PATH=/home/mrsvllmr/anaconda3/bin:$PATH",
      "source /home/mrsvllmr/anaconda3/etc/profile.d/conda.sh",
      "conda create -y -n conda_venv python=3.9",
      "export PATH=/home/mrsvllmr/anaconda3/envs/conda_venv/bin:$PATH",
      "source activate conda_venv",
      "cd /home/mrsvllmr/de_zoomcamp_2023_project",
      "pip install -r requirements.txt"
    ]
  }
}

################################################################################################################################################
# Docker compose visibility
################################################################################################################################################
# make Docker Compose visible from every directory
# resource "null_resource" "add_bin_to_path" {
#   provisioner "file" {
#     content = "export PATH=\"${HOME}/bin:${PATH}\""
#     destination = "~/.bashrc"
#     connection {
#       type     = "ssh"
#       user     = var.gce_ssh_user
#       host     = var.instance
#       private_key = file(var.gce_ssh_priv_key_file)
#     }
#   }
# }

# resource "local_file" "de-zoomcamp-2023-project-sa-key-json" {
#   filename = "/home/mrsvllmr/.gc/sa_key_file.json"
#   content  = base64decode(google_service_account_key.de-zoomcamp-2023-project-sa-key.private_key)
# }