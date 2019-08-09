from locust import HttpLocust, task, TaskSet
import json
from random import randint

class MyTaskSet(TaskSet):
    username = "api"
    password = "5b8ee56cf2d2635644a19ff1ba01d6f1"

    users_count = 1000
    order_list = []
    for i in range(1, users_count + 1):
        order_list.append([])

    headers = {"accept-encoding": "gzip, deflate", "Accept": "application/json",
                    "Content-Type": "application/json"}
    json_body = {
        "activity": {
            "subscriber": {
                "uid": ""
            },
            "event": "",
            "properties": {
                "order_id": 0
            }
        }
    }

    @task(3)
    def add_to_cart(self):
        order = str(randint(1, 10000))
        user_index = randint(1, self.users_count) - 1
        self.order_list[user_index].append(order)
        print("user_add_to_cart " + "user%i@test.com" % user_index + " order#" + order)
        self.json_body['activity']['subscriber']['uid'] = "user%i@test.com" % user_index
        self.json_body['activity']['event'] = "add_to_cart2"
        self.json_body['activity']['properties']['order_id'] = order
        response = self.client.post("/201507/activities", auth=(self.username, self.password),
                                    data=json.dumps(self.json_body),
                                    headers=self.headers, catch_response=True)
        json_var = response.json()
        print(json_var['timestamp'])

    @task(4)
    def purchase(self):
        user_index = randint(1, self.users_count) - 1
        user_order_count = self.order_list[user_index].__len__()
        if user_order_count > 0:
            order_index = randint(1, user_order_count) - 1
            print("user%i@test.com" % user_index + " purchase_order#" + self.order_list[user_index][order_index])
            print(self.order_list[user_index][order_index])
            self.json_body['activity']['subscriber']['uid'] = "user%i@test.com" % user_index
            self.json_body['activity']['event'] = "purchase"
            self.json_body['activity']['properties']['order_id'] = self.order_list[user_index][order_index]
            response = self.client.post("/201507/activities", auth=(self.username, self.password),
                                        data=json.dumps(self.json_body),
                                        headers=self.headers, catch_response=True)
            json_var = response.json()
            print(json_var['timestamp'])

            self.order_list[user_index].remove(self.order_list[user_index][order_index])
        print(self.order_list)


class MyLocust(HttpLocust):
    host = "https://phoenix.app.zetaglobal.net"
    task_set = MyTaskSet
    min_wait = 55 * 1000
    max_wait = 120 * 1000
