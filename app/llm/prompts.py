from langchain_core.prompts import PromptTemplate

validate_prompt = PromptTemplate(
    input_variables=['report_text'],
    template="""
        You are a helpful and medically-informed assistant and only speak in json format
        You have given a content below
        `
        {report_text}
        `
        Check if it is a proper medical report or not.
        Your Response should be in pure JSON format with a key "is_medical_report" that is either true or false. No other text or explanation is needed. and no markdown
    """
)

summarize_prompt = PromptTemplate(
    input_variables=['report_text', 'output_format'],
    template="""
        You are a medical data parser and only speak in json format
        
        Given the following medical report text:
        {report_text}
        
        Extract reports and categorise it based on
        - Blood Count
        - Lipid Profile
        - Diabetes
        - Kidney Profile
        - Liver Profile
        - Electrolytes
        - Anemia Studies
        - Thyroid Profile
        - Vitamin Profile
        - Infection Markers
        - Urine Analysis
        - Pancreatic Profile
        - Cardiac Markers
        - Hormonal Panel
        - Others
        
        If category is not found the report don't include that
        
        In json
        - **interpretation** some information of that report in 2-3 lines
        - **summary** based on result whether it is good need attention or anything else.
        - **value** is an array of objects with parameter and value if not found give blank array like []
        
        Strictly output in JSON Only No other text or explanation or no note or markdown is needed
        Output Json format structure is below
        {output_format}
""")

tips_prompt = PromptTemplate(
    input_variables=['test_name', 'summary', 'parameters', 'output_format'],
    template="""
        You are a helpful and medically-informed assistant and only speak in json format
        The user has uploaded a blood report. Below is a section from the report:
        ---
        🧾 Section: {test_name}
        🔍 Summary: {summary}
        📊 Relevant Values: {parameters}
        ---
        
        Please generate 2-3 clear, practical health tips based on this section. Keep them simple and actionable. If values are normal, provide maintenance advice. If abnormal, suggest general lifestyle or dietary changes the user can consider (without offering a diagnosis). Avoid complex medical jargon.
        Your response contains json with a key "tips" that contains an array of tips as string.
        {output_format}
    """
)
