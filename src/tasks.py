from locust import HttpLocust, TaskSet
import math
from bs4 import BeautifulSoup

def fetch_static_assets(session, response):
    soup = BeautifulSoup(response.text, "html.parser")
    for res in soup.find_all(src=True):
        url = res['src']

        url_label = None

        if "/w/images/" in url:
            url_label = "Image"

        if "/w/load.php" in url:
            url_label = "MW Resource loader"

        session.client.get(url, name=url_label)


class Top10Pages(TaskSet):
    """ Top 10 pages between 2016-01-09 and 2018-01-09, weighted accordingly """

    _deviceid = None

    ga_data = {
        '/wiki/Main_Page': 4164045,
        '/wiki/Cosmetic_items': 1119661,
        '/wiki/List_of_All_class_cosmetics': 979936,
        '/wiki/Weapons': 885579,
        '/wiki/List_of_Scout_cosmetics': 752997,
        '/wiki/Scout': 730104,
        '/wiki/List_of_Soldier_cosmetics': 649213,
        '/wiki/List_of_Pyro_cosmetics': 641228,
        '/wiki/Crafting': 631810,
        '/wiki/Spy': 626435
    }

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Reduce weights to reasonably equivalent percentage points
        total_weight = sum(self.ga_data.values())

        for page, weight in self.ga_data.items():
            rel_weight = math.ceil(weight / total_weight * 100)
            for i in range(0, rel_weight):
                self.tasks.append(self.partial_test_page(page))


    def partial_test_page(self, page):
        def test_page(self):
            response = self.client.get(page)
            fetch_static_assets(self, response)


        return test_page

class AverageUser(HttpLocust):
    """ Emulate an average user according to Google Analytics data collected between
        2016-01-09 and 2018-01-09 """

    task_set = Top10Pages

    # Average of 90 seconds, but include += 50% variance
    avg_wait = 90 * 1000
    min_wait = 0.5 * avg_wait
    max_wait = 1.5 * avg_wait
