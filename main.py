import pandas as pd
import streamlit as st
import pdfplumber
from gtts import gTTS
import os
import tempfile

# Create the Streamlit app
st.set_page_config(page_title="VoiceCraft", layout="wide")

# Custom CSS for styling and responsive design
st.markdown(
    """
    <style>
  
    .stApp {
        background: linear-gradient(270deg, #87CEEB, #4682B4, #1E90FF, #00BFFF);
        background-size: 600% 600%;
        animation: gradientAnimation 20s ease infinite;
    }

    @keyframes gradientAnimation {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .nav-container {
        display: flex;
        justify-content: space-around;
        background-color: #2a007c;
        backdrop-filter: blur(10px);
        padding: 10px;
        border-radius: 50px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        position: -webkit-sticky; /* For Safari */
        position: sticky;
        top: 0;
        z-index: 100;
    }
    .nav-item {
        font-size: 18px;
        font-weight: bold;
        text-decoration: none;
        margin: 0 10px;
        transition: color 0.3s ease;
    }
    .nav-item:hover {
        color: #ffd700;
        transform: scale(1.05);
    }

    [data-testid="stMarkdownContainer"] > p {
      font-size: 20px;
      font-weight: normal;
    }

    [data-testid="stHeader"]{
      background-color: rgba(0, 0, 0, 0);
    }
  

    [data-testid="stImage"] img {
        border-radius: 20px; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }

    [data-testid="stImage"] img:hover {
        transform: scale(1.02);
    }
    .st-emotion-cache-1sno8jx a {
     color: white;
}

    .st-emotion-cache-ltfnpr {
    font-family: "Source Sans Pro", sans-serif;
    font-size: 18px;
    color: white;
    text-align: center;
    margin-top: 0.375rem;
    overflow-wrap: break-word;
    padding: 0.125rem;
    }
    .stButton>button {

        background-color: #007bff;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .stProgress > div > div > div > div {
        background-color: #007bff;
    }
    
    .footer {
        position: fixed;
        left: 0;
        border-radius: 30px 30px 0px 0px;
        bottom: 0;
        width: 100%;
        background-color: #2a007c;
        padding: 10px 0px;
        text-align: center;
        font-size: 14px;
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# Custom Navigation Menu
st.markdown(
    """
    <div class="nav-container">
        <a href="#home" class="nav-item">Home 🏠</a>
        <a href="#about" class="nav-item">About 🌐</a>
        <a href="#upload-file" class="nav-item">Upload File 📜</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Home section
st.markdown('<div id="home"></div>', unsafe_allow_html=True)
st.title('Welcome to VoiceCraft')


# Create two columns
col1, col2 = st.columns(2)

# Add text in the left column
with col1:
    st.write("At VoiceCraft, we believe that every word deserves to be heard. Our cutting-edge text-to-speech technology transforms written content into natural, expressive audio that resonates with clarity and emotion. Whether you're enhancing accessibility, engaging a broader audience, or simply bringing your words to life, VoiceCraft is your trusted partner in the art of spoken communication.")

    st.write("✅ An easy-to-use Text-To-Speech interface, built just for you!")
    st.write("✅ You can upload a PDF or TXT file and convert it to an audio file.")
    st.write("✅ Once you've uploaded your file, we'll convert it into an audio file for you.")

# Add an image in the right column
with col2:
    st.image("logo.jpg", caption="Convert PDF to Audio", use_column_width=True)

# About section
st.markdown('<div id="about"></div>', unsafe_allow_html=True)
st.title('About')

st.write(" Experience the future of communication with our cutting-edge text-to-speech technology. Transform your written words into captivating audio experiences that resonate with your audience.")

st.write(
    """
  - Instant Transformation: Seamlessly convert text into natural-sounding speech with precision.
  -  Unmatched Versatility: Perfect for presentations, e-learning, accessibility, and more.
  -  Lifelike Voices: Choose from a range of voices that bring your content to life.
  -  Global Reach: Break language barriers with diverse accents and languages.
  """
      )

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
    with st.spinner('Processing...'):
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

# Footer section
st.markdown(
    """
    <div class="footer">
        © 2024 VoiceCraft. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)