# -*- mode: ruby -*-
# vi: set ft=ruby :

SITTERFIED_API_CPUS = ENV['SITTERFIED_API_CPUS'] ||= '2'
SITTERFIED_API_MEMORY = ENV['SITTERFIED_API_MEMORY'] ||= '2048'

VAGRANTFILE_API_VERSION = '2'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.define :api do |api|
    api.vm.box = 'trusty'
    api.vm.box_url = 'http://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box'
    api.vm.hostname = 'dev-api.sitterfied.com'
    api.vm.network :private_network, ip: '192.168.100.23'

    api.vm.provider :virtualbox do |vb|
      vb.customize ['modifyvm', :id, '--cpus', SITTERFIED_API_CPUS]
      vb.customize ['modifyvm', :id, '--memory', SITTERFIED_API_MEMORY]
      vb.customize ['guestproperty', 'set', :id, '/VirtualBox/GuestAdd/VBoxService/--timesync-set-threshold', 600000]
    end

    api.ssh.forward_agent = true
    api.vm.synced_folder '.', '/opt/sitterfied-api', type: 'nfs'

    if Vagrant.has_plugin?('vagrant-cachier')
      api.cache.auto_detect = true
      api.cache.scope = :machine
    end

    api.vm.provision 'ansible' do |ansible|
      ansible.inventory_path = 'ansible/hosts'
      ansible.playbook = 'ansible/playbooks/main.yml'
      ansible.host_key_checking = false
    end
  end
end
