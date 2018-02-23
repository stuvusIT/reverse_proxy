# Reverse proxy

Installs and configure nginx as reverse proxy. Redirects all http requests to https, certificates are automatically issued by [Let's Encrypt](https://letsencrypt.org).

If necessary, certificates are automatically obtained or renewed, any time ansible-playbook is executed.
Support for Unix-PAM authentication, by setting `auth` to true at target server.
Ability to restrict target domains by ip ranges and addresses.
Options to copy obtained certificates to target servers, when requested by them.

When multiple names are given for a `served_domain`, only the first name will proxy, while the other names will redirect to the first name.

## Requirements

A Debian based distribution with certbot available in current apt sources. Correctly configured DNS server.

## Role Variables

### Primary
| Option                                      | Type            | Default                                          | Description                                                                                     | Required                  |
|---------------------------------------------|-----------------|--------------------------------------------------|-------------------------------------------------------------------------------------------------|:-------------------------:|
| proxy_domains                               | list of dicts   |                                                  | List of all target servers                                                                      | Y                         |
| default_url                                 | string          | `https://github.com/stuvusIT/reverse_proxy`      | Url to redirect to if no target with requested domain is configured                             | N                         |
| letsencrypt_email                           | string          |                                                  | E-Mail address to use to request certificates                                                   | Y                         |
| default_cert_mode                           | string          | `0400`                                           | Default file access mode on certificates at target servers                                      | N                         |
| default_cert_group                          | string          | `root`                                           | Default owner group for certificates at target servers                                          | N                         |
| default_cert_owner                          | string          | `root`                                           | Default owner user for certificates at target servers                                           | N                         |
| default_crypto                              | boolean         | `true`                                           | Use https as default to forward traffic                                                         | N                         |
| domain_suffixes                             | list of strings | `['']`                                           | Domain suffixes to append to every not full qualified domain name                               | N                         |
| domain_prefixes                             | list of strings | `['']`                                           | Domain prefixes to append to every not full qualified domain name                               | N                         |
| letsencrypt_staging                         | boolean         | `false`                                          | Use letsencrypt staging servers                                                                 | N                         |
| client_max_body_size                        | string          | `1m`                                             | Set the maximum upload size at the http context                                                 | N                         |
| hsts_max_age                                | integer         | `300`                                            | Strict Transport Security (HSTS) time of life                                                   | N ___(but recommended)___ |
| reverse_proxy_use_dhparam                   | bool            | `True`                                           | Use and generate Diffie-Hellman parameters                                                      | N                         |
| reverse_proxy_dhparam_size                  | integer         | `2048`                                           | Size of Diffie-Hellman parameter                                                                | N                         |
| reverse_proxy_dhparam_max_age               | integer         | `5184000` (60 days)                              | Max age of Diffie-Hellman parameters, before regenerate                                         | N                         |
| reverse_proxy_dhparam_path                  | string          | `/etc/ssl/dhparam.pem`                           | Path to store the Diffie-Hellman parameters                                                     | N                         |
| reverse_proxy_ssl_session_timeout           | string          | `1d`                                             | nginx `ssl_session_timeout` option                                                              | N                         |
| reverse_proxy_ssl_session_cache             | string          | `shared:SSL:50m`                                 | nginx `ssl_session_cache` option                                                                | N                         |
| reverse_proxy_ssl_session_tickets           | boolean         | `False`                                          | nginx `ssl_session_tickets` option                                                              | N                         |
| reverse_proxy_ssl_protocols                 | list of strings | `TLSv1 TLSv1.1 TLSv1.2`                          | nginx `ssl_protocols` option                                                                    | N                         |
| reverse_proxy_ssl_ciphers                   | list of strings | ___see [defaults/main.yml](defaults/main.yml)___ | nginx `ssl_ciphers` option                                                                      | N                         |
| reverse_proxy_ssl_prefer_server_ciphers     | boolean         | `True`                                           | nginx `ssl_prefer_server_ciphers` option                                                        | N                         |
| reverse_proxy_ssl_stapling                  | boolean         | `True`                                           | Enable OCSP Stapling                                                                            | N                         |
| reverse_proxy_ssl_trusted_certificate       | string          |                                                  | nginx `ssl_trusted_certificate` option, path to the intermediate certificate of your CA         | N                         |
| reverse_proxy_redirect_to_first_domain      | boolean         | `True`                                           | Use first domain from every `served_domains` -> `domains` block as default domain               | N                         |
| reverse_proxy_redirect_to_first_domain_code | integer         | `302`                                            | Specify HTTP redirect code for redirects to first(default) domain                               | N                         |
| reverse_proxy_redirect_code                 | integer         | `302`                                            | Specify HTTP redirect code for redirects when using the `redirect` attribute of a served domain | N                         |

### proxy_domains
| Option             | Type          | Default | Description                                                                 | Required |
|--------------------|---------------|---------|-----------------------------------------------------------------------------|:--------:|
| target_description | string        |         | A short description of the target server                                    |     Y    |
| target_host        | string        |         | Ansible host name (will be used to copy requested certificates)             |     Y    |
| target_ip          | string        |         | IP address of target server (will be used as target address to redirect to) |     Y    |
| served_domains     | list of dicts |         | List of all domain lists served by this target server                       |     Y    |

### served_domains
| Option                | Type                    | Default                                | Description                                                                                                         | Required |
|-----------------------|-------------------------|----------------------------------------|---------------------------------------------------------------------------------------------------------------------|:--------:|
| port                  | integer                 |                                        | Target port to redirect to                                                                                          | N        |
| crypto                | boolean                 | [`{{ default_crypto }}`](#primary)     | Use https to forward traffic                                                                                        | N        |
| auth                  | boolean                 | `false`                                | restrict access to system users                                                                                     | N        |
| domains               | list of strings         |                                        | A list of domains to proxy [(see below for more information)¹](#served_domains__1)                                  | Y        |
| access_control        | list of dicts           |                                        | A list of dicts to restrict access to given set of ip ranges                                                        | N        |
| fullchain_path        | string                  |                                        | [Destination path²](#served_domains__2) for fullchain.pem at _target_host_                                          | N        |
| cert_path             | string                  |                                        | [Destination path²](#served_domains__2) for cert.pem at _target_host_                                               | N        |
| chain_path            | string                  |                                        | [Destination path²](#served_domains__2) for chain.pem at _target_host_                                              | N        |
| privkey_path          | string                  |                                        | [Destination path²](#served_domains__2) for privkey.pem at _target_host_                                            | N        |
| fullchain_mode        | string                  | [`{{ default_cert_mode }}`](#primary)  | File access mode for fullchain.pwm at _target_host_                                                                 | N        |
| cert_mode             | string                  | [`{{ default_cert_mode }}`](#primary)  | File access mode for cert.pwm at _target_host_                                                                      | N        |
| chain_mode            | string                  | [`{{ default_cert_mode }}`](#primary)  | File access mode for chain.pwm at _target_host_                                                                     | N        |
| privkey_mode          | string                  | [`{{ default_cert_mode }}`](#primary)  | File access mode for privkey.pwm at _target_host_                                                                   | N        |
| fullchain_group       | string                  | [`{{ default_cert_group }}`](#primary) | Owner group of fullchain.pwm at _target_host_                                                                       | N        |
| cert_group            | string                  | [`{{ default_cert_group }}`](#primary) | Owner group of cert.pwm at _target_host_                                                                            | N        |
| chain_group           | string                  | [`{{ default_cert_group }}`](#primary) | Owner group of chain.pwm at _target_host_                                                                           | N        |
| privkey_group         | string                  | [`{{ default_cert_group }}`](#primary) | Owner group of privkey.pwm at _target_host_                                                                         | N        |
| fullchain_owner       | string                  | [`{{ default_cert_owner }}`](#primary) | Owner of fullchain.pwm at _target_host_                                                                             | N        |
| cert_owner            | string                  | [`{{ default_cert_owner }}`](#primary) | Owner of cert.pwm at _target_host_                                                                                  | N        |
| chain_owner           | string                  | [`{{ default_cert_owner }}`](#primary) | Owner of chain.pwm at _target_host_                                                                                 | N        |
| privkey_owner         | string                  | [`{{ default_cert_owner }}`](#primary) | Owner of privkey.pwm at _target_host_                                                                               | N        |
| client_max_body_size  | string                  |                                        | Set the maximum upload size at server context                                                                       | N        |
| extra_location_config | string                  |                                        | Additional configuration items to add to the default location block (location /)                                    | N        |
| extra_locations       | list of key value dicts | []                                     | Add custom locations to this server block, the key should be a location string, the value defines the location body | N        |
| redirect              | string                  |                                        | Instead of proxying the request, redirect to this URL. The request URI is automatically appended.                   | N        |

<a id="served_domains__1">¹</a> Can be either a fully qualified domain name(with following dot ex. `www.example.com.`) or a short internal domain(will be expanded by `domain_suffixes` and `domain_prefixes` ex. `wiki` or `static.media`)

<a id="served_domains__2">²</a> Path must point to a file in a already existing directory. The file will be either overwritten or created.

### access_control
| Option | Type   | Default | Description                   | Required |
|--------|--------|---------|-------------------------------|:--------:|
| allow  | string |         | IP address or subnet to allow |     N    | | deny   | string |         | IP address or subnet to deny  |     N    |

These dicts are evaluated in given order, so a complete subnet can be allowed with the exception of a given ip, see: [nginx doku](http://nginx.org/en/docs/http/ngx_http_access_module.html#allow) for future information.

## Example Playbook
### Vars:
```yml
letsencrypt_email: hostmaster@example.com
default_url: https://stuvus.uni-stuttgart.de
domain_suffixes:
  - "example.com"
proxy_domains:
  - target_description: music player
    target_host: mpd01
    target_ip: 172.27.10.66
    served_domains:
    - access_control:
      - allow: 172.27.0.0/16
      - deny: all
      port: 6680
      https: false
      domains:
      - mpd
  - target_description: DokuWiki
    target_host: validator
    target_ip: 172.27.10.101
    served_domains:
    - auth: true
      domains:
      - wiki
      - www.wiki
      - wiki.wiki.de.
```
### Result:
This example playbook proxies as follows:

| Domain               | Proxies to               | Redirects to             | Restrictions                         |
|----------------------|--------------------------|--------------------------|--------------------------------------|
| mpd.example.com      | http://172.27.10.66:6680 | -                        | allow: 172.27.0.0/16, deny all other |
| wiki.example.com     | https://172.27.10.101    | -                        | only system users                    |
| www.wiki.example.com | https://172.27.10.101    | https://wiki.example.com | only system users                    |
| wiki.wiki.de         | https://172.27.10.101    | https://wiki.example.com | only system users                    |

## License

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

## Author Information
- [Markus Mroch (Mr. Pi)](https://github.com/Mr-Pi) _markus.mroch@stuvus.uni-stuttgart.de_
