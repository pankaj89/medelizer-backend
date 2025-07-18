from langchain_ollama import OllamaLLM

def get_llm_chain():
    """
    Get an instance of the OllamaLLM model.
    This function initializes and returns the OllamaLLM model configured for the 'meditron' model.
    We can conditionally change the model name based on the environment or configuration.
    """
    llmModel = OllamaLLM(model="meditron")
    return llmModel
