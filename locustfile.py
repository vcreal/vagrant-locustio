from locust import HttpLocust, TaskSet, task
import json

class MyTaskSet(TaskSet):
    username="api"
    password="b095754f02442701de2ca86a808ac97b"
    @task(2)
    def index(self):
        self.headers = {"accept-encoding":"gzip, deflate", "Accept":"application/json", "Content-Type":"application/json"}
        json_body={"activity":{"subscriber":{"uid":"user2@test.com"}, "event":"purchase", "properties":{"order_id":"9280", "product_id":["777","345"]}}}
        response=self.client.post("/201507/activities", auth=(self.username, self.password), data=json.dumps(json_body),
                                  headers=self.headers, catch_response=True)
        json_var=response.json()
        print(json_var['timestamp'])

    @task(0)
    def about(self):
        self.client.get("/about/")

class MyLocust(HttpLocust):
    task_set = MyTaskSet
    min_wait = 5000000
    max_wait = 15000000
