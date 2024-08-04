import ollama

def chat_with_llm(user_message, model_name):
    response = ollama.chat(
        model=model_name,
        messages=[{'role': 'user', 'content': user_message}],
    )
    print(response['message']['content'])   
    return response['message']['content']