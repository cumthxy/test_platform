
import os

from app import create_app
from apscheduler.schedulers.background import BackgroundScheduler
app = create_app('production')
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=43817, threaded=True,debug=False)
