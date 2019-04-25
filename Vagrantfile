# -*- mode: ruby -*-
# vim: ts=2 sw=2 et ft=ruby :

Vagrant.configure("2") do |config|
  # config.vm.synced_folder ".", "/vagrant", disabled: true
  # config.ssh.username = "vagrant"
  # config.ssh.insert_key = false

  config.vm.define "mongodb" do |db|
    db.vm.box = "puppetlabs/ubuntu-16.04-64-nocm"
    db.vm.hostname = "mongodb"
    db.vm.network "private_network", ip: "10.100.196.205"
    db.vm.network "forwarded_port", guest: 8081, host: 8081

    db.vm.provider "virtualbox" do |box|
      box.memory = 2048
    end

    # Nginx upstream variable for loadbalancing web-01 and web-02
    # nginx_upstreams = [{
    #   'name' => 'webservice',
    #   'strategy' => 'ip_hash',
    #   'keepalive' => 16,
    #   'servers' => ['10.100.194.201', '10.100.194.202'],
    # }]

    # Running an ansible playbook
    db.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "ansible/mongodb.yml"
      ansible.verbose = true
      # ansible.host_vars = {
      #   'mongo-express' => {
      #     'nginx_upstreams' => "'#{nginx_upstreams.to_json}'",
      #   },
      # }
    end

    # db.vm.provision 'shell', inline: 'vagrant ssh-config > .vagrant-ssh-config'
    # testing the nignx is reciving traffic from the web-o1 or web-02 server
    # nginx.vm.provision 'shell', inline: 'curl -sSf http://10.100.195.200 > /dev/null'

  end
  ####################################################
  ##
  ##  Setting up the webserver server web-01 and web-02
  ##  with ip 10.100.194.201 and 10.100.194.202
  ##
  ###################################################

  docker_users = [
    "vagrant",
  ]

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
        ansible.host_vars = {
          "web-0#{i}" => {
            "docker_users" => "'#{docker_users.to_json}'",
          },
        }
        ansible.raw_arguments = ["--diff"]
      end

      #  testing if the the web server is responding
      web.vm.provision "shell", inline: "curl -sSf http://10.100.194.20#{i}/documentation/static/index.html  > /dev/null"
    end
  end

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

    # Nginx upstream variable for loadbalancing web-01 and web-02
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

    # testing the nignx is reciving traffic from the web-o1 or web-02 server
    nginx.vm.provision "shell", inline: "curl -sSf http://10.100.195.200/documentation/static/index.html > /dev/null"
  end
end
