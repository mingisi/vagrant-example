# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  ####################################################
  ##
  ##  Setting up the nginx server on ip 10.100.195.200
  ##
  ###################################################
  config.vm.define "nginx" do |nginx|
    nginx.vm.box = "puppetlabs/ubuntu-16.04-64-nocm"
    nginx.vm.hostname = "nginx"
    nginx.vm.network "private_network", ip: "10.100.195.200"
    nginx.vm.network "forwarded_port", guest: 80, host: 80

    nginx.vm.provider "virtualbox" do |box|
      box.memory = 2048
    end

    # Nginx upstream values for loadbalancing web-01 and web-02
    nginx_upstreams = [{
      "name" => "webservice",
      "strategy" => "ip_hash",
      "keepalive" => 16,
      "servers" => ["10.100.194.201", "10.100.194.202"],
    }]

    # Running an ansible playbook
    nginx.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "ansible/nginx.yml"
      ansible.verbose = true
      ansible.host_vars = {
        "nginx" => {
          "nginx_upstreams" => "'#{nginx_upstreams.to_json}'",
        },
      }
    end
  end

  # nginx.vm.provision "shell", inline: "curl -sSf http://10.100.195.200 > /dev/null"

  ####################################################
  ##
  ##  Setting up the webserver server web-01 and web-02 
  ##  with ip 10.100.194.201 and 10.100.194.202 
  ##
  ###################################################
  (1..2).each do |i|
    config.vm.define "web-0#{i}" do |web|
      web.vm.box = "puppetlabs/ubuntu-16.04-64-nocm"
      web.vm.hostname = "web-0#{i}"
      web.vm.network "private_network", ip: "10.100.194.20#{i}"
      web.vm.provider "virtualbox" do |box|
        box.memory = 1024
      end

      web.vm.provision "ansible_local" do |ansible|
        ansible.playbook = "ansible/web.yml"
        ansible.verbose = true
      end
    end
  end
end
