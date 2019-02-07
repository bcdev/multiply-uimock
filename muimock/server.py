import concurrent.futures
import logging
import signal

import tornado.ioloop
import tornado.log
import tornado.web

PORT = 9090
JOBS = {}
EXECUTOR = concurrent.futures.ThreadPoolExecutor(max_workers=8)

LOGGER = logging.getLogger('muimock')


def make_app():
    return tornado.web.Application([
        (r"/jobs/execute", ExecuteHandler),
        (r"/jobs/list", ListHandler),
        (r"/jobs/([0-9]+)", StatusHandler),
        (r"/jobs/cancel/([0-9]+)", CancelHandler),
    ])


def main():
    def shut_down():
        LOGGER.info(f"Shutting down...")
        tornado.ioloop.IOLoop.current().stop()

    def sig_handler(sig, frame):
        LOGGER.warning(f'Caught signal {sig}')
        tornado.ioloop.IOLoop.current().add_callback_from_signal(shut_down)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tornado.log.enable_pretty_logging()
    app = make_app()
    app.listen(PORT)

    LOGGER.info(f"Server listening on port {PORT}...")
    tornado.ioloop.IOLoop.current().start()


class Job:
    """
    Some job.

    :param duration: Job execution in seconds
    """

    _CURRENT_ID = 0

    def __init__(self, duration: int):
        self.id = Job._CURRENT_ID
        self.duration = duration
        self.progress = None
        self.status = "new"
        Job._CURRENT_ID += 1

    def execute(self):
        import time
        self.status = "running"
        self.progress = 0
        steps = 10 * self.duration
        for i in range(steps):
            if self.status == "cancelled":
                return
            self.progress = (i + 1.0) / steps
            # print(self.to_dict())
            time.sleep(0.1)
        self.status = "success"

    def cancel(self):
        self.status = "cancelled"

    def to_dict(self):
        return dict(id=self.id,
                    duration=self.duration,
                    progress=self.progress,
                    status=self.status)


# noinspection PyAbstractClass
class ExecuteHandler(tornado.web.RequestHandler):
    def get(self):
        duration = int(self.get_query_argument("duration"))
        job = Job(duration)
        JOBS[job.id] = job
        EXECUTOR.submit(job.execute)
        self.write(job.to_dict())


# noinspection PyAbstractClass
class StatusHandler(tornado.web.RequestHandler):
    def get(self, job_id: str):
        job_id = int(job_id)
        job = JOBS.get(job_id)
        if job is None:
            self.send_error(404, reason="Job not found")
            return
        self.write(job.to_dict())


# noinspection PyAbstractClass
class CancelHandler(tornado.web.RequestHandler):
    def get(self, job_id: str):
        job_id = int(job_id)
        job = JOBS.get(job_id)
        if job is None:
            self.send_error(404, reason="Job not found")
            return
        job.cancel()
        self.write(job.to_dict())


# noinspection PyAbstractClass
class ListHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(dict(jobs=[job.to_dict() for job in JOBS.values()]))


if __name__ == "__main__":
    main()
