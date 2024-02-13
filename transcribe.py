import streamlit as st
from google.cloud import speech_v1p1beta1 as speech
import os

# Set up Google Cloud credentials (replace 'path_to_service_account_key.json' with your own key file)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account_key.json"

# Create a client for the Google Cloud Speech-to-Text API
client = speech.SpeechClient()

# Function to transcribe speech from audio file
def transcribe_speech(audio_file, accent):
    with st.spinner("Transcribing speech..."):
        # Load audio file
        with open(audio_file, "rb") as file:
            content = file.read()

        # Configure speech recognition request
        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.MP3,
            sample_rate_hertz=16000,
            language_code="en-IN",
            use_enhanced=True,
            model="default",
            metadata={"interaction_type": "DISCUSSION"},
            diarization_config=speech.SpeakerDiarizationConfig(
                enable_speaker_diarization=True,
                min_speaker_count=2,
                max_speaker_count=6,
            ),
        )

        # Specify accent hint if provided
        if accent:
            config.speech_contexts[0].phrases.append(accent)

        # Perform speech recognition
        response = client.recognize(config=config, audio=audio)

        # Extract and return transcriptions
        transcriptions = [result.alternatives[0].transcript for result in response.results]
        return "\n".join(transcriptions)

# Streamlit app
def main():
    st.title("Speech-to-Text Transcription")
    st.write("Upload an audio file to transcribe.")

    # File upload
    audio_file = st.file_uploader("Upload Audio File", type=["mp3", "wav"])

    # Accent selection
    accent = st.text_input("Accent (Optional)")

    # Transcription button
    if st.button("Transcribe"):
        if audio_file is not None:
            # Save the uploaded file temporarily
            temp_file = os.path.join(".", audio_file.name)
            with open(temp_file, "wb") as file:
                file.write(audio_file.getbuffer())
            # Perform transcription
            transcription = transcribe_speech(temp_file, accent)
            # Display the transcription
            st.success("Transcription:")
            st.write(transcription)
            # Delete the temporary file
            os.remove(temp_file)
        else:
            st.error("Please upload an audio file.")

if __name__ == "__main__":
    main()
