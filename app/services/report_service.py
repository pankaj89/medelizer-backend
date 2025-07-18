import json

from pypdf import PdfReader

from app.db.report.crud import update_record
from app.llm.chains import get_llm_chain
from app.llm.output_format import summarize_output_format, tips_output_format
from app.llm.prompts import validate_prompt, tips_prompt, summarize_prompt
from app.utils.llm_utils import json_parser


class ReportService:
    """
    Service class to handle medical report processing.
    It extracts content from a PDF, validates it, summarizes it,
    and updates the database with the results.
    """
    def __init__(self, task_id: str, file_path: str):
        self.task_id = task_id
        self.file_path = file_path

    def process_report(self):
        """
        Process the report by extracting content, validating it, summarizing it,
        and updating the database with the result.
        """
        content = self._extract_content()
        if self._is_valid_report(content):
            response = self._summarise_content(content)
            # Update DB for success state using task_id
            if response is not None:
                json_str = json.dumps(response)
                update_record(self.task_id, json_str, True)
            else:
                update_record(self.task_id, "Something bad occurred", True)

        else:
            # Update DB for failure state using task_id
            update_record(self.task_id, "Report is not blood report", False)
        pass

    def _extract_content(self) -> str:
        """
        Extract text content from the PDF report file.
        Returns the extracted text as a string.
        """
        content = ""
        pyPdf = PdfReader(self.file_path)
        for page in pyPdf.pages:
            content += page.extract_text() + " "
        return content

    def _is_valid_report(self, content) -> bool:
        """
        Validate if the extracted content is a proper medical report.
        Returns True if it is a valid report, otherwise False.
        """
        chain = validate_prompt | get_llm_chain() | json_parser
        response = chain.invoke(
            input={
                "report_text": content
            }
        )
        return response.get("is_medical_report", False)

    def _summarise_content(self, content) -> str:
        """
        Summarize the content of the medical report.
        Returns a structured JSON response with the summary and other details.
        """
        chain = summarize_prompt | get_llm_chain() | json_parser
        response = chain.invoke(
            input={
                "report_text": content,
                "output_format": summarize_output_format,
            }
        )
        return response

    @staticmethod
    def get_tips(test_name, summary, parameters):
        """
        Generate tips based on the test name, summary, and parameters.
        Returns a structured JSON response with tips and recommendations.
        """
        chain = tips_prompt | get_llm_chain() | json_parser
        response = chain.invoke(
            input={
                "test_name": test_name,
                "summary": summary,
                "parameters": parameters,
                "output_format": tips_output_format
            }
        )
        return response
