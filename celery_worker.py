import subprocess
from celery import Celery, current_task

app = Celery('celery_worker', broker='pyamqp://guest@localhost//')


@app.task
def task1(filename):
    outputfile = '.'.join(filename.split('.')[:-1]) + '.mp4'
    subprocess.call(['ffmpeg', '-i', filename, outputfile])
    return (current_task.request)
