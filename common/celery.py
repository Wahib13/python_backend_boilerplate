import os
from celery import Celery

app = Celery('common',
             broker=os.environ.get('BROKER_URL'),
            #  backend='rpc://',
             include=['common.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
