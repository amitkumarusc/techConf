#!/usr/bin/python -tt

import random
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from ..notifier import send_tweets, send_upcoming_conference_notification, give_tag_suggestion_to_all

sched = None
logger = None


def send_twitter_notification(should_exit=False):
    logger.info("[{}] - Sending Twitter notification".format(datetime.now()))
    send_tweets()
    if should_exit:
        sched.shutdown(wait=False)


def send_conf_notification(should_exit=False):
    logger.info("[{}] - Sending conference notification".format(datetime.now()))
    send_upcoming_conference_notification()
    if should_exit:
        sched.shutdown(wait=False)


def send_tag_suggestions(should_exit=False):
    logger.info("[{}] - Sending tag suggestions".format(datetime.now()))
    give_tag_suggestion_to_all()
    if should_exit:
        sched.shutdown(wait=False)


def random_time(start, end):
    sec_diff = int((end - start).total_seconds())
    secs_to_add = random.randint(0, sec_diff)
    return start + timedelta(seconds=secs_to_add)


def get_random_times(n, start, end):
    times = []
    for i in range(0, n):
        times.append(random_time(start, end))
    times.sort()
    return times


def schedule_jobs(times, function):
    for ind, atime in enumerate(times):
        logger.info("[{}] - Time of notification is {}".format(datetime.now(), atime))
        if ind == (len(times) - 1):
            sched.add_job(function, 'date', run_date=atime,
                          args={"should_exit": True})
        else:
            sched.add_job(function, 'date', run_date=atime)


def notification_schedules():
    dadate = datetime.now()
    year = dadate.year
    month = dadate.month
    day = dadate.day

    # the lower bound is 8 o' clock
    lower_bound = datetime(year, month, day, 8, 0, 0)

    # the upper bound is 9 o' clock PM
    upper_bound = datetime(year, month, day, 21, 0, 0)

    twitter_notificatons_count = 10
    conf_notifications_count = 1
    tag_suggestions_count = 1

    twitter_times = get_random_times(twitter_notificatons_count, lower_bound, upper_bound)
    conf_times = get_random_times(conf_notifications_count, lower_bound, upper_bound)

    schedule_jobs(twitter_times, send_twitter_notification)
    schedule_jobs(conf_times, send_conf_notification)
    schedule_jobs(tag_suggestions_count, send_tag_suggestions)

    logger.info("[{}] - Adding notification schedules".format(datetime.now()))


def create_schedules():
    global sched

    sched = BackgroundScheduler()
    notification_schedules()
    sched.start()
