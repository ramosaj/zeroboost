FROM python:3.8.0

RUN pip install pandas python-dotenv python-dateutil psycopg2 alembic
RUN pip install freezegun pytest pytest-recording  # testing
RUN pip install flask flask-graphql flask-cors sqlalchemy requests #flask, database
    
RUN pip install python-ballchasing 

COPY . /zeroboost-backend

ENTRYPOINT ["flask","--app", "zeroboost-backend","run", "-p", "5172","--host=0.0.0.0", "--debug"]
