import tkinter as tk
from tkinter import filedialog, Text
from jumpssh import SSHSession
from functools import partial
from PIL import ImageTk, Image
import os

root = tk.Tk()
root.title("GUI DeterLab")
root.resizable(False, False)

def sshToNode(nodeName):
	yourCommand = 'ssh -t ' + entryUsername.get() + '@users.isi.deterlab.net \'ssh ' + nodeName + '.' + entryExperiment.get() + '.' + entryProject.get() + '\''
	tell.app( 'Terminal', 'do script "' + yourCommand + '"')


def login():

	for widget in frame.winfo_children():
		widget.destroy()
	
	gatewaySession = SSHSession('users.isi.deterlab.net', entryUsername.get(), password=entryPassword.get()).open()
	ltmap = gatewaySession.get_cmd_output('cat /proj/' + entryProject.get() + '/exp/' + entryExperiment.get() + '/tbdata/ltmap')

	if not os.path.isfile('img/' + entryExperiment.get()  + '.png'):
		gatewaySession.get(remote_path='/proj/' + entryProject.get() + '/exp/' + entryExperiment.get() + '/tbdata/' + entryExperiment.get() + '.png', local_path='img/')

	experimentLabel = tk.Label(frame, text="Experiment: " + entryExperiment.get() + " Project: " + entryProject.get(), bg="white", pady=30)
	experimentLabel.pack()

	for line in ltmap.split('\n'):
		#check if first character is h
		count = 1
		if line[0] == 'h':
			nodeName=line[line.find(' ')+1:-1]

			label = tk.Label(frame, text="Node " + nodeName, bg="gray")
			label.pack()

			buttonNew = tk.Button(
				frame,
				text="Login to " + nodeName,
				width=15,
				padx=10,
				pady=5,
				#height=5
				command=partial(sshToNode, nodeName)
			)

			buttonNew.pack()

	topologyLabel = tk.Label(frame, text="Topology image:", pady=5)
	topologyLabel.pack()

	image = Image.open("img/" + entryExperiment.get() + ".png")
	img = ImageTk.PhotoImage(image)
	panel = tk.Label(frame, image=img)
	panel.pack()

	root.mainloop()


canvas = tk.Canvas(root, height=600, width=700, bg="#8F0000")
canvas.pack()

frame = tk.Frame(root, bg="white")
frame.place(width=550, height=550, relx=0.1, rely=0.05)

labelUsername = tk.Label(root, text="Username:", padx=10, pady=5, width=20, anchor='w')
entryUsername = tk.Entry()

labelPassword = tk.Label(root, text="Password:", padx=10, pady=5, width=20, anchor='w')
entryPassword = tk.Entry(show='*')

labelProject = tk.Label(root, text="Project:", padx=10, pady=5, width=20, anchor='w')
entryProject = tk.Entry()

labelExperiment = tk.Label(root, text="Experiment:", padx=10, pady=5, width=20, anchor='w')
entryExperiment = tk.Entry()

labelUsername.pack()
entryUsername.pack()

labelPassword.pack()
entryPassword.pack()

labelProject.pack()
entryProject.pack()

labelExperiment.pack()
entryExperiment.pack()

button = tk.Button(
	root,
	text="Log in",
	padx=10,
	pady=10,
	command=login
	)

button.pack()

root.mainloop()
