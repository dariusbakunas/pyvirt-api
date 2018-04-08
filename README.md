## Python Rest API for interacting with libvirt daemon

[![Build Status](https://travis-ci.org/dariusbakunas/pyvirt-api.svg?branch=master)](https://travis-ci.org/dariusbakunas/pyvirt-api)

*This is used by my [homeportal](https://github.com/dariusbakunas/homeportal) project*

### Local dev:

* Create instance/config.py file at project root:

    ```bash
    XEN_URI = 'xen://...'
    ```
    
### Run in docker:

    ```bash
    docker-compose build
    docker-compose up -d # run in detached mode
    ```