import multiprocessing
import os


bind = "0.0.0.0:5000"
workers = os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1)

accesslog = "-"
errorlog = "-"
capture_output = True
