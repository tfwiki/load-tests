from locust import HttpLocust
from pages import PyromaniaTop10Pages


class PyromaniaUser(HttpLocust):
    """ Emulate Pyromania update users, according to behaviour observed on 2012-06-28 """

    task_set = PyromaniaTop10Pages

    # Average of 64 seconds, but include += 50% variance
    avg_wait = 64 * 1000
    min_wait = 0.5 * avg_wait
    max_wait = 1.5 * avg_wait
