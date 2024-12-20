# Post Generator

Post Generator is a AI-based Streamlit application that transforms text inputs into professionally crafted social media posts for LinkedIn and X (formerly Twitter) using OpenAI's GPT models.

## Features ✨

- 📝 Multiple text input methods:
  - Direct text input
  - File upload support (txt, pdf, docx)
  - Multi-file processing
- 🎯 Platform-specific optimization:
  - LinkedIn posts (up to 3000 characters)
  - X posts (up to 280 characters)
- ⚙️ Customizable post preferences:
  - Professional or casual tone
  - Adjustable emoji usage (None/Few/Many)
  - Platform-specific formatting
- 🤖 Advanced AI Models:
  - Support for multiple GPT models (gpt-4o, gpt-4o-mini, o1-mini, o1-preview)
- 📋 Easy-to-use interface:
  - One-click post generation
  - Copy to clipboard functionality
- 🔒 Secure API key handling

## Prerequisites 🛠️

- Python 3.11
- OpenAI API key
- Streamlit
- OpenAI Python package
- python-docx
- PyPDF2

## Installation 💻

1. Clone this repository:
```bash
git clone https://github.com/felixfrohboese/post-generator.git
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```


## Usage 📱

1. **API Key Setup** 🔑
   - Enter your OpenAI API key in the designated field
   - The application will validate your key before proceeding

2. **Select AI Model** 🤖
   - Choose from available models (gpt-4o, gpt-4o-mini, o1-mini, o1-preview)

3. **Input Content** 📝
   - Choose between direct text input or file upload
   - Supported file formats: .txt, .pdf, .docx
   - Multiple files can be uploaded simultaneously

4. **Configure Post Preferences** ⚙️
   - Select target platform (LinkedIn or X)
   - Choose tone (Professional/Casual)
   - Set emoji usage level
   - Adjust maximum length (auto-set based on platform)

5. **Generate and Copy** ✨
   - Click "Generate Post" to create your content
   - Use "Copy to Clipboard" to easily transfer the generated post

## Important Notes ⚠️

- All inputs are processed in the current session
- The application requires an active internet connection
- API usage is subject to OpenAI's pricing and usage policies
- Platform-specific formatting is automatically applied

## Technical Details 🔧

- Built with Streamlit for the web interface
- Integrates with OpenAI's GPT models
- Supports multiple document formats
- Implements platform-specific content guidelines
- Uses reference examples for improved output quality

## Privacy & Security 🔒

- API keys are handled securely and not stored
- File processing is done in-memory
- No data is retained after the session ends

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.