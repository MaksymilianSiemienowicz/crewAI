from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os 
from tools.save_to_csv import SaveToCSV


@CrewBase
class OrderCreatingCrew():
    """OrderCreatimg crew"""
    
    agents_config = 'config/agents.yml'
    tasks_config = 'config/tasks.yml'
   
    
    def __init__(self) -> None:
        self.google_llm = LLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini/gemini-1.5-flash"
        )
    
    @agent
    def generate_order(self) -> Agent:
        return Agent(
            config=self.agents_config['order_mail_generator'],
            llm = self.google_llm,
        )
    
    @task
    def genetate_order_task(self) -> Task:
        return Task(
            config=self.tasks_config['order_mail_generator_task'],
            agent=self.generate_order(),
        )
    
    @agent
    def save_to_csv(self) -> Agent:
        return Agent(
            config=self.agents_config['save_order_mail'],
            llm = self.google_llm,
            tools = [SaveToCSV()]
        )
        
    @task
    def save_to_csv_task(self) -> Task:
        return Task(
            config=self.tasks_config['save_order_mail_task'],
            agent=self.save_to_csv(),
            tools = [SaveToCSV()]
        )
   
    @crew
    def crew(self) -> Crew:
        """Creates the OrderCreatimg crew"""
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.sequential,
            verbose = True
        )