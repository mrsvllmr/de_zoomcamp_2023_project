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

  service_accounts {
    email = google_service_account.de-zoomcamp-2023-project-sa-id.email
    scopes = ["cloud-platform"]
  }

  metadata = {
    sshKeys = "${var.gce_ssh_user}:${file(var.gce_ssh_pub_key_file)}"
  }

  provisioner "remote-exec" {
    connection {
      type        = "ssh"
      user        = var.gce_ssh_user
      host        = google_compute_instance.instance.network_interface[0].access_config[0].nat_ip
      private_key = file(var.gce_ssh_priv_key_file)
    }
    inline = [
      "git clone https://github.com/mrsvllmr/de_zoomcamp_2023_project.git",
      "sudo apt-get install wget",
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