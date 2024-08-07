from llm import chat_with_llm

def determine_guardrails(user_question, model):
    # Prompt to determine intent
    guardrails_prompt = f'''Role: You are a Prompt Guardrails. If the user's question is identified as illegal or harmful or irrelevant respond "NO" else "YES"\n\nUser Question: {user_question}'''
    guardrails_response = chat_with_llm(guardrails_prompt, model)
    print(guardrails_response)
    if guardrails_response == "NO":
        return "Sorry"
    else:
        return "YES"