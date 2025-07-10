import json
from langchain_core.runnables import Runnable

class RunnableExtractJSON(Runnable):
    def invoke(self, input, config=None):
        print("🧪 Raw LLM Output:\n", input)
        import re
        json_pattern = re.compile(r'(\{[\s\S]*\}|\[[\s\S]*\])', re.MULTILINE)
        for match in json_pattern.finditer(input):
            try:
                print("🧪 Parsed Output:\n", match.group(0))
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                continue
        return None

json_parser = RunnableExtractJSON()

def extract_decore(child_function):
    import re
    def extraction_logic(*args, **kwargs):
        content = child_function(*args, **kwargs)
        print(">>>>>> child_function returns: ", content)
        json_pattern = re.compile(r'(\{[\s\S]*\}|\[[\s\S]*\])', re.MULTILINE)
        for match in json_pattern.finditer(content):
            try:
                parsed = json.loads(match.group(0))
                return parsed
            except json.JSONDecodeError:
                continue
        return None

    return extraction_logic
