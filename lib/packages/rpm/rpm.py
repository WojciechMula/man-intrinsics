import logging
log = logging.getLogger('main')

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


from lib.packages.package import Package
from lib.uops import normalize
from .patterns import *


class RpmSupport(Package):
    def __init__(self, options, datasource, generated_files):
        super(RpmSupport, self).__init__(options, datasource)
        self.generated_files = generated_files


    def create(self):
        path = os.path.join(self.options.rpm_spec_dir, 'man-intrinsics.spec')
        with open(path, 'wt') as f:
            data = {
                'version'       : self.format_version(),
                'description'   : self.format_description(),
                'installdir'    : DEFAULT_DIR,
                'files'         : self.format_files(),
            }

            content = SPEC % data
            f.write(content)

            log.info("%s was created" % path)


    def format_files(self):
        result = []
        for name in self.generated_files:
            result.append(os.path.join(DEFAULT_DIR, name))

        return '\n'.join(result)

