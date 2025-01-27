from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PGSearchTool
import os 
from tools.move_to_spam_tool import MoveToSpamTool
from tools.move_to_deals_tool import MoveToDealsTool
from tools.move_to_order_tool import MoveToOrdersTool
from tools.move_to_other_tool import MoveToOtherTool

@CrewBase
class InboxManaginCrew():
    """InboxManaging crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
   
    
    def __init__(self) -> None:
        self.google_llm = LLM(
        api_key=os.getenv("OPENAI_API_KEY"),
        model="openai/gpt-4"
        )

    @agent
    def text_categorizor(self) -> Agent:
        return Agent(
            config=self.agents_config['text_categorizor'],
            llm = self.google_llm,
        )


    @task
    def text_categorizor_task(self) -> Task:
        return Task(
            config=self.tasks_config['text_categorizor_task'],
            agent=self.text_categorizor()
        )
        
    @agent
    def email_handler(self) -> Agent:
        return Agent(
            config=self.agents_config['email_handler'],
            tools=[MoveToSpamTool(), MoveToDealsTool(), MoveToOrdersTool(), MoveToOtherTool()],
            llm = self.google_llm,
        )
        
    @task
    def email_handler_task(self) -> Task:
        return Task(
            config=self.tasks_config['email_handler_task'],
            agent=self.email_handler(),
            tools=[MoveToSpamTool(), MoveToDealsTool(), MoveToOrdersTool(), MoveToOtherTool()] 
        )

    @crew
    def crew(self) -> Crew:
        """Creates the InboxManaging crew"""
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.sequential,
            verbose = True
        )