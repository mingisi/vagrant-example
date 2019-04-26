# -*- mode: ruby -*-
# vim: ts=2 sw=2 et ft=ruby :

nginx_upstreams = [{
  "name" => "webservice",
  "strategy" => "ip_hash",
  "keepalive" => 16,
  "servers" => ["10.100.194.201", "10.100.194.202"],
}]

docker_users = [
  "vagrant",
]

boxes = {
  "mongodb" => {
                :box => "puppetlabs/ubuntu-16.04-64-nocm",
                :ip  => '10.100.196.205',
                :cpu => "100",
                :ram => "1024",
                :playbook => 'ansible/mongodb.yml',
  },
  "web-01" => {
                :box => "puppetlabs/ubuntu-16.04-64-nocm",
                :ip  => '10.100.194.201',
                :cpu => "100",
                :ram => "1024",
                :playbook => 'ansible/web.yml',
                :ansible_host_vars => {
                  "web-01" => {
                    "docker_users" => "'#{docker_users.to_json}'",
                  }
                }
  },
  "web-02" => {
                :box => "puppetlabs/ubuntu-16.04-64-nocm",
                :ip  => '10.100.194.202',
                :cpu => "100",
                :ram => "1024",
                :playbook => 'ansible/web.yml',
                :ansible_host_vars => {
                  "web-02" => {
                    "docker_users" => "'#{docker_users.to_json}'",
                  }
                }
  },
  "nginx" => {
                :box => "puppetlabs/ubuntu-16.04-64-nocm",
                :ip  => '10.100.195.200',
                :cpu => "100",
                :ram => "1024",
                :forwarded_port => {
                    :guest => 80,
                    :host => 80
                },
                :playbook => 'ansible/nginx.yml',
                :ansible_host_vars => {
                  "nginx" => {
                    "nginx_upstreams" => "'#{nginx_upstreams.to_json}'",
                  },
                },
                :test_url => "http://10.100.195.200/documentation/static/index.html"
  },
}


Vagrant.configure("2") do |config|

  boxes.each do |box_name, box|
    config.vm.define box_name do |machine|
      machine.vm.box = box[:box]
      machine.vm.hostname = box_name
      machine.vm.network "private_network", ip: box[:ip]

      # enable port fowarding 
      if box.key?(:forwarded_port)
        machine.vm.network "forwarded_port", guest: box[:forwarded_port][:guest], host: box[:forwarded_port][:host]
      end

      # limiting cpu and momery
      machine.vm.provider "virtualbox" do |v|
        v.memory = box[:ram]
        # v.customize ["modifyvm", :id, "--cpuexecutioncap", box[:cpu]]
        # v.customize ["modifyvm", :id, "--memory",          box[:ram]]
      end

      # run ansible playbook
      machine.vm.provision "ansible_local" do |ansible|
        ansible.playbook = box[:playbook]
        if  box.key?(:ansible_host_vars)
          ansible.host_vars = box[:ansible_host_vars]
        end
      end

      # healthcheck url - curl request to check if the box responds
      if box.key?(:test_url)
        machine.vm.provision 'shell', inline: "curl -sSf %s > /dev/null" % box[:test_url]
      end
    end
  end
end
