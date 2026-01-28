import streamlit as st
from pypdf import PdfReader 
import os
from dotenv import load_dotenv
from groq import Groq
import csv
from io import StringIO 

load_dotenv()

# --- 1. File Processing (Now keeps files separate) ---
def get_files_text(uploaded_files):
    file_contents = []
    
    for file in uploaded_files:
        file_name = file.name.lower()
        text = ""
        try:
            if file_name.endswith('.pdf'):
                pdf_reader = PdfReader(file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            elif file_name.endswith('.csv'):
                content = file.getvalue().decode("utf-8")
                csv_file = StringIO(content)
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    text += " ".join(row) + "\n"
            
            if text:
                file_contents.append(text)
                
        except Exception as e:
            st.error(f"Error reading file '{file.name}': {e}")
            continue 
            
    return file_contents

# --- 2. Smart Context Search (The "Equal Opportunity" Fix) ---
def find_relevant_context(file_contents, user_question):
    """
    Search EVERY file individually to find the best match in each.
    Then combine them.
    """
    question_words = set(user_question.lower().split())
    best_chunks_from_all_files = []

    for file_text in file_contents:
        chunks = file_text.split('\n\n')
        if len(chunks) < 3: 
            chunks = [file_text[i:i+1000] for i in range(0, len(file_text), 1000)]
        scored_chunks = []
        for chunk in chunks:
            score = 0
            chunk_lower = chunk.lower()
            for word in question_words:
                if word in chunk_lower and len(word) > 3:
                    score += 1
            scored_chunks.append((score, chunk))
        
        scored_chunks.sort(key=lambda x: x[0], reverse=True)
        
        if scored_chunks:
            best_chunks_from_all_files.append(scored_chunks[0][1])
            if len(scored_chunks) > 1:
                best_chunks_from_all_files.append(scored_chunks[1][1]) 

    final_context = "\n---\n".join(best_chunks_from_all_files)
    
    return final_context[:10000]

# --- 3. The Direct Intelligence ---
def get_groq_response(context_text, user_question):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Answer strictly based on the context provided."
            },
            {
                "role": "user",
                "content": f"Context:\n{context_text}\n\nQuestion: {user_question}"
            }
        ]

        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.1-8b-instant",
            temperature=0.5,
        )

        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"Error communicating with Groq: {e}"

# --- 4. THE UI ---
def main():
    st.set_page_config(page_title="DocuChat", page_icon="📄")

    with st.sidebar:
        st.title("📄 DocuChat")
        st.write("Upload PDFs or CSVs to chat.")
        
        uploaded_files = st.file_uploader(
            "Upload Files", 
            accept_multiple_files=True, 
            type=['pdf', 'csv']
        )
        
        if st.button("Start Processing"):
            if not uploaded_files:
                st.warning("Upload a file first.")
            else:
                with st.spinner("Analyzing..."):
                    file_contents = get_files_text(uploaded_files)
                    if file_contents:
                        st.session_state.file_contents = file_contents
                        st.success("Ready to Chat!")
                    else:
                        st.warning("No text found.")

        if "file_contents" in st.session_state and st.session_state.file_contents:
            st.divider()
            if st.button("Clear History"):
                st.session_state.messages = []
                st.rerun()

    st.title("Chat with your Data")

    if "file_contents" not in st.session_state:
        st.session_state.file_contents = [] 
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display History
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input Bar
    if prompt := st.chat_input("Ask a question..."):
        
        if not st.session_state.file_contents:
            st.error("Please upload a file in the sidebar first.")
        else:
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    relevant_text = find_relevant_context(st.session_state.file_contents, prompt)
                    response = get_groq_response(relevant_text, prompt)
                    st.markdown(response)
                    
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()