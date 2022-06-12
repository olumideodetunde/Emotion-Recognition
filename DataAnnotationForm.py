# import openpyxl and tkinter modules
import os
from tkinter.messagebox import QUESTION
from openpyxl import *
from tkinter import *
from playsound import playsound
from datetime import datetime

#Function to compile sounds
def compile_sounds(dir_path):
	extension = (".wav")
	sound = []
	for files in os.listdir(dir_path):
		if files.endswith(extension):
			sound.append(files)
		else:
			pass
	return sound

# globally declare wb and sheet variable and opening the existing excel file
wb = load_workbook('./Excel Database 2.xlsx')
sheet = wb.active

# create global variables
file_path = "./IADS-E/IADS-E sound stimuli (IADS-2 is not included)/Animal/Block 1"
idx = 0  #counter
start_time = None #timestamp
end_time = None #timestamp
sound_list = compile_sounds(file_path)
emotion = None #widget
emotion_rating = None #widget

#Function for excel to handle excel dimension and headers
def excel():
	# resize the width of columns in excel spreadsheet
	sheet.column_dimensions['A'].width = 30
	sheet.column_dimensions['B'].width = 30
	sheet.column_dimensions['C'].width = 30
	sheet.column_dimensions['D'].width = 30
	sheet.column_dimensions['E'].width = 30
	sheet.column_dimensions['F'].width = 30

	# write given data to an excel spreadsheet at particular location
	sheet.cell(row=1, column=1).value = "SoundID"
	sheet.cell(row=1, column=2).value = "Starttime"
	sheet.cell(row=1, column=3).value = "Emotion"
	sheet.cell(row=1, column=4).value = "Emotionrating"
	sheet.cell(row=1, column=5).value = "Endtime"
	sheet.cell(row=1, column=6).value = "UserID"

# Functions to take data from GUI window and write to an excel file
def insert():
	print("Insert")
	global start_time
	global end_time
	global idx
	global emotion, emotion_rating
	end_time = get_end_time()

	# assigning the max row and max column value upto which data is written in an excel sheet to the variable
	current_row = sheet.max_row
	current_column = sheet.max_column

	# get method returns current text as string which we write into excel spreadsheet at particular location
	sheet.cell(row=current_row + 1, column=1).value = sound_list[idx]
	sheet.cell(row=current_row + 1, column=2).value = start_time
	sheet.cell(row=current_row + 1, column=3).value = emotion.get()
	sheet.cell(row=current_row + 1, column=4).value = emotion_rating.get()
	sheet.cell(row=current_row + 1, column=5).value = end_time
	sheet.cell(row=current_row + 1, column=6).value = user_id_field.get()

	# save the file
	wb.save('./Excel Database 2.xlsx')

	#update the id and refresh screen or end program
	idx += 1
	if idx <= len(sound_list):
		print('continue to the next question')
		refresh_screen(idx)
	else:
		# inform user that program will be exiting
		# if possible exit your your program here
		print('end program')
		
	#Function to refresh screen
def refresh_screen(question_idx):
	update_number = 1
	emotion_rating.set("(How intensely?)") # reset emotion intensity to default value
	emotion.set("(Please select emotion)") # reset emotion dropdown to default value
	sound_label.config(text= f'sound {question_idx + update_number} of 30')  #update sound counter label
	return emotion_rating, emotion

	#Function to collect startime datetime
def get_start_time():
	current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
	return current_time

	#Function to playsound
def play():
	global start_time
	global sound_list
	global idx
	start_time = get_start_time() #get starttime upon clicking plays sound
	playsound(sound_list[idx])

	#Function to collect endtime timestamp
def get_end_time():
	current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
	return current_time


# Driver code
if __name__ == "__main__":

	root = Tk() # create a GUI window
	root.configure(background='light green') # set the background colour of GUI window
	root.title("Form for emotion data collection with sounds")# set the title of GUI window
	root.geometry("525x250")# set the configuration of GUI window
	excel()

	#create textbox and label for userid and position
	user_id = Label(root,text="User ID",fg="Black", bg="Light Blue")
	user_id_field = Entry(root)
	user_id.grid(row=0, column=0)
	user_id_field.grid(row=0,column=1)

    #create sound play button and position
	play_button = Button(root, text="Play Sound", fg="Black", bg="Light Blue", command = lambda: play())
	play_button.grid(row=1, column=0)

	#create Soundlabel and position
	sound_label = Label (root, text= f'sound {idx + 1} of 30' , fg="Black", bg="Light Blue")
	sound_label.grid(row=2, column=0)
	
	#create an emotion dropdown button and position
	emotion = StringVar(root)
	emotion.set("Plese select emotion") # default value
	w3 = OptionMenu(root, emotion, "Sadness", "Fear", "Happiness")
	w3.grid(row=1, column=1)

	#create an emotion intensity dropdown button and position
	emotion_rating = StringVar(root)
	emotion_rating.set("How intense?") # default value
	w4 = OptionMenu(root, emotion_rating, "1", "2", "3", "4", "5", "6", "7", "8", "9")
	w4.grid(row=1, column=2)

	# call excel function
	excel()

	# create a Submit Button and place into the root window
	submit = Button(root, text="Submit", fg="Black",
							bg="Red", command=insert)
	submit.grid(row=1, column=3)

	# start the GUI
	root.mainloop()