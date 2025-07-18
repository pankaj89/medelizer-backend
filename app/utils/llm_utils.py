import json
from langchain_core.runnables import Runnable


class RunnableExtractJSON(Runnable):
    def invoke(self, input, config=None):
        """
        Extracts JSON from the given input string using a regular expression.
        The function searches for a valid JSON object or array in the input string and returns it as a Python dictionary or list.
        If no valid JSON is found, it returns None.

        This method used by a LangChain pipeline to extract JSON content from a string.
        Args:
            input (str): The input string containing potential JSON content.
            config (optional): Configuration parameters (not used in this implementation).

        Returns:
            dict or list or None: Parsed JSON object if found, otherwise None.
        """
        import re
        json_pattern = re.compile(r'(\{[\s\S]*\}|\[[\s\S]*\])', re.MULTILINE)
        for match in json_pattern.finditer(input):
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                continue
        return None


json_parser = RunnableExtractJSON()


def extract_decore(child_function):
    """
    Decorator to extract JSON from the output of a child function.
    It uses a regular expression to find and parse JSON content from the string returned by the child function.
    """
    import re
    def extraction_logic(*args, **kwargs):
        content = child_function(*args, **kwargs)
        json_pattern = re.compile(r'(\{[\s\S]*\}|\[[\s\S]*\])', re.MULTILINE)
        for match in json_pattern.finditer(content):
            try:
                parsed = json.loads(match.group(0))
                return parsed
            except json.JSONDecodeError:
                continue
        return None

    return extraction_logic
