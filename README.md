ssh-knock-interceptor
===

Make jumphosts and knock easier without messing up your ssh config.


## Why?

Maintaining knock commands in your ssh config becomes a huge mess over time.


## Requirements

- Python 3.6+
- knockd
- bash

## Setup

1. Clone the repo in your home folder:
   `git clone https://github.com/timo-reymann/ssh-knock-interceptor.git $HOME/.ssh-knock-interceptor`
2. Add to your ssh config:
    ```
   Host *.example.com
      ProxyCommand bash -c 'source $HOME/.ssh-knock-interceptor/init && ssh-knock-interceptor %h; ssh ${KNOCK_HOST} -W %h:%p'
    ```
3. Create the config file for the knock hosts in `.ssh/knock-config`:
   ```ini
   [app*.example.com]
   sequence = 1000 2000 3000
   host = jumphost-apps.example.com

   [web*.example.com]
   sequence = 1001 2001 3001
   host = jumphost-webservers.example.com
   ```

## How it works

It consists of three parts:

- Python script to parse and validate ini file
- Bash wrapper function to source env vars
- Integration into existing ssh config
