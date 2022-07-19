from vosk import Model, KaldiRecognizer
import speech_recognition
import pyttsx3
import wave
import json
import os
import webbrowser
from datetime import date

def play_greetings(*args: tuple):
	if args[0]:
		print('play_greetings')
	else:
		pass

def time_to_quit(*args: tuple):
	if args[0]:
		today = date.today()
		d1 = date(2022, 9, 9)
		delta = d1 - today
		play_voice_assistant_speech("Nicolas il te reste exactement " + str(delta) + "jours avant ton départ")
	else:
		pass

def search_for_term_on_youtube(*args: tuple):
	if args[0]: 
		search_term = " ".join(args[0])
		print(search_term)
		url = "https://www.youtube.com/results?search_query=" + search_term
		webbrowser.get().open(url)
		play_voice_assistant_speech("Here is what I found for " + search_term + "on youtube")
	else:
		pass

def search_for_term_on_google(*args: tuple):
	if args[0]:
		print('google')
	else:
		pass

def search_fordefinition_on_findchip(*args: tuple):
	if args[0]: 
		search_term = " ".join(args[0])
		print(search_term)
		url = "https://www.findchips.com/search/" + search_term
		webbrowser.get().open(url)
		play_voice_assistant_speech("Here is what I found for " + search_term + "on findchip")
	else:
		pass


def get_translation(*args: tuple):
	if args[0]:
		print('translate')
	else:
		pass

def change_language(*args: tuple):
	if args[0]:
		print('change')
	else:
		pass

def get_weather_forecast(*args: tuple):
	if args[0]:
		print('weather')
	else:
		pass

def takeNote(*args: tuple):
	if args[0]:
		fileDir = os.getcwd()
		noteFile = open(fileDir+"\\copy.txt", "a")
		for line in args:
			essai = str(line).strip('[]')
			essai1 = essai.replace(",","")
			essai2 = essai1.replace("'","")
			noteFile.write(essai2)
	else:
		pass


commands = {
	("hello", "hi", "morning", ""): play_greetings,
	("bye", "salut", "au revoir", "exit", "stop", ""): time_to_quit,
	("search", "google", "find", ""): search_for_term_on_google,
	("video", "youtube", "watch", "voir"): search_for_term_on_youtube,
	("findchip", "chercher", "composant", "find", ""): search_fordefinition_on_findchip,
	("translate", "interpretation", "translation", "", "", ""): get_translation,
	("language", ""): change_language,
	("weather", "forecast", "", ""): get_weather_forecast,
	("note", "noter", "", ""): takeNote
}

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
		voice_input = voice_input.split(" ")
		command = voice_input[0]
		command_options = [str(input_part) for input_part in voice_input[1:len(voice_input)]]
		execute_command_with_name(command, command_options)


