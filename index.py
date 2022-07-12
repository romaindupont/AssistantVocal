from vosk import Model, KaldiRecognizer
import speech_recognition
import pyttsx3
import wave
import json
import os

def play_greetings():
	return

def play_farewell_and_quit():
	return

def search_for_term_on_youtube(*args: tuple):
	if not args[0]: 
		return 
		search_term = " ".join(args[0])
		url = "https://www.youtube.com/results?search_query=" + search_term
		webbrowser.get().open(url)
		play_voice_assistant_speech("Here is what I found for " + search_term + "on youtube")

def search_for_term_on_google():
	return
def search_fordefinition_on_wikipedia():
	return
def get_translation():
	return
def change_language():
	return
def get_weather_forecast():
	return
commands = {
		("hello", "hi", "morning", ""): play_greetings,
		("bye", "goodbye", "quit", "exit", "stop", ""): play_farewell_and_quit
,
("search", "google", "find", ""): search_for_term_on_google,
("video", "youtube", "watch", ""): search_for_term_on_youtube,
("wikipedia", "definition", "about", "", ""): search_fordefinition_on_wikipedia,
("translate", "interpretation", "translation", "","",""): get_translation,
("language", ""): change_language,
("weather", "forecast", "", ""): get_weather_forecast,}

class VoiceAssistant:
	name = ""
	sex = ""
	speech_language = ""
	recognition_language = ""


def setup_assistant_voice():
	voices = ttsEngine.getProperty("voices")
	if assistant.speech_language == "fr":
		assistant.recognition_language = "fr-FR"
		if assistant.sex == "female":
			ttsEngine.setProperty("voice", voices[1].id)
		else:
			ttsEngine.setProperty("voice", voices[2].id)
	else:
		assistant.recognition_language = "fr-FR"
		ttsEngine.setProperty("voice", voices[0].id)


def play_voice_assistant_speech(text_to_speech):
	ttsEngine.say(str(text_to_speech))
	ttsEngine.runAndWait()

def record_and_recognize_audio(*args: tuple):
	with microphone:
		recognized_data = ""
		recognizer.adjust_for_ambient_noise(microphone, duration=2)
		try:
			print("Listening...")
			audio = recognizer.listen(microphone, 5, 5)
			with open("microphone-results.wav", "wb") as file:
				file.write(audio.get_wav_data())
		except speech_recognition.WaitTimeoutError:
			print("Check if the microphone is on, please ?")
			return 
		try: 
			print("started recognition ...")
			recognized_data = recognizer.recognize_google(audio, language="fr").lower()
		except speech_recognition.UnknownValueError:
			pass
		except speech_recognition.RequestError:
			print("try to use offline recognition...")
			recognized_data = use_offline_recognition()
			return recognized_data

def use_offline_recognition():
	recognized_data = ""
	try:
		if not os.path.exists("models/vosk-model-small-fr-0.4"):
			print("Please download model from: \n" "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder")
			exit(1)
		wave_audio_file = wave.open("microphone-results.wav", "rb")
		model = Model("models/vosk-model-small-fr-0.4")
		offline_recognizer = KaldiRecognizer(model, wave_audio_file.getframerate())
		data = wave_audio_file.readframes(wave_audio_file.getnframes())
		if len(data) > 0:
			if offline_recognizer.AcceptWaveform(data):
				recognized_data = offline_recognizer.Result()
				recognized_data = json.loads(recognized_data)
				recognized_data = recognized_data["text"]
	except:
		print("Speech service is unavailable, try later")
		return recognized_data
		
def execute_command_with_name(command_name: str, *args: list):
	for key in commands.keys():
		if command_name in key:
			commands[key](*args)
		else:
			pass


if __name__ == "__main__":
	recognizer = speech_recognition.Recognizer()
	microphone = speech_recognition.Microphone()
	ttsEngine = pyttsx3.init()
	assistant = VoiceAssistant()
	assistant.name = "Alice"
	assistant.sex = "female"
	assistant.speech_language = "fr"
	setup_assistant_voice()
	while True:
		voice_input = record_and_recognize_audio()
		os.remove("microphone-results.wav")
		print(voice_input)
		voice_input = voice_input.split(" ")
		command = voice_input[0]
		command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
		execute_command_with_name(command, command_options)


