# Reverse proxy

Installs and configure nginx as reverse proxy. Redirects all http requests to https, certificates are automatically issued by [Let's Encrypt](https://letsencrypt.org).

If necessary, certificates are automatically obtained or renewed, anytime ansible-playbook is executed.
Support for Unix-PAM authentication, by setting `auth` to true at target server.

## Requirements

A Debian based distribution with certbot available in current apt sources.

## Role Variables
```yml
letsencrypt_email: <your e-mail address> # Email address which should be used to request Letsencrypt certificates
default_url: <your fallback address> # Default or fallback address (clients are redirected to this address in case target server isn't reachable)
staging: [true|false*] # Use Letsencrypt staging server
url_suffix: # List of suffixes automatically added to all domains
  - ""
url_prefix: # List of prefixes automatically added to all domains
  - ""
  - "www."
proxy_targets: # List of target servers and domains served by them
  - target: <ip> # Replace <ip> with an actually real target server
    auth: [true|false*] # Set auth either to true or false (enables Unix PAM authentication)
    domains: # List of domains served by this target server
      - example.com
      - fuu.de
      - testserver.bla.org

# * default value
```
**WARNING:** `letsencrypt_email` **is required, if not specified no certificates are requested and deployed!!!**

Default values are specified [here](defaults/main.yml) (except auth, which is specified by template file).

## Dependencies

## Example Playbook
### Playbook:

### Vars:
```yml
letsencrypt_email: test@example.com
default_url: www.example.com
url_suffix:
  - example.com
  - example.my-domain.com
url_prefix:
  - ""
  - "www"
proxy_targets:
  - target: 172.30.0.2
    domains:
      - pictures
      - images
  - target: 172.30.0.2
    auth: true
    domains:
      - private.pictures
  - target: 172.30.0.3
    auth: false
    domains:
      - static
```
### Result:
This example playbook redirects as follows:

| domain                                     | target server | authentication required |
|--------------------------------------------|---------------|-------------------------|
| pictures.example.com                       | 172.30.0.2    | no                      |
| pictures.example.my-domain.com             | 172.30.0.2    | no                      |
| www.pictures.example.com                   | 172.30.0.2    | no                      |
| www.pictures.example.my-domain.com         | 172.30.0.2    | no                      |
| images.example.com                         | 172.30.0.2    | no                      |
| www.images.example.my-domain.com           | 172.30.0.2    | no                      |
| www.images.example.com                     | 172.30.0.2    | no                      |
| images.example.my-domain.com               | 172.30.0.2    | no                      |
| private.pictures.example.com               | 172.30.0.2    | yes                     |
| private.pictures.example.my-domain.com     | 172.30.0.2    | yes                     |
| www.private.pictures.example.com           | 172.30.0.2    | yes                     |
| www.private.pictures.example.my-domain.com | 172.30.0.2    | yes                     |
| static.example.com                         | 172.30.0.3    | no                      |
| static.example.my-domain.com               | 172.30.0.3    | no                      |
| www.static.example.com                     | 172.30.0.3    | no                      |
| www.static.example.my-domain.com           | 172.30.0.3    | no                      |

## License

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

## Author Information
* [Markus Mroch (Mr. Pi)](https://github.com/Mr-Pi) _markus.mroch@stuvus.uni-stuttgart.de_
