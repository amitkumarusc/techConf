#!/usr/bin/python -tt

import sys
from apscheduler.schedulers.background import BackgroundScheduler
import notification_schedules


def run_daily_notifier():
    notification_schedules.create_schedules()


def start():
    print "Starting the main schedular"
    sched = BackgroundScheduler()
    sched.add_job(run_daily_notifier, 'interval', days=1, args=[])
    sched.start()
    print "All tasks scheduled successfully"
    return 0


if __name__ == '__main__':
    STATUS = start()
    sys.exit(STATUS)