### install vagrant

    brew update
    brew cask install virtualbox
    brew cask install vagrant

### start vagrant box

    vagrant up

### How it works

* Vegrant file build two webserver and one nginx server ( which works as a load balancer )
  * which is set on a 10.100.195.200"
* webserver runs simple docker application (https://hub.docker.com/r/vad1mo/hello-world-rest)
  