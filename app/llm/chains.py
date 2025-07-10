from langchain_ollama import OllamaLLM

def get_llm_chain():
    llmModel = OllamaLLM(model="llama3.2")
    return llmModel
