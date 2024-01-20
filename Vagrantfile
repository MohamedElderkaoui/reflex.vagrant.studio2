Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"  
  config.vm.network :forwarded_port, host: 8080, guest: 80
  config.vm.network :forwarded_port, host: 5432, guest: 5432
   config.vm.synced_folder './', '/vagrant'

  config.vagrant.plugins = "vagrant-docker-compose"


  config.vm.provision "shell", inline: <<-SHELL
    #!/bin/bash

    # Update and upgrade packages
    sudo apt-get update
    sudo apt-get upgrade -y
    cd /vagrant
    echo 'Installing node...'
    # remome the folder ./env
    rm -rf env
    # Install Python3 and venv
    sudo apt-get install -y python3 python3-venv

    # Create and activate virtual environment
    python3 -m venv env
    source env/bin/activate

    # Install project dependencies
    pip install -r /vagrant/requirements.txt
    reflex init 
    # Install sqlite
    sudo apt-get install -y sqlite3
    cd ./hello_wolrd/hello_wolrd
    reflex dn init
    reflex db makemigrations --message 'all2' 
    
    
  SHELL
end
