from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os 
from tools.mail_send_tool import SendMail

@CrewBase
class DealsManaginCrew():
    """DealsManaging crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
   
    
    def __init__(self) -> None:
        self.google_llm = LLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini/gemini-1.5-flash"
        )

    @agent
    def deal_accpeter(self) -> Agent:
        return Agent(
            config=self.agents_config['deal_accpeter'],
            llm = self.google_llm,
        )

    @task
    def deal_accpeter_task(self) -> Task:
        return Task(
            config=self.tasks_config['deal_accpeter_task'],
            agent=self.deal_accpeter()
        )
        
    @agent
    def deal_responder(self) -> Agent:
        return Agent(
            config=self.agents_config['deal_responder'],
            llm = self.google_llm,
            tools = [SendMail()]
        )
        
    @agent
    def deal_response_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['deal_responder'],
            llm = self.google_llm,
        )        
    
    @task
    def deal_mail_creator_task(self) -> Task:
        return Task(
            config=self.tasks_config['deal_mail_creator_task'],
            agent=self.deal_response_generator()
        )
    
    @task
    def deal_mail_sender_task(self) -> Task:
        return Task(
            config=self.tasks_config['deal_mail_sender_task'],
            agent=self.deal_responder(),
            tools = [SendMail()]
        )
        
    @agent
    def prepare_information_email(self) -> Agent:
        return Agent(
            config=self.agents_config['prepare_information_email'],
            llm = self.google_llm,
        )

    @task
    def prepare_information_email_task(self) -> Task:
        return Task(
            config=self.tasks_config['prepare_information_email_task'],
            agent=self.prepare_information_email(),
        )  

    @agent
    def sent_information_email(self) -> Agent:
        return Agent(
            config=self.agents_config['sent_information_email'],
            llm = self.google_llm,
        )

    @task
    def sent_information_email_task(self) -> Task:
        return Task(
            config=self.tasks_config['sent_information_email_task'],
            agent=self.sent_information_email(),
            tools = [SendMail()]
        )  

    @crew
    def crew(self) -> Crew:
        """Creates the DealsManaging crew"""
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.sequential,
            verbose = True
        )