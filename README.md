# Reverse proxy

Installs and configure nginx as reverse proxy. Redirects all http requests to https, certificates are automatically issued by [Let's Encrypt](https://letsencrypt.org).

If necessary, certificates are automatically obtained or renewed, any time ansible-playbook is executed.
Support for Unix-PAM authentication, by setting `auth` to true at target server.
Ability to restrict target domains by ip ranges and addresses.
Options to copy obtained certificates to target servers, when requested by them.

## Requirements

A Debian based distribution with certbot available in current apt sources. Correctly configured DNS server.

## Role Variables

### Primary
| Option               | Type            | Default                                     | Description                                                         | Required |
|----------------------|-----------------|---------------------------------------------|---------------------------------------------------------------------|:--------:|
| proxy_domains        | list of dicts   |                                             | List of all target servers                                          |     Y    |
| default_url          | string          | `https://github.com/stuvusIT/reverse_proxy` | Url to redirect to if no target with requested domain is configured |     N    |
| letsencrypt_email    | string          | `false`                                     | E-Mail address to use to request certificates                       |     Y    |
| default_cert_mode    | string          | `0400`                                      | Default file access mode on certificates at target servers          |     N    |
| default_cert_group   | string          | `root`                                      | Default owner group for certificates at target servers              |     N    |
| default_cert_owner   | string          | `root`                                      | Default owner user for certificates at target servers               |     N    |
| default_crypto       | boolean         | `true`                                      | Use https as default to forward traffic                             |     N    |
| domain_suffixes      | list of strings | `['']`                                      | Domain suffixes to append to every not full qualified domain name   |     N    |
| domain_prefixes      | list of strings | `['']`                                      | Domain prefixes to append to every not full qualified domain name   |     N    |
| letsencrypt_staging  | boolean         | `false`                                     | Use letsencrypt staging servers                                     |     N    |
| client_max_body_size | string          | `1m`                                        | Set the maximum upload size at the http context                     |     N    |

### proxy_domains
| Option             | Type          | Default | Description                                                                 | Required |
|--------------------|---------------|---------|-----------------------------------------------------------------------------|:--------:|
| target_description | string        |         | A short description of the target server                                    |     Y    |
| target_host        | string        |         | Ansible host name (will be used to copy requested certificates)             |     Y    |
| target_ip          | string        |         | IP address of target server (will be used as target address to redirect to) |     Y    |
| served_domains     | list of dicts |         | List of all domain lists served by this target server                       |     Y    |

### served_domains
| Option               | Type            | Default                    | Description                                                                        | Required |
|----------------------|-----------------|----------------------------|------------------------------------------------------------------------------------|:--------:|
| port                 | integer         |                            | Target port to redirect to                                                         |     N    |
| crypto               | boolean         | `{{ default_crypto }}`     | Use https to forward traffic                                                       |     N    |
| auth                 | boolean         | `false`                    | restrict access to system users                                                    |     N    |
| domains              | list of strings |                            | A list of domains to proxy [(see below for more information)¹](#served_domains__1) |     Y    |
| access_control       | list of dicts   |                            | A list of dicts to restrict access to given set of ip ranges                       |     N    |
| fullchain_path       | string          |                            | [Destination path²](#served_domains__2) for fullchain.pem at {{ target_host }}     |     N    |
| cert_path            | string          |                            | [Destination path²](#served_domains__2) for cert.pem at {{ target_host }}          |     N    |
| chain_path           | string          |                            | [Destination path²](#served_domains__2) for chain.pem at {{ target_host }}         |     N    |
| privkey_path         | string          |                            | [Destination path²](#served_domains__2) for privkey.pem at {{ target_host }}       |     N    |
| fullchain_mode       | string          | `{{ default_cert_mode }}`  | File access mode for fullchain.pwm at {{ target_host }}                            |     N    |
| cert_mode            | string          | `{{ default_cert_mode }}`  | File access mode for cert.pwm at {{ target_host }}                                 |     N    |
| chain_mode           | string          | `{{ default_cert_mode }}`  | File access mode for chain.pwm at {{ target_host }}                                |     N    |
| privkey_mode         | string          | `{{ default_cert_mode }}`  | File access mode for privkey.pwm at {{ target_host }}                              |     N    |
| fullchain_group      | string          | `{{ default_cert_group }}` | Owner group of fullchain.pwm at {{ target_host }}                                  |     N    |
| cert_group           | string          | `{{ default_cert_group }}` | Owner group of cert.pwm at {{ target_host }}                                       |     N    |
| chain_group          | string          | `{{ default_cert_group }}` | Owner group of chain.pwm at {{ target_host }}                                      |     N    |
| privkey_group        | string          | `{{ default_cert_group }}` | Owner group of privkey.pwm at {{ target_host }}                                    |     N    |
| fullchain_owner      | string          | `{{ default_cert_owner }}` | Owner of fullchain.pwm at {{ target_host }}                                        |     N    |
| cert_owner           | string          | `{{ default_cert_owner }}` | Owner of cert.pwm at {{ target_host }}                                             |     N    |
| chain_owner          | string          | `{{ default_cert_owner }}` | Owner of chain.pwm at {{ target_host }}                                            |     N    |
| privkey_owner        | string          | `{{ default_cert_owner }}` | Owner of privkey.pwm at {{ target_host }}                                          |     N    |
| client_max_body_size | string          |                            | Set the maximum upload size at server context                                      |     N    |

<a id="served_domains__1">¹</a> Can be either a fully qualified domain name(with following dot ex. `www.example.com.`) or a short internal domain(will be expanded by `domain_suffixes` and `domain_prefixes` ex. `wiki` or `static.media`)

<a id="served_domains__2">²</a> Path must point to a file in a already existing directory. The file will be either overwritten or created.

### access_control
| Option | Type   | Default | Description                   | Required |
|--------|--------|---------|-------------------------------|:--------:|
| allow  | string |         | IP address or subnet to allow |     N    |
| deny   | string |         | IP address or subnet to deny  |     N    |

These dicts are evaluated in given order, so a complete subnet can be allowed with the exception of a given ip, see: [nginx doku](http://nginx.org/en/docs/http/ngx_http_access_module.html#allow) for future information.

## Dependencies

## Example Playbook
### Playbook:

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
  - target_description: DokoWiki
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
This example playbook redirects as follows:

| domain               | redirected to            | restrictions                         |
|----------------------|--------------------------|--------------------------------------|
| mpd.example.com      | http://172.27.10.66:6680 | allow: 172.27.0.0/16, deny all other |
| wiki.example.com     | https://172.27.10.101    | only system users                    |
| www.wiki.example.com | https://172.27.10.101    | only system users                    |
| wiki.wiki.de         | https://172.27.10.101    | only system users                    |

## License

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

## Author Information
* [Markus Mroch (Mr. Pi)](https://github.com/Mr-Pi) _markus.mroch@stuvus.uni-stuttgart.de_
