from __future__ import absolute_import, unicode_literals
from celery import app


@app.task(name='pokemon')
def task_number_one():
    print "okemonsdsadusgfjsdgfjdsfSDFUSDJDSJBDA"
    return "sbfbd"
