from locust import HttpLocust
from pages import Top10Pages


class AverageUser(HttpLocust):
    """ Emulate an average user according to Google Analytics data collected between
        2016-01-09 and 2018-01-09 """

    task_set = Top10Pages

    # Average of 90 seconds, but include += 50% variance
    avg_wait = 90 * 1000
    min_wait = 0.5 * avg_wait
    max_wait = 1.5 * avg_wait