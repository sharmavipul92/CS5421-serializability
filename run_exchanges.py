import argparse
from sqlalchemy.orm import sessionmaker
import time
from db_connect import get_conn
import random

## Argument parser to take the parameters from the command line
## Example on how to run: python run_exchanges.py 10 SERIALIZABLE
parser = argparse.ArgumentParser()
parser.add_argument('E', type = int, help = 'number of exchange transactions in a process')
parser.add_argument('I', help = 'isolation level')
args = parser.parse_args()

## Execute an exchange query and swap the balance of two accounts
def exchange(sess):
    query1 = "SELECT * from account where id IN(" + `random.randint(1,100000)` + "," + `random.randint(1,100000)` + ")"
    res = sess.execute(query1).fetchall()
    # print res
    query2 = "UPDATE account SET balance = CASE id WHEN " + `res[1].id` + " THEN " + `res[0].balance` + " WHEN " + `res[0].id` + " THEN " + `res[1].balance` + " ELSE balance END WHERE id IN(" + `res[1].id` + "," + `res[0].id` + ")"
    sess.execute(query2)
    sess.commit()


## Create E swap operations
def E_swaps(sess, E):
    start = time.time()

    for i in xrange(0, E):
        while True:
            try:
                exchange(sess)
            except Exception as e:
                print e
                continue
            break

        time.sleep(0.0001)
    stop = time.time()
    return stop-start

## Create the engine and run the swaps
engine = get_conn()
Session = sessionmaker(bind=engine.execution_options(isolation_level=args.I, autocommit=True))
sess = Session()
time = E_swaps(sess, args.E)
print time
