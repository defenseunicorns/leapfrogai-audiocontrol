import openai
openai.api_key = 'Free the models'
openai.api_base = "https://leapfrogai.dd.bigbang.dev"

audio_file= open("/Users/mvanhemert/Desktop/microphone-recording.webm", "rb")
transcript = openai.Audio.translate("whisper-1", audio_file, language="en") # openai.Audio.transcribe("whisper-1", audio_file)
