'''Run actions on remote machines over SSH.

By default, Sloth CI apps run actions in a subprocess on the same machine they're running on. This extension overrides this and makes the app execute actions on remote machines over SSH.

You can authenticate with login and password or by providing key files.


Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.ext.ssh_exec


Usage
-----

.. code-block:: yaml
    :caption: ssh_exec.yml

    extensions:
        run_over_ssh:
            # Use the sloth_ci.ext.ssh_exec module.
            module: ssh_exec

            # Hosts, comma-delimited. Optional port number can be provided after ':' (if not specified, 22 is used).
            hosts:
                - ssh.example.com
                - myserver.com:23

            # Username to use for authentication.
            username: admin

            # Password to use for authentication or to unlock a private key.
            # password: foobar

            # Additional private key files. If not specified, only the keys from the default location are loaded (i.e. ~/.ssh).
            # keys: 
            #   - ~/my_ssh_keys/key_rsa
            #   - somekey
'''


__title__ = 'sloth-ci.ext.ssh_exec'
__description__ = 'SSH executor for Sloth CI'
__version__ = '1.1.0'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend_sloth(cls, extension):
    '''Replace the default ``execute`` method with the SSH-based one.'''

    from paramiko import SSHClient
    from paramiko.client import AutoAddPolicy


    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            self._ssh_config = extension['config']

            self._ssh_client = SSHClient()

            self.logger.debug('Loading system host keys.')
            self._ssh_client.load_system_host_keys()

            keys = self._ssh_config.get('keys')

            if keys:
                self.logger.debug('Loading additional host keys: %s' % keys)

                for key in keys:
                    self._ssh_client.load_host_keys(key)

            if self._ssh_config.get('auto_add_unknown_hosts'):
                self.logger.debug('Automatically adding unknown hosts.')

                self._ssh_client.set_missing_host_key_policy(AutoAddPolicy())

        def execute(self, action):
            '''Execute an action on remote hosts.

            :param action: action to be executed

            :returns: True if the execution was successful; raises exception otherwise
            '''

            for host in self._ssh_config.get('hosts'):
                try:
                    split_host = host.split(':')
                    hostname = split_host[0]

                    if len(split_host) == 2:
                        port = int(split_host[1])
                    else:
                        port = 22

                    username = self._ssh_config.get('username')
                    password = self._ssh_config.get('password')

                    self.exec_logger.debug('Connecting to %s:%d with username %s)' % (hostname, port, username))

                    self._ssh_client.connect(
                        hostname=hostname,
                        port=port,
                        username=username,
                        password=password,
                    )

                    stdin, stdout, stderr = self._ssh_client.exec_command(action)

                    for out in stdout:
                        self.exec_logger.debug('%s' % out)

                    for err in stderr:
                        self.exec_logger.debug('%s' % err)

                    self.exec_logger.info('Action executed: %s' % action)
                    return True

                except Exception:
                    raise


    return Sloth