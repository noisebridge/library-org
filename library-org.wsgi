import sys
sys.path.insert(0, '/var/www/library.noisebridge.systems/library-org')


activate_this = '/var/www/library.noisebridge.systems/library-org/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))


from controller import app as application
