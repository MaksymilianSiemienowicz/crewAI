from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
import os 
from tools.postgresql_query_executor_tool import PostgresQueryExecutor
from tools.mail_send_tool import SendMail

@CrewBase
class OrdersManaginCrew():
    """OrdersManaging crew"""
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
   
    
    def __init__(self) -> None:
        self.google_llm = LLM(
        api_key=os.getenv("GEMINI_API_KEY"),
        model="gemini/gemini-1.5-flash"
        )

    @agent
    def postgres_query_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['postgres_query_generator'],
            llm = self.google_llm,
        )

    @task
    def postgres_query_generator_task(self) -> Task:
        return Task(
            config=self.tasks_config['postgres_query_generator_task'],
            agent=self.postgres_query_generator()
        )
    
    @agent
    def postgresql_rag_search(self) -> Agent:
        return Agent(
            config=self.agents_config['postgresql_rag_search'],
            llm = self.google_llm,
            tools = [PostgresQueryExecutor()]
        )

    @task
    def postgresql_rag_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['postgresql_rag_search_task'],
            agent=self.postgresql_rag_search(),
            tools = [PostgresQueryExecutor()]
        )
        
    @agent
    def order_accepter(self) -> Agent:
        return Agent(
            config=self.agents_config['order_accepter'],
            llm = self.google_llm
        )

    @task
    def order_accepter_task(self) -> Task:
        return Task(
            config=self.tasks_config['order_accepter_task'],
            agent=self.order_accepter()
        )
        
    @agent
    def order_response_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['order_response_creator'],
            llm = self.google_llm
        )

    @task
    def order_response_creator_task(self) -> Task:
        return Task(
            config=self.tasks_config['order_response_creator_task'],
            agent=self.order_response_creator()
        )
        
    @agent
    def order_responser(self) -> Agent:
        return Agent(
            config=self.agents_config['order_responser'],
            llm = self.google_llm,
            tools=[SendMail()]
        )

    @task
    def order_responser_task(self) -> Task:
        return Task(
            config=self.tasks_config['order_responser_task'],
            agent=self.order_responser(),
            tools=[SendMail()]
        )
        
    @agent
    def order_information_mail_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['order_information_mail_generator'],
            llm = self.google_llm
        )

    @task
    def order_information_mail_generator_task(self) -> Task:
        return Task(
            config=self.tasks_config['order_information_mail_generator_task'],
            agent=self.order_information_mail_generator()
        )
        
    @agent
    def order_information_mail_sender(self) -> Agent:
        return Agent(
            config=self.agents_config['order_information_mail_sender'],
            llm = self.google_llm,
            tools=[SendMail()]
        )

    @task
    def order_information_mail_sender_task(self) -> Task:
        return Task(
            config=self.tasks_config['order_information_mail_sender_task'],
            agent=self.order_information_mail_sender(),
            tools=[SendMail()]
        )
        
    @crew
    def crew(self) -> Crew:
        """Creates the OrdersManaging crew"""
        return Crew(
            agents = self.agents,
            tasks = self.tasks,
            process = Process.sequential,
            verbose = True
        )