import pandas as pd
import streamlit as st
import pdfplumber
from gtts import gTTS
import os
import tempfile

# Create the Streamlit app
st.set_page_config(page_title="PDF to Audio Converter", layout="wide")

# Custom CSS for navigation
st.markdown(
    """
    <style>
    .nav-container {
        display: flex;
        justify-content: space-around;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
    }
    .nav-item {
        font-size: 18px;
        font-weight: bold;
        color: #007bff;
        text-decoration: none;
        margin: 0 10px;
    }
    .nav-item:hover {
        text-decoration: underline;
        color: #0056b3;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Custom Navigation Menu
st.markdown(
    """
    <div class="nav-container">
        <a href="#home" class="nav-item">Home</a>
        <a href="#about" class="nav-item">About</a>
        <a href="#upload-file" class="nav-item">Upload File</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Home section
st.markdown('<div id="home"></div>', unsafe_allow_html=True)
st.title('Welcome to PDF to Audio Converter')

# Create two columns
col1, col2 = st.columns(2)

# Add text in the left column
with col1:
    st.write("Use the navigation bar to switch between sections.")
    st.write("You can upload a PDF file and convert it to an audio file.")
    st.write("Once you've uploaded your file, we'll convert it into an audio file for you.")

# Add an image in the right column
with col2:
    st.image("logo.jpg", caption="Convert PDF to Audio", use_column_width=True)

# About section
st.markdown('<div id="about"></div>', unsafe_allow_html=True)
st.title('About')
st.write('''Experience the future of communication with our cutting-edge text-to-speech technology. 
Transform your written words into captivating audio experiences that resonate with your audience.

Instant Transformation: Watch as your text is seamlessly converted into natural-sounding speech, delivered with precision and clarity.
Unmatched Versatility: From engaging presentations to accessible content, our TTS solution adapts to your every need.
Lifelike Voices: Immerse yourself in a world of authentic voices that bring your message to life.
Global Reach: Break language barriers and connect with audiences worldwide through our diverse range of accents and languages.
Whether you're aiming to enhance accessibility, boost engagement, or simply streamline your workflow, our text-to-speech technology is your ultimate companion.''')

# Upload File section
st.markdown('<div id="upload-file"></div>', unsafe_allow_html=True)
st.title('Upload PDF or TXT File')

# PDF extraction using pdfplumber
def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

# TXT file reader
def extract_text_from_txt(txt_file):
    try:
        return txt_file.read().decode("utf-8")
    except Exception as e:
        st.error(f"Error reading text file: {e}")
        return None

# Save extracted text to CSV
def save_text_to_csv(text, csv_path):
    try:
        df = pd.DataFrame({"Text": [text]})
        df.to_csv(csv_path, index=False)
    except Exception as e:
        st.error(f"Error saving text to CSV: {e}")

# Convert text to speech
def text_to_speech(text, audio_path):
    try:
        tts = gTTS(text)
        tts.save(audio_path)
    except Exception as e:
        st.error(f"Error converting text to speech: {e}")

# File uploader section
uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file is not None:
    # Handle PDF files
    if uploaded_file.name.endswith(".pdf"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(uploaded_file.getvalue())
            temp_file_path = temp_file.name

        extract_text = extract_text_from_pdf(temp_file_path)

    # Handle TXT files
    elif uploaded_file.name.endswith(".txt"):
        extract_text = extract_text_from_txt(uploaded_file)

    if extract_text:
        # Display extracted text
        st.header('Extracted Text')
        st.text_area('Extracted Text from File', extract_text, height=300)

        # Save extracted text to CSV
        csv_file_path = "extracted_text.csv"
        save_text_to_csv(extract_text, csv_file_path)

        # Convert text to speech
        audio_file_path = "text_to_speech.mp3"
        text_to_speech(extract_text, audio_file_path)

        # Read the audio data
        with open(audio_file_path, 'rb') as audio_file:
            audio_data = audio_file.read()

        # Display the audio file
        st.header('Audio File')
        st.audio(audio_data, format='audio/mp3')

        # Create a downloadable audio file
        st.header('Downloadable Audio File')
        st.download_button('Download Audio File', audio_data, file_name='text_to_speech.mp3')

        # Clean up temporary files
        if uploaded_file.name.endswith(".pdf"):
            os.remove(temp_file_path)
        os.remove(audio_file_path)
    else:
        st.error("Failed to extract text from the file. Please check the file and try again.")
