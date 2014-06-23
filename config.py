CRSF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

import os
from blolapp import app

DATABASE=os.path.join(app.root_path, 'blol.db')
SECRET_KEY='development key'
USERNAME='admin'
PASSWORD='default'

DEBUG = False