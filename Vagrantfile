Vagrant.configure("2") do |config|
  # Especifica la caja base para la máquina virtual
  config.vm.box = "ubuntu/bionic64"  

  # Reenvío de puertos para acceder a la máquina virtual desde el host
  config.vm.network :forwarded_port, host: 3000, guest: 80
  config.vm.network :forwarded_port, host: 5432, guest: 5432

  # Carpeta sincronizada para compartir archivos entre el host y la máquina virtual
  config.vm.synced_folder './', '/vagrant'

  # Instalación de plugins de Vagrant
  config.vagrant.plugins = "vagrant-docker-compose"

  # Aprovisionamiento mediante un script de shell
  config.vm.provision "shell", inline: <<-SHELL
    #!/bin/bash

    # Actualiza y actualiza los paquetes
    sudo apt-get update
    sudo apt-get upgrade -y

    # Cambia al directorio compartido /vagrant
    cd /vagrant

    # Instalación de Node.js
    echo 'Instalando Node.js...'
    # Elimina la carpeta ./env si existe
    rm -rf env
    # Instala Python 3 y venv
    sudo apt-get install -y python3 python3-venv

    # Crea y activa un entorno virtual de Python
    python3 -m venv env
    source env/bin/activate

    # Instala las dependencias del proyecto
    pip install -r /vagrant/requirements.txt

    # Instalación de SQLite
    sudo apt-get install -y sqlite3

    # Cambia al directorio del proyecto
    cd snakegam

    # Inicializa la base de datos con Django
    reflex dn init
    # Crea las migraciones de la base de datos
    reflex db makemigrations --message 'all2' 
    # Ejecuta las migraciones y arranca el servidor
    reflex rum
  SHELL
end
