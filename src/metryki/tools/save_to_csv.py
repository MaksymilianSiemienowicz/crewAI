from crewai.tools import BaseTool
import csv

class SaveToCSV(BaseTool):
    name: str = "Save to CSV"
    description: str = "Save to CSV"
    
    def _run(self, query: str, file_path: str, content: str, subject: str) -> str:
        """
        Save content, subject in to CSV file
        """
        with open(file_path, mode='a') as file:
            writer = csv.writer(file)
            writer.writerow([content, subject])
        

        return("SAVED TO CSV!")