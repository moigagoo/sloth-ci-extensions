﻿'''Run actions inside a `Docker <https://www.docker.com/>`__ image.

By default, Sloth CI apps run actions in a subprocess on the same machine they're running on. This extension overrides this and makes the app execute each action as a container inside a given Docker image.


Installation
------------

.. code-block:: bash

    $ pip install sloth-ci.ext.docker_exec


Usage
-----

.. code-block:: yaml
    :caption: docker_exec.yml

    extensions:
        run_in_docker:
            # Use the module sloth_ci.ext.docker_exec.
            module: docker_exec

            # Image name. If missing, slug of the Sloth app listen point is used.
            # image: foo

            # Path to the Docker daemon to connect to. Can point to either a tcp URL or a unix socket. If missing, the client connects to /var/run/docker.sock.
            # base_url: tcp://555.55.55.55:5555 *.

            # Docker API version used on the server. If missing, the latest version is used.
            # version: 1.10

            # Path to the Dockerfile used to build an image if it doesn't exist. If missing, current directory is used.
            # path_to_dockerfile: docker/files

            # Memory limit in MB.
            # memory_limit: 10

            # CPU share in per cent.
            # cpu_share: 5
'''


__title__ = 'sloth-ci.ext.docker_exec'
__description__ = 'Docker executor for Sloth CI'
__version__ = '1.1.3'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend_sloth(cls, extension):
    '''Replace the default ``execute`` method with the Docker-based one.'''

    from docker import Client

    from slugify import slugify


    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            self._docker_config = extension['config']

            self._docker_client = Client(
                self._docker_config.get('base_url'),
                timeout=10
            )

            self._docker_client._version = str(self._docker_config.get('version') or self._docker_client._version)

            self._docker_image = self._docker_config.get('image') or slugify(self.listen_point)

        def execute(self, action):
            '''Execute an action inside a container, then commit the changes to the image and remove the container.

            :param action: action to be executed

            :returns: True if the execution was successful; raises exception otherwise
            '''

            self.processing_logger.info('Executing action: %s', action)

            try:
                container_id = self._docker_client.create_container(
                    self._docker_image,
                    command=action,
                    working_dir=self.config.get('work_dir') or '.',
                    mem_limit = self._docker_config.get('memory_limit') or 0,
                    cpu_shares = self._docker_config.get('cpu_share') or None
                )['Id']

                self._docker_client.start(container_id)

                for log in self._docker_client.attach(container_id, logs=True, stream=True):
                    self.processing_logger.debug('%s', log)

                self._docker_client.commit(
                    container_id,
                    self._docker_image,
                    message=action
                )

                self._docker_client.remove_container(container_id)

                self.processing_logger.info('Action executed: %s', action)
                return True

            except Exception:
                raise


    return Sloth
