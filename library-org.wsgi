activate_this = '/var/www/library.noisebridge.systems/library-org/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

import sys

sys.path.append('/var/www/library.noisebridge.systems/library-org/')

from controller import app as application

