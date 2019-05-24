from locust import HttpLocust, task, TaskSet
import json
from random import randint

class MyTaskSet(TaskSet):
    username = "api"
    password = "5b8ee56cf2d2635644a19ff1ba01d6f1"

    users_list = ["test-event-property@someemail.com", "eb_transactional_campaign@email.com", "user2@test.com"]
    users_count = users_list.__len__()
    order_list = [[], [], []]

    @task(3)
    def add_to_cart(self):
        order = str(randint(0, 10000))
        user_index = randint(1, self.users_count) - 1
        print("user_add_to_cart " + self.users_list[user_index] + " order#" + order)
        self.order_list[user_index].append(order)

        self.headers = {"accept-encoding": "gzip, deflate", "Accept": "application/json",
                        "Content-Type": "application/json"}
        json_body = {"activity": {"subscriber": {"uid": self.users_list[user_index]}, "event": "add_to_cart",
                                  "properties": {"order_id": order}}}
        response = self.client.post("/201507/activities", auth=(self.username, self.password),
                                    data=json.dumps(json_body),
                                    headers=self.headers, catch_response=True)
        json_var = response.json()
        print(json_var['timestamp'])

    @task(4)
    def purchase(self):
        user_index = randint(1, self.users_count) - 1
        user_order_count = self.order_list[user_index].__len__()
        if user_order_count > 0:
            order_index = randint(1, user_order_count) - 1
            print("user " + self.users_list[user_index] + " purchase_order#" + self.order_list[user_index][order_index])
            print(self.order_list[user_index][order_index])


            self.headers = {"accept-encoding": "gzip, deflate", "Accept": "application/json",
                            "Content-Type": "application/json"}
            json_body = {"activity": {"subscriber": {"uid": self.users_list[user_index]}, "event": "purchase",
                                      "properties": {"order_id": self.order_list[user_index][order_index]}}}
            response = self.client.post("/201507/activities", auth=(self.username, self.password),
                                        data=json.dumps(json_body),
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
