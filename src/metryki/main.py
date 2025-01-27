from spam_generator_crew  import SpamCreatingCrew
from order_generator_crew import OrderCreatingCrew
import time
from deal_generator_crew import DealCreatingCrew

def run():
    
    ai = OrderCreatingCrew().crew()
    ai.kickoff()


for i in range(100):
    time.sleep(10)
    run()