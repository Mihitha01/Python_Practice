#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

import requests
import time

# Hugging Face Inference API endpoint
API_URL = "https://api-inference.huggingface.co/models/TheBloke/Nous-Hermes-13b-GPTQ"

# Replace with your free Hugging Face API token
headers = {"Authorization": "Bearer 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"}

def chat_with_gpt(prompt):
    payload = {
        "inputs": f"User: {prompt}\nAssistant:",
        "parameters": {"max_new_tokens": 200, "temperature": 0.7}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=60)
        data = response.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"].split("Assistant:")[-1].strip()
        elif "error" in data:
            return f"Error from API: {data['error']}"
        else:
            return "Sorry, I couldn’t generate a response."
    except requests.exceptions.Timeout:
        return "Error: Model is taking too long to respond. Try again."
    except Exception as e:
        return f"Unexpected error: {e}"

if __name__ == "__main__":
    print("💬 Chatbot is ready! Type 'quit', 'exit', or 'bye' to stop.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            print("Chatbot: Goodbye! 👋")
            break

        response = chat_with_gpt(user_input)
        print("Chatbot:", response)
        time.sleep(1)  # small pause for readability

