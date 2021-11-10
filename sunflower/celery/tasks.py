from sunflower.celery import app

@app.task
def sum(x, y):
    return x + y
