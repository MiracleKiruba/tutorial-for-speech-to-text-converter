import os
import speech_recognition as sr
import moviepy.editor as mp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import tkinter as tk
from tkinter import filedialog


def browse_file():
    file_path = filedialog.askopenfilename()
    input_path.set(file_path)


def process_video():
    input_file = input_path.get()
    if not input_file or not os.path.exists(input_file):
        status_label.config(text="Please select a valid input file.")
        return
    num_seconds_video = 52 * 60
    print("The video is {} seconds".format(num_seconds_video))
    l = list(range(0, num_seconds_video + 1, 60))

    diz = {}

    for i in range(len(l) - 1):
        try:
            ffmpeg_extract_subclip(input_file, l[i] - 2 * (l[i] != 0), l[i + 1],
                                   targetname="chunks/cut{}.mp4".format(i + 1))

            clip = mp.VideoFileClip(r"chunks/cut{}.mp4".format(i + 1))
            clip.audio.write_audiofile(r"converted/converted{}.wav".format(i + 1))
            r = sr.Recognizer()
            audio = sr.AudioFile("converted/converted{}.wav".format(i + 1))
            with audio as source:
                r.adjust_for_ambient_noise(source)
                audio_file = r.record(source)
            result = r.recognize_google(audio_file)
            diz['chunk{}'.format(i + 1)] = result
        except:
            pass
    l_chunks = [diz['chunk{}'.format(i + 1)] for i in range(len(diz))]
    text = '\n'.join(l_chunks)

    with open('recognized.txt', mode='w') as file:
        file.write("EXTRACTED TEXT FROM THE SPEECH IS:")
        file.write("\n")
        file.write(text)
        status_label.config(text="Processing complete.")

    # read the contents of the recognized.txt file and display them in the text box
    with open('recognized.txt', mode='r') as file:
        recognized_text = file.read()
        output_text.delete('1.0', tk.END)  # clear any previous text
        output_text.insert(tk.END, recognized_text)


# create the GUI
root = tk.Tk()
root.title("Video to Text Converter")

input_path = tk.StringVar()
input_path.set("")

input_label = tk.Label(root, text="Input file:")
input_label.pack()

input_entry = tk.Entry(root, textvariable=input_path)
input_entry.pack()

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

process_button = tk.Button(root, text="Process Video", command=process_video)
process_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

output_label = tk.Label(root, text="Recognized text:")
output_label.pack()

output_text = tk.Text(root)
output_text.pack()


root.mainloop()
