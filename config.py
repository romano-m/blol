CRSF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

import os
from blolapp import app

DATABASE=os.path.join(app.root_path, 'blolapp.db')
SECRET_KEY='development key'
USERNAME='admin'
PASSWORD='default'

DEBUG = False