import argparse
from sqlalchemy.orm import sessionmaker
import time
from db_connect import get_conn

## Argument parser to take the parameters from the command line
## Example on how to run: python run_sums.py 10 READ_COMMITTED
parser = argparse.ArgumentParser()
parser.add_argument('S', type = int, help = 'number of sums')
parser.add_argument('I', help = 'isolation level')
args = parser.parse_args()

## Execute a sum query and return the results
def sum_balance(sess):
    res = sess.execute('SELECT sum(balance) from account').fetchone()
    return res[0]

## Create S sums operations
def S_sums(sess, S):
    sums = []
    start = time.time()

    for i in xrange(0, S):
        while True:
            try:
                sum = sum_balance(sess)
                sums.append(sum)
            except Exception as e:
                print e
                continue
            break

    stop = time.time()
    return sums, stop-start

## Create the engine and run the sums
engine = get_conn()
Session = sessionmaker(bind=engine.execution_options(isolation_level=args.I, autocommit=True))
sess = Session()
sums, time = S_sums(sess, args.S)
print sums
