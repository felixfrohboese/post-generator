import streamlit as st
from openai import OpenAI
import docx
import PyPDF2
import io
import os

def load_specifications():
    """Load all specification and example files from platform_specs folder."""
    specs = {}
    files = {
        'linkedin_structure': 'platform_specs/linkedin_structure_specs.txt',
        'x_structure': 'platform_specs/x_structure_specs.txt',
        'linkedin_examples': 'platform_specs/linkedin_examples.txt',
        'x_examples': 'platform_specs/x_examples.txt'
    }
    
    for key, filename in files.items():
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                specs[key] = file.read().strip()
        except FileNotFoundError:
            st.warning(f"Warning: {filename} not found. Some features may be limited.")
            specs[key] = ""
    
    return specs

# Load specifications at startup
SPECIFICATIONS = load_specifications()

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
    ["gpt-4o-mini", "gpt-4o", "o1-mini", "o1-preview"],
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
    tone = st.selectbox(
        "Tone",
        ["Professional (factual)", "Casual (creative)"],
        help="Select the tone and style for your post"
    )

with col2:
    emoji_usage = st.selectbox(
        "Emoji Usage",
        ["None", "Few", "Many"],
        help="Select how many emojis should be used in the post"
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
            # Get platform-specific specifications and examples
            structure_specs = SPECIFICATIONS[f'{platform.lower()}_structure']
            examples = SPECIFICATIONS[f'{platform.lower()}_examples']
            
            prompt = f"""
            Create a {platform} post based on the following text.
            
            Platform-specific structure requirements:
            {structure_specs}
            
            Reference examples for this platform:
            {examples}
            
            Tone and Style: {tone}
            Maximum length: {max_length} characters
            Emoji usage: {emoji_usage}

            Original text:
            {text_content}

            Rules:
            1. Keep the post within {max_length} characters
            2. Use the specified tone and style:
               - For "Professional (factual)": Keep it formal and fact-based
               - For "Casual (creative)": Be more conversational and creative
            3. Format it appropriately for {platform} following the structure requirements above
            4. Use the reference examples as inspiration for structure and style
            5. For emoji usage:
               - If "None": Don't use any emojis
               - If "Few": Use 1-3 relevant emojis strategically placed
               - If "Many": Use 4-8 relevant emojis throughout the post
            """

            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": prompt}],
                    #temperature=0.7 # commented out since o1 models cannot be adjusted with temperature
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