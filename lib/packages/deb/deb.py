import logging
log = logging.getLogger('main')

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import errno

from .patterns import *
from lib.packages.package import Package


class DebSupport(Package):
    def __init__(self, options, datasource):
        super(DebSupport, self).__init__(options, datasource)


    def create(self):
        self.dir = os.path.join(self.options.deb_dir, 'DEBIAN')
        try:
            os.mkdir(self.dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        self.create_control()
        self.create_postinst()
        self.create_postrm()


    def create_control(self):
        path = os.path.join(self.dir, 'control')
        with open(path, 'wt') as f:
            data = {
                'version'    : self.format_version(),
                'details'    : self.format_description(),
                'maintainer' : self.format_maintainer(),
            }

            content = CONTROL % data
            f.write(content)

            log.info("%s was created" % path)


    def format_description(self):
        details = []
        for line in self.get_description():
            if line == '':
                line = '.'

            # important: description has to be indented
            details.append(' ' + line)

        return '\n'.join(details)


    def format_maintainer(self):
        return os.getlogin()


    def _create_script(self, name, content):
        path = os.path.join(self.dir, name)
        if os.path.exists(path):
            os.unlink(path)

        with open(path, 'wt') as f:
            f.write(content)

        os.chmod(path, 0o555) # read/execute

        log.info("%s was created" % path)


    def create_postinst(self):
        self._create_script('postinst', POSTINST)


    def create_postrm(self):
        self._create_script('postrm', POSTREMOVE)

