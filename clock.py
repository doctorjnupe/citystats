#!/usr/bin/env python
import os
import datetime
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from citystats import Cities
from citystats.forecast import post_forecast
from m2x.client import M2XClient


logging.basicConfig()
sched = BlockingScheduler()

def timed_job():
    print("Starting citystats script...")

    client = M2XClient(key = os.environ['M2X_API_KEY'])

    print("Getting cities...")
    cities_obj = Cities()

    print("Posting forecast...")
    post_forecast(client, cities_obj.cities)
    print("Finished posting forecast!")

# Start time for first job is 10 minutes after first run of clock.py
start_time = datetime.datetime.now() + datetime.timedelta(0,600)
sched.add_job(timed_job, trigger='interval', next_run_time=start_time, days=2)

sched.start()
