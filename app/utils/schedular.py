import time
import dbupdater, notifier
from threading import Timer
from .. import app

class Schedular(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.function   = function
        self.interval   = interval
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

def schedule_tasks():
    print "Scheduling All Tasks"
    gb_update_schedule = Schedular(app.config['DB_UPDATER_TIME'], dbupdater.fetch_conferences)    
    notification_schedule = Schedular(app.config['NOTIFICATION_TIME'], notifier.notify_all)         
    print "Task Scheduled Successfully"