import sys
import os
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

from apps import app
from apps.configure import config

from flask_cors import CORS
cors = CORS (
    app,
    resources={r"/*" : {"origins" : "*"}}
)

if __name__ == '__name__':
    app.run(port=config.PORT, debug=True)