# Ansible Consul Role

ansible-role-consul is an [ansible](http://www.ansible.com) role which:

 * Installs consul
 * Configures consul in either server/client mode
 * Optionally installs dnsmasq
 * Configures consul service(s)

- - - -
# Variables

Here is a list of all the default variables for this role, which are also available in `defaults/main.yml`.

```yml
---
consul_version: 0.7.5
consul_download_username: ""
consul_download_password: ""
consul_download_folder: /tmp

consul_is_ui: false

consul_logfile_dir: /var/log/consul

consul_dns_allow_stale: false
consul_dns_max_stale: 5s
consul_dns_node_ttl: 0s
consul_dns_service_ttl: 0s
consul_dns_enable_truncate: false
consul_dns_only_passing: false
consul_recursors: []

consul_dnsmasq_upstream_template: "resolv_dnsmasq.conf.j2"
consul_kv_template: "consulkv.j2"
consul_add_path_template: "consul.sh.j2"

consul_binary: consul

consul_user: consul
consul_group: consul
```

Creates an http basic auth user/pass. This should be used when `consul_is_ui` is `true`.

    consul_htpasswd_file_path: "/opt/consul/htpasswd.consul"
    consul_htpasswd_user: Your_Htpasswd_User
    consul_htpasswd_pass: "iOSISDOFIOFH09345kjSDFKLDLjkh093245sdfsdf"


```yml
consul_use_systemd: false
consul_use_upstart: true
consul_use_initd: false

consul_is_server: false

consul_domain: consul.

# Inventory group name to search through for consul servers
consul_group_name: consul_servers

consul_servers: ['127.0.0.1']
consul_log_level: "INFO"
consul_syslog: false
consul_rejoin_after_leave: true
consul_leave_on_terminate: false

consul_join_at_start: false
consul_retry_join: false
consul_retry_interval: 30s
consul_retry_max: 0

consul_servers_wan: []
consul_join_wan: false
consul_retry_join_wan: false
consul_retry_interval_wan: 30s
consul_retry_max_wan: 0
consul_advertise_address_wan: false
```

This relates to the ansible_IFACE so that you can choose the interface regardless of EC2/GCE/Vagrant/etc

    consul_iface: "eth0" # This relates to the ansible_IFACE so that you can choose the interface regardless of EC2/GCE/Vagrant/etc

```yml
consul_rpc_address: ""
consul_bind_address: "0.0.0.0"
consul_dynamic_bind: false
consul_client_address: "127.0.0.1"

# encrypt using string from consul keygen
consul_gossip_encrypt: "glconsulglconsulglcons=="

consul_client_address_bind: false
consul_datacenter: "default"

consul_port_dns: 8600
consul_port_http: 8500
consul_port_https: -1
consul_port_rpc: 8400
consul_port_serf_lan: 8301
consul_port_serf_wan: 8302
consul_port_server: 8300
consul_install_dnsmasq: false
consul_install_consulate: false
consul_dnsmasq:
  listen_interface:
    - lo
    - docker0
    - eth0
  no_dhcp_interface:
    - lo
    - docker0
    - eth0
  upstream_servers:
    - 8.8.8.8
    - 8.8.4.4
consul_node_name: "{{ inventory_hostname }}"
consul_verify_server_hostname: false
```

Boolean to enable/disable ACLS. Defaults to false.

    consul_use_acls: false

    consul_acl_datacenter: "{{ consul_datacenter }}"
    consul_acl_default_policy: "allow"
    consul_acl_down_policy: "allow"
    consul_acl_master_token: "78ab5382-6bc9-4bc6-857f-d65f72fe3453"
    consul_acl_token:
    consul_acl_ttl: "30s"

An instance might be defined through:

```yml
# start as a server
consul_is_server: true
# name datacenter
consul_datacenter: test
# name the node
consul_node_name: vagrant
# bind to ip
consul_bind_address: "{{ ansible_default_ipv4['address'] }}"
# encrypt using string from consul keygen
consul_gossip_encrypt: "glconsulglconsulglcons=="
```

## Enable TLS encryption

See [https://www.consul.io/docs/agent/encryption.html](https://www.consul.io/docs/agent/encryption.html) for details.

These files will be created on your Consul host:

```yml
consul_cert_file: "/opt/consul/cert/consul.crt",
consul_key_file: "/opt/consul/cert/consul.key",
consul_ca_file: "/opt/consul/cert/ca.crt",
```

When you provide these vars. You should use Ansible Vault to encrypt these vars or perhaps pass them on the command line.

```yml
consul_tls_cert: |
  CERT CONTENTS HERE

consul_tls_key: |
  KEY CONTENTS HERE

consul_tls_ca_cert: |
  CERT CONTENTS HERE
```

## Atlas Variables

```yml
consul_atlas_infrastructure: "your_infrastructure_name"
consul_atlas_token: "your_consul_token"

# if you want to use Atlas autodiscovery for clustering
consul_atlas_join: true
```

## Telemetry Variables
Consul has excellent [telemetry support](https://www.consul.io/docs/agent/telemetry.html). To enable it, use any of the following variables:

```yml
# if you want Consul to send metrics to a statsd instance
consul_statsd_address: "127.0.0.1:8125"
# if you want Consul to send metrics to a statsite instance
consul_statsite_address: "127.0.0.1:8125"
# this sets the prefix consul uses for all metrics
consul_statsite_prefix: "consul"
```

## DNS Variables
Consul provides the ability to use it as a [DNS resolver](https://www.consul.io/docs/agent/dns.html) for service and node lookups. To enable [dns_config](https://www.consul.io/docs/agent/options.html#dns_config) with the below default values, set the `consul_dns_config` variable to `true`

```yml
consul_dns_allow_stale: false
consul_dns_max_stale: 5s
consul_dns_node_ttl: 0s
consul_dns_service_ttl: 0s
consul_dns_enable_truncate: false
consul_dns_only_passing: false
consul_recursors:
  - 8.8.8.8
  - 8.8.4.4
```

## Handlers

These are the handlers that are defined in `handlers/main.yml`.

* `restart consul`
* `restart dnsmasq`
* `reload consul config`
* `reload systemd`

## Example playbook that configures a Consul server on Ubuntu

```yml
---

- hosts: all
  vars:
    consul_is_server: "true"
    consul_datacenter: "test"
    consul_bind_address: "{{ ansible_default_ipv4['address'] }}"
  roles:
    - ansible-consul
```

## Example playbooks that configures a Consul server on CentOS 7

```yml
---

- hosts: all
  vars:
    httpd_is_behind_loadbalancer: false
    httpd_vhosts_enabled:
      - url: consul.pgporada.test
        enable_ssl_vhost: false
        aliases: []
        serveradmin: philporada@gmail.com
        errorlog: "/var/log/httpd/error_log"
        accesslog: "/var/log/httpd/access_log"
        directory: "/var/www/test1"
        docrootdir: public_html
        use_default_index_page: true
        extra_parameters_main: |
          RewriteEngine On
        extra_parameters_include: |
          # Hide git related stuff
          RewriteRule ^(.*/)?\.git+ - [R=404,L]
          RewriteRule ^(.*/)?\.gitignore+ - [R=404,L]
        extra_parameters_include: |
          #
          <Location "/">
              Require ip 216.109.198.154/32
              Require ip 192.168.33.1/24
              AuthType Basic
              AuthName "Restricted"
              AuthBasicProvider file
              AuthUserFile "{{ consul_htpasswd_file_path }}"
              Require valid-user
          </Location>
          # CVE-2016-5385, CVE-2016-5387
          RequestHeader unset Proxy early
          #
          # Hide git related stuff
          RewriteRule ^(.*/)?\.git+ - [R=404,L]
          RewriteRule ^(.*/)?\.gitignore+ - [R=404,L]
          #
          ProxyRequests Off
          ProxyPreserveHost On
          ProxyPass        / http://localhost:8500/
          ProxyPassReverse / http://localhost:8500/

    consul_is_server: true
    consul_is_ui: true
    consul_iface: eth1
    consul_htpasswd_file_path: "/opt/consul/htpasswd.consul"
    consul_htpasswd_user: test-htpasswd-user
    consul_htpasswd_pass: "SVNljknfeio45h6tSsdfDFj234590"
  roles:
    - ansible-consul
    - pgporada.httpd
```

- - - -
# How to hack away at this role
Before submitting a PR, please create a test and run it through test-kitchen. You will need to have at least Ruby 2.x, probably through rbenv, gem, and Bundler.


Testing

    bundle install
    bundle update
    bundle exec kitchen create
   	bundle exec kitchen converge
   	bundle exec kitchen verify
	bundle exec kitchen destroy

Or in one shot

    bundle install
    bundle exec kitchen test

Please run yamllint if you have it

    find -type f -name "*.yml" -exec yamllint -f parsable {} \;

You will want to added the following entry to `/etc/hosts` so you can hit your local version. Note that the 192.168.33.102 comes from `.kitchen.yml`.

    192.168.33.221 consul.pgporada.test

You should now be able to access [http://consul.pgporada.test/](http://consul.pgporada.test/) and see the Consul dashboard!

- - - -
# Theme Music
[The Aggrolites - Grave Digger](https://www.youtube.com/watch?v=6J25JeenPDY)

- - - -
# License and Author Information
Initial based on (C) Matthew Finlayson under the Apache license.

Heavily altered by Phil Porada.
