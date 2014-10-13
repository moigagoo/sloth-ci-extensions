﻿'''OpenVZ executor for Sloth CI app extension that replaces the default executor and runs actions inside a given OpenVZ container.

Config params::

    [openvz_exec]
    ;Container id.
    ctid = 123
'''


__title__ = 'sloth-ci.ext.openvz_exec'
__description__ = 'OpenVZ executor app extension for Sloth CI'
__version__ = '0.0.1'
__author__ = 'Konstantin Molchanov'
__author_email__ = 'moigagoo@live.com'
__license__ = 'MIT'


def extend(cls):
    class Sloth(cls):
        def __init__(self, config):
            super().__init__(config)

            self._openvz_config = self.config['openvz_exec']

        def execute(self, action):
            '''Execute an action inside an OpenVZ container.

            :param action: action to be executed

            :returns: True if successful, Exception otherwise
            '''

            self.processing_logger.info('Executing action: %s', action)

            try:
                ctid = self._openvz_config['ctid']

                openvz_exec_command = 'vzctl exec %d' % ctid

                super().execute(openvz_exec_command + ' ' + action)

                self.processing_logger.info('Action executed: %s', action)
                return True

            except Exception:
                raise

    return Sloth