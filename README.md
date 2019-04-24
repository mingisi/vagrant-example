### install vagrant

    brew update
    brew cask install virtualbox
    brew cask install vagrant

    brew install python 


### start vagrant boxs

    vagrant up

### Summary
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

* Above digram displays simple architecture
  
* Ansible is used to deploy to the above servers. ansible roles have been used for modularity. following roles have been created
  * docker - installs docker on ubuntu
  * nginx  - installs nginx on ubuntu
  * service - runns a docker container 
  * sudoers - add vagrent and admin group to sudoers 
   
* Application is simple nodejs, rest api which works with mongodb, most of the application code was extracted from following blog (`https://medium.freecodecamp.org/how-to-build-blazing-fast-rest-apis-with-node-js-mongodb-fastify-and-swagger-114e062db0c9`). the app has been dockerised so that it can be easy deployed on both servers  `app-01` and `app-02`

### How it works

*NGINX*

*  `nginx` is installed on the server using `apt`. `nginx` is configured to load balancer and distribute traffic between the the two application server. nginx uses the default configuration file it comes with but the `vhost` file is customized include `upstream` (http://nginx.org/en/docs/http/load_balancing.html) 
        e.g

            upstream myapp1 {
                ip_hash;
                server 10.100.194.201;
                server 10.100.194.202;
            }
 
 `ansible/nginx.yml` ansibile playbook is used to install nginx and deploy the vhost file onto a Ubuntu VM. In addition to that it updates the  `/etc/sudoers` file, giving permison to `vagrent` user to sudo without a password and force the password on the `admin` group

*APPLICATION*

* The same code for application can be found `./app/fastify-api` 
  * application has been already been pushed into docker hub `smuthalib/node-rest-api:v1.0.0` 
  * `fastify-api` docker application/service needs environment varible `MONGODB_URL` passed e.g `MONGODB_URL=mongodb://10.100.196.205` 
  *  to build the application locally, change dir to `./app/fastify-api/src` and run the following command `docker build -t smuthalib/node-rest-api .` 


*DATABASE*

*  mongodb deploy has without any password and has no data folders mounted ( data is not persistent) . 

### Testing

Install tool for testing  

    virtualenv -p /usr/local/opt/python/bin/python3.7 .alvenv 
    source ./.alvenv/bin/activate
    pip install molecule 
    pip install python-vagrant

vagrant ssh-config > .vagrant/ssh-config
testinfra --hosts=default --ssh-config=.vagrant/ssh-config tests.py
