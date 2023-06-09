import openai
import datefinder
import locationtagger
import nltk
import spacy

openai.api_key = 'Free the models'
openai.api_base = "https://leapfrogai.dd.bigbang.dev"

audio_file= open("audio.mp3", "rb")
transcript = openai.Audio.translate("whisper-1", audio_file, language="en") # openai.Audio.transcribe("whisper-1", audio_file)
print(transcript)

place_entity = locationtagger.find_locations(text = transcript.text)

# Find any states mentioned in the transcript
if len(place_entity.regions) > 0:
    print("The states listed:", place_entity.regions)

dates_found_generator = datefinder.find_dates(transcript.text)
dates_found = list(dates_found_generator)
if len(dates_found) > 0:
    print("The dates found", list(dates_found))