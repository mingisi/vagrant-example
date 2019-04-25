testinfra_hosts = ["mongodb"]


def test_docker_package(host):
    docker = host.package("docker-ce")
    assert docker.is_installed
    # assert docker.version.startswith("18.09")
    
def test_docker_service(host):
    docker = host.service('docker')
    assert docker.is_running == True
    assert docker.is_enabled == True


def test_docker_app(host):
    docker = host.docker("mongodb")
    assert docker.is_running

def test_docker_app_listing(host):
    assert host.socket("tcp://0.0.0.0:27017").is_listening 