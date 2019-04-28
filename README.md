### Setup

    brew update
    brew cask install virtualbox
    brew cask install vagrant
    brew install python 
    pip install tox (https://tox.readthedocs.io/en/latest/install.html)

### Bring the environment up and run test

1. `vagrant up` 
2. `tox` 

VM should come up and `tox` will re-run the provision then run the infrastructure test and then run api test. `tox` config can be found in `tox.ini`

### Overview
```

                          10.100.194.201
                          +--------+
                     +----+ App 01 +---+
                     |    + -------+   |
       +---------+   |                 |  +---------+
+----> |Nginx(LB)+---+                 +--+ MongoDB |
       +---------+   |                 |  +---------+
   10.100.195.200    |    +--------+   |  10.100.196.205
                     +----+ App 02 +---+
                          +--------+
                          10.100.194.202

```

* Above diagram displays the simple architecture
* Ansible is used to deploy to the above servers. ansible roles have been used for modularity. following roles have been created
  * docker - installs docker, docker-compose and docker-py on ubuntu
  * nginx  - installs nginx on ubuntu
  * service - runs a docker container 
  * sudoers - add vagrent and admin group to sudoers 
   
* Application is a simple Node.js with a rest API which works with mongodb, most of the application code was extracted from following blog (`https://medium.freecodecamp.org/how-to-build-blazing-fast-rest-apis-with-node-js-mongodb-fastify-and-swagger-114e062db0c9`). The app has been dockerized so that it can be easy deployed on both servers `app-01` and `app-02`

### How it works

Created Vagrantfile that creates 4 machines using this box: `puppetlabs/ubuntu-16.04-64-nocm` 

Nginx is installed on the VM using ansible playbook `./ansible/nginx.yml`. `ansible_local` provisioner was used so that user doesn't need to have ansible installed on the host machine. It should get installed on the VM. but this will slow down the building of the VMs

Nginx has been set to use the default configuration file it comes with but the vhost file is customized to include the `upstream` (http://nginx.org/en/docs/http/load_balancing.html).vhost
``` 
e.g

     upstream myapp1 {
         ip_hash;
         server 10.100.194.201;
         server 10.100.194.202;
     }
```
simple curl command is run after the installation of nginx and theapp to check if the nginx and the app servers respond.

e.g

```
curl -sSf http://10.100.195.200/documentation/static/index.html > /dev/null 
```

Nginx playbook `./ansible/nginx.yml` has an additional role called `sudoers` (ansible/roles/sudoers). which should allow `vagrant` user to `sudo` without a password and that anyone in the `admin` group is not able to `sudo` without a password. For testing purposes, I have added user called `james` to the admin group

My preferred method would have been to create a user file in `/etc/sudoers.d` e.g `/etc/sudoers.d/vagrant`

Ansible script should be idempotent. If the nginx config changes the ansible handler will restart the nginx.

I have created a simple Rest API service using Node.js which has been pushed to docker hub (`smuthalib/node-rest-api`) most of the code used to create this application was based on 
https://medium.freecodecamp.org/how-to-build-blazing-fast-rest-apis-with-node-js-mongodb-fastify-and-swagger-114e062db0c9. 

The application has a rest API which can be used to store car information in mongodb, source code for the application can be found in `./app/fastify-api/src`, and set of  simple tests created for the application can be found ( ./app/api-test ), which was written in python. Application need an environment variable `MONGODB_URL` set `e.g MONGODB_URL=mongodb://10.100.196.205`. To build the application locally, change the dir to `./app/fastify-api/src` and run the following command `docker build -t smuthalib/node-rest-api` .

The nginx is installed on the VMs but the application and db run as docker containers. the db does not have a password, has no replication and does not have persistent storage.

Ansible Roles (nginx and docker) have been created in a way that they can be easily modified using variables, and importing tasks depending on the OS and to work with other OS. but for this exercise they were made to work with Ubuntu. Nignx role should be modified to handle the nginx config as well, I have left some code commented out, which can be used to do that

Ansible `docker` role installs docker, docker-compose and docker-py as well 

Ansible `service` role is used to deploy application and mongodb.

Ansible host variables are being populated via Vagrantfile `ansible.host_vars`

testinfra python module is used to test infrastructure and tox module is run the python test. 

Test for infrastructure can be found in `./testinfra` folder

Ansible roles are not tested. Ansible Molecule could have been be used to test the ansible roles.

### Extra Test

* Running the linters
```
    tox -e linters
```

* Running the api test ( testing if application is running )
```
    tox -e api-test
```

