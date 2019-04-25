testinfra_hosts = ["web-01", "web-02"]


def test_docker_package(host):
    docker = host.package("docker-ce")
    assert docker.is_installed
    # assert docker.version.startswith("18.09")
    
def test_docker_service(host):
    docker = host.service('docker')
    assert docker.is_running == True
    assert docker.is_enabled == True

def test_pip_packages(host):
    plist = host.pip_package.get_packages()
    assert 'docker-py' in plist


def test_docker_app(host):
    docker = host.docker("node-rest-api")
    assert docker.is_running
    print(docker.id)

def test_docker_app_listing(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening 