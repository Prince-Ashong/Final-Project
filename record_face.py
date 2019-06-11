import cv2
import numpy as np 
import sqlite3
import os
import tkinter as tk
conn = sqlite3.connect('database.db')
c = conn.cursor()
if not os.path.exists('./dataset'):
    os.makedirs('./dataset')

root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())
lmain = tk.Label(root)
lmain.pack()
label=tk.Label(text='Enter your name')
label.pack(side=tk.TOP,padx=10,pady=10)
entry = tk.Entry(root, width=10)
entry.pack(side=tk.TOP,padx=10,pady=10)

def yes():
	face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
	cap = cv2.VideoCapture(1)
	uname = entry.get()
	c.execute('INSERT INTO users (name) VALUES (?)', (uname,))


	uid = c.lastrowid
	sampleNum = 0
	while True:
  		ret, img = cap.read()
  		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  		faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  		for (x,y,w,h) in faces:
  			sampleNum = sampleNum+1
  			cv2.imwrite("dataset/User."+str(uid)+"."+str(sampleNum)+".jpg",gray[y:y+h,x:x+w])
  			cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
  			cv2.waitKey(100)
  		cv2.imshow('img',img)
  		cv2.waitKey(1);
  		if sampleNum > 5:
  			break
	cap.release()
	conn.commit()

	cv2.destroyAllWindows()
click_button = tk.Button(master=root, text='take', command=yes)
click_button.pack()

#click_button = tk.Button(master=root, text='Click', command=call)
#click_button.pack()

root.mainloop()