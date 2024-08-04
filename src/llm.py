import ollama

def llm(user_message, model_name):
    response = ollama.chat(
        model=model_name,
        messages=[{'role': 'user', 'content': user_message}],
    )
    print(response['message']['content'])   
    return response['message']['content']