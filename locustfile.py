from locust import HttpUser, task, between


class GatewayUser(HttpUser):
    wait_time = between(1, 2)

    @task(5)
    def users(self):
        self.client.get("/users/allUsers")

    @task(3)
    def products(self):
        self.client.get("/products/allProducts")

    @task(2)
    def orders(self):
        self.client.get("/orders/allOrders")