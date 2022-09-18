ssh-knock-interceptor
===

Make jumphosts and knock easier without messing up your ssh config.


## Why?

Maintaining knock commands in your ssh config becomes a huge mess over time.


## Requirements

- Python 3.6+
- bash

## Setup

1. Clone the repo in your home folder:
   `git clone https://github.com/timo-reymann/ssh-knock-interceptor.git $HOME/.ssh-knock-interceptor`
2. Add to your ssh config:
    ```ssh-config
   Host *.example.com
       ProxyCommand bash -c 'source $HOME/.ssh-knock-interceptor/init %h %p'
    ```
3. Create the config file for the knock hosts in `.ssh/knock-config`:
   ```ini
   [app*.example.com]
   sequence = 1000 2000 3000
   host     = jumphost-apps.example.com

   [web*.example.com]
   sequence = 1001 2001 3001
   host     = jumphost-webservers.example.com
   
   [advanced*.example.com]
   use_udp  = true
   sequence = 1001 2001:tcp 3001
   host     = jumphost-webservers.example.com
   ```

## How it works

It consists of three parts:

- Python script 
   - parse and validate ini file
   - knock with python
- Bash wrapper
    - to source env vars
    - execute ssh command in same tty
- Integration into existing ssh config
