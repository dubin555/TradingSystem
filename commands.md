###### Command to run celery background job which try to make possible deals
python3 manage.py celery worker --loglevel=info

###### Command to start the job
python3 manage.py shell
from trading.tasks import *
try_make_deals.delay()

###### Command to clear mysql database
python3 manage.py flush

###### Command to run some test
python3 test/test_server.py
