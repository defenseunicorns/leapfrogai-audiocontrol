import streamlit as st
from audio_recorder_streamlit import audio_recorder

st.title("Plot Data with Your Voice!")
audio_bytes = audio_recorder(
    text="Click the Robot and Start Talking",
    recording_color="#0000CD",
    neutral_color="#87CEFA	",
    icon_name="robot",
    icon_size="6x",
)
if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

    #wav_file = open("audio.mp3", "wb")
    #wav_file.write(audio_bytes)

    # post the bytes `audio_bytes` to the openai REST endpoint
    
