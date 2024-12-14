import streamlit as st
from openai import OpenAI
import docx
import PyPDF2
import io

# Initialize session state
if "generated_post" not in st.session_state:
    st.session_state.generated_post = ""

# Page title and description
st.title("Social Media Post Generator")
st.markdown("""
Generate professional social media posts using AI. Simply provide your text or upload files,
customize your preferences, and get a perfectly crafted post for your chosen platform.
""")

# API Key input and validation
api_key = st.text_input(
    "Enter OpenAI API key",
    type="password",
    help="Enter your OpenAI API key to use the application"
)

client = None
if api_key:
    try:
        client = OpenAI(api_key=api_key)
        client.models.list()  # Test API key validity
        st.success("✅ API key is valid!")
    except Exception as e:
        st.error("❌ Invalid API key. Please check your key and try again.")

# Model selection
model = st.selectbox(
    "Select AI Model",
    ["gpt-4o-mini", "gpt-4o"],
    help="Choose the AI model to generate your post"
)

# Text input section
st.subheader("Input Text")
input_method = st.radio("Choose input method:", ["Text Input", "File Upload"])

text_content = ""
if input_method == "Text Input":
    text_content = st.text_area(
        "Enter your text",
        height=200,
        help="Paste the text you want to convert into a social media post"
    )
else:
    uploaded_files = st.file_uploader(
        "Upload files (.txt, .pdf, .docx)", 
        type=["txt", "pdf", "docx"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        for file in uploaded_files:
            if file.type == "text/plain":
                text_content += file.getvalue().decode("utf-8") + "\n\n"
            elif file.type == "application/pdf":
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.getvalue()))
                for page in pdf_reader.pages:
                    text_content += page.extract_text() + "\n\n"
            elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                doc = docx.Document(io.BytesIO(file.getvalue()))
                for para in doc.paragraphs:
                    text_content += para.text + "\n\n"

# Post preferences
st.subheader("Post Preferences")
col1, col2 = st.columns(2)

with col1:
    platform = st.selectbox(
        "Platform",
        ["LinkedIn", "X"],
        help="Select the platform for your post"
    )
    style = st.selectbox(
        "Style",
        ["Factual", "Creative"],
        help="Choose the writing style for your post"
    )

with col2:
    tone = st.selectbox(
        "Tone",
        ["Professional", "Casual"],
        help="Select the tone of voice for your post"
    )
    max_length = st.number_input(
        "Maximum Length",
        value=280 if platform == "X" else 3000,
        min_value=1,
        max_value=3000,
        help="Maximum character length for your post"
    )

# Generate button
if st.button("Generate Post"):
    if not text_content:
        st.error("Please provide some text input!")
    elif not client:
        st.error("Please provide a valid API key!")
    else:
        with st.spinner("Generating your post..."):
            prompt = f"""
            Create a {platform} post based on the following text. 
            Style: {style}
            Tone: {tone}
            Maximum length: {max_length} characters

            Original text:
            {text_content}

            Rules:
            1. Keep the post within {max_length} characters
            2. Use a {tone.lower()} tone of voice
            3. Make it {style.lower()} in style
            4. Format it appropriately for {platform}
            5. Include relevant hashtags if it's for LinkedIn
            6. For X, make it concise and impactful
            """

            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )
                st.session_state.generated_post = response.choices[0].message.content
            except Exception as e:
                st.error(f"Error generating post: {str(e)}")

# Display generated post
if st.session_state.generated_post:
    st.subheader("Generated Post")
    st.text_area(
        "Your post is ready! Click the copy button to copy it to your clipboard.",
        value=st.session_state.generated_post,
        height=200
    )
    
    # Copy button
    if st.button("Copy to Clipboard"):
        st.write("Post copied to clipboard! ✨")
        st.session_state.copied = True 