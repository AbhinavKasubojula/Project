import streamlit as st
import requests
import json

# Function to generate response from the model (using your existing logic)
def generate_response(cx, q):
    # Retrieved text as context from Pinecone
    retrieved_text = cx

    # Prepare the prompt for the Llama 3 model
    question = q
    prompt = f"Here is some context:\n{retrieved_text}\n\nBased on this, can you answer the following question: {question}"

    # Ollama API call to generate a response
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "llama3.1:latest",
        "prompt": prompt,
        "stream": False  # Disable streaming
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check the response from the model
    if response.status_code == 200:
        result = response.json()
        return result['response']
    else:
        return "Error: Could not retrieve response."

# Function to handle the correction prompt
def handle_correction():
    correction = st.text_input("Please provide your correction prompt:")
    if st.button("Submit Correction"):
        st.write(f"You submitted the correction: {correction}")
        # Logic to handle correction, such as sending it back to the model

# Main Streamlit app
def app():
    st.title("Interactive Model Response")

    # Input for the question and context (you can pull this dynamically)
    context = st.text_area("Context from Pinecone", value="Here is some sample context.", height=150)
    question = st.text_input("Enter your question", value="Do you remember your last 3 responses?")

    if st.button("Get Response"):
        # Generate response from the model
        response = generate_response(context, question)
        st.write(f"Model Response: {response}")

        # Display the options after the response
        st.write("What would you like to do?")
        option = st.radio(
            "Select an option:",
            ('I\'m okay with the answer', 'Give a prompt to correct answer', 'Skip to next question')
        )

        if option == 'I\'m okay with the answer':
            st.write("You accepted the answer.")
            # Logic for accepting the answer, e.g., moving to the next question
        elif option == 'Give a prompt to correct answer':
            handle_correction()  # Call the correction handler function
        elif option == 'Skip to next question':
            st.write("You skipped to the next question.")
            # Logic for skipping to the next question

if __name__ == "__main__":
    app()
