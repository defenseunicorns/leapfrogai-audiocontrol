import streamlit as st
from audio_recorder_streamlit import audio_recorder

st.title("Audio Recorder")
audio_bytes = audio_recorder()
if audio_bytes:
    #st.audio(audio_bytes, format="audio/wav")

    wav_file = open("audio.mp3", "wb")
    wav_file.write(audio_bytes)
