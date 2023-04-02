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

  # # Use the service account to authenticate the GC cli
  # metadata_startup_script = <<-SCRIPT
  #   # Create the directory for the service account key file
  #   mkdir -p /home/gcp_user/.gc && touch /home/gcp_user/.gc/sa_key_file.json
    
  #   # Write the service account key file
  #   echo "${google_service_account_key.de-zoomcamp-2023-project-sa-key.private_key}" > /home/gcp_user/.gc/sa_key_file.json
    
  #   # make files visible
  #   ls -a

  #   # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
  #   export GOOGLE_APPLICATION_CREDENTIALS=/home/gcp_user/.gc/sa_key_file.json
    
  #   # Authenticate the GC cli
  #   gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS
  # SCRIPT

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
      "sudo apt-get update",
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
      "sudo apt-get install git",
      "git clone https://github.com/mrsvllmr/de_zoomcamp_2023_project.git",
      "sudo apt-get install wget",
      "wget https://repo.anaconda.com/archive/Anaconda3-2022.10-Linux-x86_64.sh"
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