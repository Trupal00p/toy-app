import webapp2
import json
from webob import Response

tasks = [
    {"id": 1, "title": "Task 1", "completed": False},
    {"id": 2, "title": "Task 2", "completed": True},
]


def add_cors_headers(response):
    response.headers.add_header("Access-Control-Allow-Origin", "*")
    response.headers.add_header(
        "Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS"
    )
    response.headers.add_header("Access-Control-Allow-Headers", "Content-Type")
    return response


class TasksHandler(webapp2.RequestHandler):
    def options(self):
        self.response = add_cors_headers(self.response)
        self.response.set_status(204)

    def get(self):
        self.response = add_cors_headers(self.response)
        self.response.content_type = "application/json"
        self.response.write(json.dumps(tasks))

    def post(self):
        self.response = add_cors_headers(self.response)
        new_task = json.loads(self.request.body)
        tasks.append(new_task)
        self.response.set_status(201)
        self.response.content_type = "application/json"
        self.response.write(json.dumps(new_task))


class TaskHandler(webapp2.RequestHandler):
    def options(self, task_id):
        self.response = add_cors_headers(self.response)
        self.response.set_status(204)

    def delete(self, task_id):
        self.response = add_cors_headers(self.response)
        global tasks
        task_id = int(task_id)
        tasks = [task for task in tasks if task["id"] != task_id]
        self.response.set_status(204)


app = webapp2.WSGIApplication(
    [
        ("/tasks", TasksHandler),
        ("/tasks/(\d+)", TaskHandler),
    ],
    debug=True,
)


def main():
    from paste import httpserver

    httpserver.serve(app, host="127.0.0.1", port="5000")


if __name__ == "__main__":
    main()
