reverse_proxy
=============

Configure a nginx reverse proxy with ansible and letsencrypt.

Certificates are automatically updated on any ansible-playbook run, if necessary.
Support for Unix-PAM authentication, by setting `auth` to true at target server.

Requirements
------------

a debian based distribution with certbot available in apt cache(no need to manually install).

Role Variables
--------------
```yml
webserver:
  suffix: #list of suffixes automatically added to all domains
    - ""
  prefix: #list of prefixes automatically added to all domains
    - ""
    - "www."
  targets: #list of target servers and domains served by them
    - target: <ip> #replace <ip> with an actually real target server
      auth: [true|false*] #set auth either to true or false (enables unix pam authentication)
      domains: #list of domains served by this target server
        - example.com
        - fuu.de
        - testserver.bla.org

# * default value
```

Dependencies
------------

Example Playbook
----------------
```yml
webserver:
  suffix:
    - example.com
    - example.my-domain.com
  prefix:
    - ""
    - "www"
  targets:
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

License
-------

<a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-sa/4.0/80x15.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-sa/4.0/">Creative Commons Attribution-ShareAlike 4.0 International License</a>.

Author Information
------------------
* [Markus Mroch (Mr. Pi)](https://github.com/Mr-Pi) _markus.mroch@stuvus.uni-stuttgart.de_
