**# Project overview**
You are building a social media post generator app, where users can paste text or text files (.pdf, .docx, .md) from which an X or LinkedIn post is created by the OpenAI API according to certain platform- and content specific customizations, which the user will provide.

You will be using Python, Streamlit, the OpenAI API

**# Core functionalities**

Single page application 
1. User provides OpenAI API key in a text field
    1. The app will check whether the API key is valid
    2. The app will display a message to the user whether the API key is valid or not
2. User selects AI model from a dropdown field (gpt-4o-mini, gpt-4o)
3. User provides the text input 
    1a. User inserts the text into a large text field or 
    1b. User drops one or multiple files into a file drop target zone
4. User selects preferences for post generation
    1. User selects platform from dropdown (LinkedIn or X)
    2. User selects post style (factual or creative)
    3. User selects tone (professional or casual)
    4. User selects length in characters (280 for X, 3000 for LinkedIn)
5. User clicks generate button
    1. The app will take the inputs from the fields and generate a prompt for the OpenAI API, based on the following l
    2. The app will call the OpenAI API with the prompt
6. App will display the generated post in a large text field which can be copied to the clipboard

**# Doc**
**## Documentation of how to use the OpenAI API and Streamlit app completions**
CODE EXAMPLE:
```
from openai import OpenAI
import os
import streamlit as st

# Initialize session state variables

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display title and instructions
st.title("Memos-to-Text")
st.markdown("""
## AI-powered Speech-to-Text Transcriptions
            
### What does Memos-to-Text do?
Memos-to-Text processes uploaded audio files, provides a transcription in the chat and enables interaction with it (e.g. summary, extraction of infos, generation of response drafts).
            
### How to use it:
- **Step 1 | Input parameters**: Provide your OpenAI API key, potentially make changes to the pre-selected parameters. More context by hovering about the info sign of each input field. 
- **Step 2 | Upload Files and Receive Transcription**: Upload your audio files (mp3, wav, m4a) to trigger the transcription, which will be displayed in the chat interface.
- **Step 3 | Ask Questions**: Interact with the transcriptions (e.g. summarize, provide response, ask ChatGPT for advice on the content).
- **Important Note**: All inputs are saved in the session state, so you don't have to re-input them. They will, however, be deleted once you close the app.
            

---
""")

# API Key input field
api_key_input = st.text_input(
    "Enter OpenAI API key",
    type="password",
    help="Enter your OpenAI API key to use the application"
)

# Update session state if API key changed
if api_key_input:
    st.session_state.openai_api_key = api_key_input
    # Initialize OpenAI client with provided API key
    try:
        
        client = OpenAI(api_key=api_key_input)  # Simplified client initialization
        
        # Test the connection with a lightweight API call
        client.models.list()
        st.success("✅ API key is valid --> Now upload an audio file and let the transcription be done for you!")
        
    except Exception as e:
        error_message = str(e)
        if "auth" in error_message.lower():
            st.error("❌ Invalid API key. Please check your key and try again.")
        else:
            st.error(f"❌ Error connecting to OpenAI: {error_message}")
        client = None


    # Model configuration
    col1, col2 = st.columns(2)
    with col1:
        model_name = st.selectbox(
            "Large Language Model (LLM)", 
            ["gpt-4o", "gpt-4o-mini"],
            index=0,
            help="""
            The model to use for the LLM. 
            gpt-4o is the most recent general model. 
            gpt-4o-mini is its more lightweight and cost effective alternative."""
        )
    with col2:
        temperature = st.slider(
            "Temperature", 
            min_value=0.0, 
            max_value=1.0, 
            value=0.1, 
            step=0.1,
            help="Temperature controls randomness in responses. Lower values are more focused and deterministic. 0.1 is a good value for most cases."
        )

    # File upload and transcription section
    audio_file = st.file_uploader(
        "Upload an audio file", 
        type=['mp3', 'wav', 'm4a']
    )

    # Transcription button
    if st.button("Start Transcription"):
        if audio_file is None:
            st.error("Please upload an audio file first.")
        elif client is None:
            st.error("OpenAI client not initialized. Please check your API key configuration.")
        else:
            with st.spinner(f"Processing {audio_file.name}..."):
                try:
                    # Transcribe the audio file directly from memory
                    transcript = client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file
                    )
                    
                    # Format the transcription message with clear separation
                    transcribed_text = f"""Transcription: {transcript.text}"""
                    
                    # Add transcription to messages as assistant message
                    st.session_state.messages.append({"role": "assistant", "content": transcribed_text})
                    st.session_state.messages.append({"role": "assistant", "content": """This is the transcription of your audio file. I can do many things with it: \n(1) summarize it, \n(2) extract information, \n(3) generate a response draft \n(4) ask ChatGPT for advice on the content, \n(5) ... you name it! \nWhat would you like me to do with this transcription - pick a number or write your own prompt!"""})
                 

                    
                except Exception as e:
                    st.error(f"Error processing audio file: {str(e)}")

    # Display chat history (this will show the transcription once)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input and response
    prompt = st.chat_input("What would you like to know about the transcription?")
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                temperature=temperature,
                stream=True,
            )
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})


else:
    st.warning("⚠️ Please enter your OpenAI API key to use the application")
    client = None
```

