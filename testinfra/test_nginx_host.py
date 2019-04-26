testinfra_hosts = ["nginx"]

def test_sudoers_file(host):
    with host.sudo():
        sudoers = host.file("/etc/sudoers")
        passwd = host.file("/etc/passwd")
        assert sudoers.contains("vagrant")
        assert sudoers.contains("admin")

def test_vagrant_user(host):
    user = host.user("vagrant")
    assert user.exists

def test_package_checks(host):
    nginx = host.package("nginx")
    assert nginx.is_installed
    assert nginx.version.startswith("1.10")
    

def test_nginx_service(host):
    service = host.service('nginx')
    assert service.is_running == True
    assert service.is_enabled == True


def test_nginx_listing_port(host):
    assert host.socket("tcp://0.0.0.0:80").is_listening
    assert host.socket("tcp://:::80").is_listening

