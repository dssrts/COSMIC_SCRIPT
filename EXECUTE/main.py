import tkinter as tk
#import pygame as pg
from tkVideoPlayer import TkinterVideo
from PIL import Image, ImageTk  # Import Pillow
from pathlib import Path
import parser1
import lexer
import sys

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Repositories\make_a_compiler\EXECUTE\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def input_entry(widget):
    input_text.configure(bg="#817ACD")
    input_text.configure(bd=2)

def input_out(widget):
    input_text.configure(bg="#817ACD")
    input_text.configure(bd=0)

# def remove_player(videoplayer,window):
#     videoplayer.destroy()
#     window.destroy()
#     root.deiconify()

# def loading_screen():
#     root.withdraw()
#     loading_window = tk.Toplevel()
#     loading_window.attributes('-fullscreen',True)
#     loading_window.resizable(False,False)

#     videoplayer = TkinterVideo(master=loading_window, scaled=True)
#     videoplayer.load(r"C:\\Compiler Design\\Intro\\cosmicloading.mp4")
#     pg.mixer.music.load("C:\\Compiler Design\\Intro\\cosmicaudio.MP3")
#     videoplayer.pack(expand=True, fill="both")
#     videoplayer.play()
#     pg.mixer.music.play(loops=0)
#     videoplayer.bind("<<Ended>>",lambda remove: remove_player(videoplayer,loading_window))

# Function to run the lexer and update the GUI
def run_lexer():
    input_text_str = input_text.get("1.0", "end-1c")
    result, error = lexer.run("<stdin>",input_text_str)
    output_text.delete(0, tk.END)
    token_text.delete(0, tk.END)
    errors_text.delete(0, tk.END)
    print(result)
    print (error)
    if error:
        for err in error:
            errors_text.insert(tk.END, err)
    for item in result:
        if item:
            output_text.insert(tk.END, item.value)
            token_text.insert(tk.END, item.token)
    

    # if error:
    #     errors_text.insert(tk.END, error.as_string())
    # else:
    #     errors_text.insert(tk.END, "Success!", result)
    #     #token_text.insert(tk.END, item.token)

def run_syntax():
    input_text_str = input_text.get("1.0", "end-1c")
    result, error = parser1.run("<stdin>",input_text_str)
    output_text.delete(0, tk.END)
    token_text.delete(0, tk.END)
    errors_text.delete(0, tk.END)
    print(result)
    if error:
        errorResult, fileDetail, arrowDetail, arrows = error.as_string()
        errors_text.insert(tk.END, errorResult)
        errors_text.insert(tk.END, fileDetail)
        errors_text.insert(tk.END, arrowDetail)
        errors_text.insert(tk.END, arrows)
    else:
        errors_text.insert(tk.END, "Success!", result)
        #token_text.insert(tk.END, item.token)

#create main canvas
root = tk.Tk()
root.geometry("1280x720")
root.resizable(False, False)  # Disable window resizing
ico = Image.open('D:\\Repositories\\make_a_compiler\\EXECUTE\\logo-automata.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)
root.title("Cosmic Script")
root.configure(bg="#252655")
# pg.mixer.init()
# loading_screen()

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate position x and y for the Tkinter window
x = (screen_width / 2) - (1280 / 2)
y = (screen_height / 2) - (720 / 2) - 40

# Set the position of the window to the center
root.geometry(f"1280x720+{int(x)}+{int(y)}")

# Configure the main window to expand with the window size
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)  # Add a row configuration for the error window

#create a Canvas widget
canvas = tk.Canvas(root, width=1280, height=720)
canvas.pack()

#galaxy bg
image_image_1 = Image.open(relative_to_assets("image_1.png"))
image_1 = ImageTk.PhotoImage(image_image_1)
canvas.create_image(640, 360, image=image_1)

#logo at the upper left corner
image_image_6 = Image.open(relative_to_assets("image_6.png"))
image_6 = ImageTk.PhotoImage(image_image_6)
canvas.create_image(213.0, 47.0, image=image_6)

#create upper left entry/input frame
input_frame1 = tk.Frame(root, width=1000, height=580, bg="white")  # Set width and height
input_frame1.place(x=45.0, y=97.9747314453125, width=553.0, height=313.1805114746094)  # Set position and dimensions
input_label = tk.Label(input_frame1, text="COSMIC SCRIPT > ", font=("Nexa Heavy", 15, "bold"), fg="#817ACD", bg="white")
input_label.pack(side=tk.TOP, pady=5)
input_text = tk.Text(input_frame1, height=20, width=100, font=("Nexa Heavy", 10), fg="white")
input_text.pack(fill="both", expand=True)
input_text.configure(bg="#817ACD", relief="flat")
input_text.bind("<FocusIn>",input_entry)
input_text.bind("<FocusOut>",input_out)
input_text.pack(side=tk.TOP, padx=10, pady=(0,10))
input_frame1.configure(bg="white")

#create middle frame
input_frame2 = tk.Frame(root, width=244.0, height=263.1805114746094, bg="white")  # Set width and height
input_frame2.place(x=624.0, y=97.9747314453125, width=290.0, height=313.1805114746094)  # Set position and dimensions
input_label = tk.Label(input_frame2, text="LEXEME", font=("Nexa Heavy", 15, "bold"), fg="#817ACD", bg="white")
input_label.pack(side=tk.TOP, pady=5)
output_text = tk.Listbox(input_frame2, selectmode=tk.SINGLE, height=34, width=40, font=("Nexa Heavy", 10), fg="white")
output_text.configure(bg="#817ACD", relief="flat")
output_text.pack(fill="both", expand=True, side=tk.TOP, padx=10, pady=(0,10))
input_frame2.configure(bg="white")

#create upper right frame
input_frame3 = tk.Frame(root, width=1089.0, height=249.5649871826172, bg="white")  # Set width and height
input_frame3.place(x=943.0, y=97.9747314453125, width=294.0, height=313.1805114746094)  # Set position and dimensions
input_label = tk.Label(input_frame3, text="TOKEN", font=("Nexa Heavy", 15, "bold"), fg="#817ACD", bg="white")
input_label.pack(side=tk.TOP, pady=5)
token_text = tk.Listbox(input_frame3, selectmode=tk.SINGLE, height=34, width=40, font=("Nexa Heavy", 10), fg="white")
token_text.configure(bg="#817ACD", relief="flat")
token_text.pack(fill="both", expand=True, side=tk.TOP, padx=10, pady=(0,10))
input_frame3.configure(bg="white")

#create lower frame for error
input_frame4 = tk.Frame(root, width=643.0, height=580.5000076293945, bg="white")  # Set width and height
input_frame4.place(x=51.0, y=498.3636474609375, width=1184.0, height=202.27272033691406)  # Set position and dimensions
errors_text = tk.Listbox(input_frame4, selectmode=tk.SINGLE, font=("Nexa Heavy", 10), fg="white")
errors_text.pack(fill="both", expand=True)
errors_text.configure(bg="#817ACD", relief="flat")
errors_text.pack(side=tk.TOP, padx=10, pady=10)
input_frame4.configure(bg="white")

# "Lexer" button on the lower left corner of the input frame
run_button = tk.Button(root, text="Lexer", font=("Nexa Heavy", 15), fg="#817ACD", bg="white", command=run_lexer)
run_button.place(x=50.0, y=437.0, width=126.0, height=40.0)
run_button.configure(relief="flat")

# "Semantic" button to the right of the "Lexer" button
semantic_button = tk.Button(root, text="Semantic", font=("Nexa Heavy", 15), fg="#817ACD", bg="white")
semantic_button.place(x=192.0, y=437.0, width=127.0, height=40.0)
semantic_button.configure(relief="flat")

# "Syntax" button to the right of the "Semantic" button
syntax_button = tk.Button(root, text="Syntax", font=("Nexa Heavy", 15), fg="#817ACD", bg="white", command=run_syntax)
syntax_button.place(x=348.0, y=437.0, width=123.0, height=39.0)
syntax_button.configure(relief="flat")

# Redirect error output to the errors window
class ErrorOutput(object):
    def write(self, message):
        errors_text.insert(tk.END, message)
        errors_text.see(tk.END)  # Automatically scroll to the latest message

sys.stderr = ErrorOutput()

root.mainloop()
