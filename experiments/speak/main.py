import gtts
# from playsound import playsound

tts = gtts.gTTS("Hello world")

tts.save("hello.mp3")
# playsound("hello.mp3")