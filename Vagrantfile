# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.vm.network "private_network", ip: "192.168.33.10"
  config.ssh.insert_key = false
  config.ssh.private_key_path = ["key", "~/.vagrant.d/insecure_private_key"]
  config.vm.provision "file", source: "key.pub", destination: "~/.ssh/authorized_keys"
end
