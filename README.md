check_mk-agent
=========

check_mk-agent is a role to install the [check_mk](https://mathias-kettner.de/check_mk.html) agent on various Linux and Unix-like systems. Once the installation of the agent is done on the client machine, you can also use the module (check_mk_agent_api) included in this role to register your client with you check_mk omd instance. See the example directory

Requirements
------------

 . [check_mk_web_api](https://github.com/brennerm/check-mk-web-api)
 '''
 pip install check_mk_web_api
 '''

Role Variables
--------------

See [defaults/main.yml](./defaults/main.yml)

Dependencies
------------

None

Example Playbook
----------------

TODO

License
-------

BSD

Author Information
------------------

An optional section for the role authors to include contact information, or a website (HTML is not allowed).
