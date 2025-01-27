
from inbox_main import start as inbox_start
from orders_main import start as orders_start
from deals_main import start as deals_start

import os

import os
import threading

def run_inbox():
    inbox_start()

def run_orders():
    orders_start()

def run_deals():
    deals_start()

if __name__ == '__main__':
    inbox_thread = threading.Thread(target=run_inbox)
    orders_thread = threading.Thread(target=run_orders)
    deals_thread = threading.Thread(target=run_deals)

    inbox_thread.start()
    orders_thread.start()
    deals_thread.start()

    inbox_thread.join()
    orders_thread.join()
    deals_thread.join()