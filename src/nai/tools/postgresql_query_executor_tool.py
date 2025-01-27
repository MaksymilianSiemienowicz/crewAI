from crewai.tools import BaseTool
import psycopg2
import os
class PostgresQueryExecutor(BaseTool):
    name: str = "PostgresQueryExecutor"
    description: str = "Execute postgresql query"
    
    def _run(self, query: str, postgres_query: str) -> str:
        """
        Move mail with id emailid to spam if was classified as a SPAM
        """
        try:
            connection = psycopg2.connect(
                dbname=os.environ.get("POSTGRES_DB"),
                user=os.environ.get('POSTGRES_USER'),
                password=os.environ.get('POSTGRES_PASSWORD'),
                host=os.environ.get('POSTGRES_HOST'),
                port=os.environ.get('POSTGRES_PORT')
            )
            cursor = connection.cursor()
            cursor.execute(postgres_query)
            rows = cursor.fetchall()
            
            result = "\n".join([str(row) for row in rows])
            cursor.close()
            connection.close()
        
            return(result)
        
        except Exception as e:
            return e
    