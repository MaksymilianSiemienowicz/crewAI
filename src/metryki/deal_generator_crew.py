from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os 
from tools.save_to_csv import SaveToCSV


@CrewBase
class DealCreatingCrew():
    """DealCreatimg crew"""
    
    agents_config = 'config/agents.yml'
    tasks_config = 'config/tasks.yml'
   
    
    def __init__(self) -> None:
        self.google_llm = LLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini/gemini-1.5-flash"
        )
    
    @agent
    def generate_deal(self) -> Agent:
        return Agent(
            config=self.agents_config['deal_mail_generator'],
            llm = self.google_llm,
        )
    
    @task
    def genetate_deal_task(self) -> Task:
        return Task(
            config=self.tasks_config['deal_mail_generator_task'],
            agent=self.generate_deal(),
        )
    
    @agent
    def save_to_csv(self) -> Agent:
        return Agent(
            config=self.agents_config['save_deal_mail'],
            llm = self.google_llm,
            tools = [SaveToCSV()]
        )
        
    @task
    def save_to_csv_task(self) -> Task:
        return Task(
            config=self.tasks_config['save_deal_mail_task'],
            agent=self.save_to_csv(),
            tools = [SaveToCSV()]
        )
   
    @crew
    def crew(self) -> Crew:
        """Creates the DealCreatimg crew"""
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.sequential,
            verbose = True
        )