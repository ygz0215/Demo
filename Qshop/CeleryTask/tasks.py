from __future__ import absolute_import
from Qshop.celery import app


@app.task
def Test():
    print('hi')