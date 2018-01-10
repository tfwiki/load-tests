import math
from locust import TaskSet
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


class GoogleAnalytics(TaskSet):
    """ TaskSet based on Google Analytics data """

    _deviceid = None

    ga_data = {
        'example_page': 123
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


class Top10Pages(GoogleAnalytics):
    """ Top 10 pages between 2016-01-09 and 2018-01-09, weighted accordingly """

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


class PyromaniaTop10Pages(Top10Pages):
    """ Top 10 pages on 2012-06-28 """

    ga_data = {
        "/wiki/Main_Page": 134075,
        "/wiki/Pyromania_Update": 49776,
        "/wiki/Doomsday": 30943,
        "/wiki/Pyro": 23533,
        "/wiki/ARG": 21261,
        "/wiki/Meet_the_Pyro": 18845,
        "/wiki/Non-player_characters": 14484,
        "/wiki/Main_Page/ru": 12651,
        "/wiki/Astro-chievements": 9413,
        "/wiki/File:Pyromania_Day1_Doomsday_Screengrab.png": 8794,
    }
