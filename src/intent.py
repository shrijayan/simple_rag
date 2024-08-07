from llm import chat_with_llm

def determine_intent(user_question, model):
    # Prompt to determine intent
    intent_prompt = f'''Role: You are a Intent Classifier. If the user's question is identified as a general question like "Hi", "Hello", "Thank you", "Good Bye", or any general question like which will used in starting of the conversation return "LLM"; else return "RAG". Your input will be the user question and your output will be "LLM" or "RAG" based on the question.\n\nUser Question: {user_question}'''
    intent_response = chat_with_llm(intent_prompt, model)
    return intent_response