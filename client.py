from threading import Thread
import speech_recognition as sr
import pyaudio
import Queue
from flask import Flask,request
import requests

app = Flask(__name__)

flag = False
speech = ""
fname = ""

def record():
	r = sr.Recognizer()
	r.pause_threshold = 0.8
	r.dynamic_energy_threshold = True

	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)

	q = Queue.Queue()
	
	def async(func):
		def wrapper(*audio):
			thr = Thread(target = func, args = audio)
			thr.start()
		return wrapper

	@async
	def recognition(audio):
		global speech
		print "uploading...."
		speech = speech + r.recognize_google(audio)
		print speech

	while(True):
		with sr.Microphone() as source:
			print "Recording......"
			audio = r.record(source,duration = 10)
			recognition(audio)
			if flag == False:
				return

@app.route("/msg", methods = ['POST','GET'])
def msg():
	global flag
	global fname
	if request.method == 'GET':
		cmd = request.args.get('cmd')
		#print fname.__class__.__name__
		if cmd == 'start':
			flag = True
			fname = request.args.get('fname')
			#record()
			thr = Thread(target = record)
			thr.start()
			return "Started Recording"
		elif cmd == 'end':
			flag = False
			f = open(str(fname)+".txt",'w')
			f.write(speech)
			f.close()
			return "Ended Recording"

@app.route("/play",methods = ['POST','GET'])
def play():
	if request.method == 'GET':
		name = str(request.args.get('fname'))+".txt"
		f = open(name,'r')
		print name
		return f.read()

app.run(host = "0.0.0.0", port = 5000, debug = True)