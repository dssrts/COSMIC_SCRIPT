import tkinter as tk
from tkinter import ttk
#import pygame as pg
from tkVideoPlayer import TkinterVideo
from PIL import Image, ImageTk  # Import Pillow
from pathlib import Path
import parser1
import lexer
import sys


OUTPUT_PATH = Path(__file__).parent
#ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\seped\Documents\GitHub\COSMIC_SCRIPT\EXECUTE\assets\frame0")
#ASSETS_PATH = OUTPUT_PATH / Path(r"C:\\Users\\RaffyAldiny\\Documents\\GitHub\\COSMIC_SCRIPT\\EXECUTE\\assets\\frame0")
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\\Users\\Melissa\\Documents\\GitHub\\COSMIC_SCRIPT\\EXECUTE\\assets\\frame0")
# ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Repositories\make_a_compiler\EXECUTE\assets\frame0")
#ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\DELL\Documents\GitHub\COSMIC_SCRIPT\EXECUTE\assets\frame0")
#ASSETS_PATH = OUTPUT_PATH / Path(r"D:\\Cosmic Script\\COSMIC_SCRIPT\\EXECUTE\\assets\\frame0")
# List to store the history of input text changes
input_history = []
keysym_buffer = ""
newline_count = 1
reserve_word = ['takeoff','landing','galaxy()','var','inner','outer','if','else','elseif','do','whirl',
                'true','false','saturn','form','force','universe','blast','skip', 'void']

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def get_scrollbar_one_position(event):
    delta = int(-1*(event.delta/10))
    input_text.yview_scroll(delta,"units")
    input_text1_counter.yview_scroll(delta,"units")

def input_entry(event):
    input_text.configure(bg="#817ACD")
    input_text.configure(bd=8)
    update_line_numbers(event)

def input_out(event):
    input_text.configure(bg="#817ACD")
    input_text.configure(bd=8)

def multiple_yview(*args):
    input_text.yview(*args)
    input_text1_counter.yview(*args)

# def highlight_reserve_word(keysym):
#     input_text.tag_remove('found', '1.0', tk.END)
#     for word in reserve_word:
#         idx = '1.0'
#         while idx:
#             idx = input_text.search(r'\m{}\M'.format(word), idx, regexp=True, nocase=1, stopindex=tk.END)
#             if idx:
#                 lastidx = '{}+{}c'.format(idx, len(word))
#                 if input_text.get(idx, lastidx).islower():
#                     input_text.tag_add('found', idx, lastidx)
#                 else:
#                     input_text.tag_add('reserveidenti', idx, lastidx)
#                 idx = lastidx

#     input_text.tag_config('found', foreground='yellow')
#     input_text.tag_config('reserveidenti', foreground='white')
    # ...

# ...

# ...

# ...

# ...

# def highlight_reserve_word(keysym):
#     input_text.tag_remove('found', '1.0', tk.END)
#     input_text.tag_remove('comment', '1.0', tk.END)

#     for word in reserve_word:
#         idx = '1.0'
#         while idx:
#             idx = input_text.search(r'\m{}\M'.format(word), idx, regexp=True, nocase=1, stopindex=tk.END)
#             if idx:
#                 lastidx = '{}+{}c'.format(idx, len(word))
#                 if input_text.get(idx, lastidx).islower():
#                     input_text.tag_add('found', idx, lastidx)
#                 else:
#                     input_text.tag_add('reserveidenti', idx, lastidx)
#                 idx = lastidx

#     lines = input_text.get("1.0", tk.END).split('\n')
#     in_multiline_comment = False
#     comment_start = None

#     for i, line in enumerate(lines):
#         # Single-line comments starting with '/*'
#         if '/*' in line:
#             comment_start = i + 1  # Line numbers start from 1
#             input_text.tag_add('comment', f'{comment_start}.0', f'{comment_start}.end')

#         # Multiline comments starting with '//*'
#         if '//*' in line:
#             in_multiline_comment = True
#             comment_start = i + 1  # Line numbers start from 1
#             input_text.tag_add('comment', f'{comment_start}.0', f'{comment_start + 1}.0')

#         if in_multiline_comment:
#             input_text.tag_add('comment', f'{i + 1}.0', f'{i + 1}.end')

#         # Multiline comments ending with '*//'
#         if '*//' in line:
#             in_multiline_comment = False
#             comment_end = i + 1  # Line numbers start from 1
#             input_text.tag_add('comment', f'{comment_end}.0', f'{comment_end + 1}.0')

#     input_text.tag_config('found', foreground='yellow')
#     input_text.tag_config('reserveidenti', foreground='white')
#     input_text.tag_config('comment', foreground='pink')

# ...
def highlight_reserve_word(keysym):
    input_text.tag_remove('found', '1.0', tk.END)
    input_text.tag_remove('comment', '1.0', tk.END)

    for word in reserve_word:
        idx = '1.0'
        while idx:
            idx = input_text.search(r'\m{}\M'.format(word), idx, regexp=True, nocase=1, stopindex=tk.END)
            if idx:
                lastidx = '{}+{}c'.format(idx, len(word))
                if input_text.get(idx, lastidx).islower():
                    input_text.tag_add('found', idx, lastidx)
                else:
                    input_text.tag_add('reserveidenti', idx, lastidx)
                idx = lastidx

    lines = input_text.get("1.0", tk.END).split('\n')
    in_multiline_comment = False

    for i, line in enumerate(lines):
        # Single-line comments starting with '/*'
        comment_start = line.find('/*')
        if comment_start != -1:
            input_text.tag_add('comment', f'{i + 1}.{comment_start + 2}', f'{i + 1}.end')

        # Multiline comments starting with '//*'
        if '//*' in line:
            in_multiline_comment = True
            comment_start = i + 1  # Line numbers start from 1
            input_text.tag_add('comment', f'{comment_start}.3', f'{comment_start + 1}.0')  # Start highlighting from position 3

        if in_multiline_comment:
            input_text.tag_add('comment', f'{i + 1}.0', f'{i + 1}.end')

        # Multiline comments ending with '*//'
        if '*//' in line:
            in_multiline_comment = False
            comment_end = i + 1  # Line numbers start from 1
            input_text.tag_add('comment', f'{comment_end}.0', f'{comment_end + 1}.0')

    input_text.tag_config('found', foreground='yellow')
    input_text.tag_config('reserveidenti', foreground='white')
    input_text.tag_config('comment', foreground='pink')
# ...





def update_line_numbers(event):
    highlight_reserve_word(event.keysym)
    input_text1_counter.config(state="normal")
    input_text1_counter.delete("1.0", "end")
    lines = input_text.get("1.0", "end").count("\n")
    input_text1_counter.insert("1.0", "\n".join(str(i) for i in range(1, lines + 1)),"right")
    input_text1_counter.yview("end")
    input_text1_counter.config(state="disabled")

# Function to undo changes in the input_text widget
def clear():
    input_text.delete("1.0", tk.END)
    output_text.delete(0, tk.END)
    token_text.delete(0, tk.END)
    errors_text.delete(0, tk.END)

def remove_player(videoplayer,window):
    videoplayer.destroy()
    window.destroy()
    root.deiconify()

# def loading_screen():
#     root.withdraw()
#     loading_window = tk.Toplevel()
#     loading_window.attributes('-fullscreen',True)
#     loading_window.resizable(False,False)

#     videoplayer = TkinterVideo(master=loading_window, scaled=True)
#     videoplayer.load(r"D:\\Cosmic Script\\COSMIC_SCRIPT\\EXECUTE\\Intro\\cosmicloading.mp4")
#     pg.mixer.music.load("D:\\Cosmic Script\\COSMIC_SCRIPT\\EXECUTE\\Intro\\cosmicaudio.MP3")
#     videoplayer.pack(expand=True, fill="both")
#     videoplayer.play()
#     pg.mixer.music.play(loops=0)
#     videoplayer.bind("<<Ended>>",lambda remove: remove_player(videoplayer,loading_window))

# Function to run the lexer and update the GUI
# def run_lexer():
#     input_text_str = input_text.get("1.0", "end-1c")
#     result, error = lexer.run("<stdin>",input_text_str)
#     output_text.delete(0, tk.END)
#     token_text.delete(0, tk.END)
#     errors_text.delete(0, tk.END)
#     count = 0
#     print(result)
#     print (error)
#     if error:
#         for err in error:
#             errors_text.insert(tk.END, err)
#     for item in result:
#         count += 1
#         if item:
#             output_text.insert(tk.END, "%s.\t   %s" % (count,item.value))
#             token_text.insert(tk.END,  "%s.\t   %s" % (count,item.token))

#     # if error:
#     #     errors_text.insert(tk.END, error.as_string())
#     # else:
#     #     errors_text.insert(tk.END, "Success!", result)
#     #     #token_text.insert(tk.END, item.token)

def run_lexer():
    input_text_str = input_text.get("1.0", "end-1c")
    result, error = lexer.run("<stdin>", input_text_str)
    
    # Clear the text widgets before inserting new results
    output_text.delete(0, tk.END)
    token_text.delete(0, tk.END)
    
    
    count = 0
    print(result)
    print(error)
    errors_text.delete(0, tk.END)
    if error:
        
        for err in error:
            errors_text.insert(tk.END, err)
    for item in result:
        count += 1
        if item:
            
            output_text.insert(tk.END, "%s.\t   %s" % (count, item.value))
            token_text.insert(tk.END,  "%s.\t   %s" % (count, item.token))
def run_syntax():
    input_text_str = input_text.get("1.0", "end-1c")

    # Run lexer
    lexer_result, lexer_error = lexer.run("<stdin>", input_text_str)

    # Display lexer output
    output_text.delete(0, tk.END)
    token_text.delete(0, tk.END)
    count = 0
    for item in lexer_result:
        count += 1
        if item:
            output_text.insert(tk.END, "%s.\t   %s" % (count,item.value))
            token_text.insert(tk.END,  "%s.\t   %s" % (count,item.token))

    # Display lexer errors
    errors_text.delete(0, tk.END)
    if lexer_error:
        for err in lexer_error:
            errors_text.insert(tk.END, err)
    else:
        # If lexer is successful, run syntax parser
        syntax_result, syntax_error = parser1.run("<cosmic script>", input_text_str)
        if syntax_error:
            for err in syntax_error:
                errorResult, fileDetail, arrowDetail, arrows = err.as_string()
                errors_text.insert(tk.END, errorResult)
                errors_text.insert(tk.END, fileDetail)
                errors_text.insert(tk.END, arrowDetail)
                errors_text.insert(tk.END, arrows)
        else:
            for res in syntax_result:
                errors_text.insert(tk.END, res)
            #token_text.insert(tk.END, item.token)

#create main canvas
root = tk.Tk()
root.geometry("1280x720")
root.resizable(False, False)  # Disable window resizing
#ico = Image.open('C:\\Users\\seped\\Documents\\GitHub\\COSMIC_SCRIPT\\EXECUTE\\assets\\frame0\\logo-automata.png')
#ico = Image.open('C:\\Users\\RaffyAldiny\\Documents\\GitHub\\COSMIC_SCRIPT\\EXECUTE\\assets\\frame0\\logo-automata.png')
ico = Image.open('C:\\Users\\Melissa\\Documents\\GitHub\\COSMIC_SCRIPT\\EXECUTE\\assets\\frame0\\logo-automata.png')
# ico = Image.open('D:\\Repositories\\make_a_compiler\\EXECUTE\\logo-automata.png')
#ico = Image.open('C:\\Users\\DELL\\Documents\\GitHub\\COSMIC_SCRIPT\\EXECUTE\\assets\\frame0\s\logo-automata.png')
#ico = Image.open('D:\\Cosmic Script\\COSMIC_SCRIPT\\EXECUTE\\assets\\frame0\\logo-automata.png')
photo = ImageTk.PhotoImage(ico)
root.wm_iconphoto(False, photo)
root.title("Cosmic Script")
root.configure(bg="#252655")
#pg.mixer.init()
#loading_screen()

#Create the style ttk
style = ttk.Style()
style.theme_use('default')
style.configure("Vertical.TScrollbar", background="#474287",relief='flat',borderwidth=0,arrowcolor="#FFFFFF",troughcolor="#8b87c2")
style.map("Vertical.TScrollbar",background=[('active', '#6762a6')])
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

#Create upper left entry/input frame
input_frame1 = tk.Frame(root, width=1000, height=580, bg="white")
input_frame1.place(x=45.0, y=97.9747314453125, width=607, height=328.1805114746094)
input_frame1.configure(bg="white")
input_label = tk.Label(input_frame1, text="COSMIC SCRIPT > ", font=("Nexa Heavy", 15, "bold"), fg="#817ACD", bg="white")
input_label.pack(side=tk.TOP, pady=5)

#Create text widget for line number
input_text1_counter = tk.Text(input_frame1, height=20, width=3, font=("Nexa Heavy", 10,'bold'), fg="#E2ECEE",bd=8)
input_text1_counter.pack(fill=tk.Y)
input_text1_counter.configure(bg="#817ACD", relief="flat",state="normal")
input_text1_counter.tag_configure("right",justify="right")
input_text1_counter.pack(side=tk.LEFT, padx=(10,0), pady=(0,10))
input_text1_counter.bind("<MouseWheel>",get_scrollbar_one_position)

#Create text widget for user input
input_text = tk.Text(input_frame1, height=20, width=100, font=("Nexa Heavy", 10), fg="white",bd=8)
input_text.pack(fill="both", expand=True,side=tk.TOP, padx=10, pady=(0,10))
input_text.configure(bg="#817ACD", relief="flat")
input_text.tag_config('reserve', foreground="yellow")
input_text.tag_config('plain', foreground="white")
#User input text widget events
input_text.bind("<FocusIn>",input_entry)
input_text.bind("<FocusOut>",input_out)
input_text.bind("<KeyRelease>",update_line_numbers)
input_text.bind("<MouseWheel>",get_scrollbar_one_position)

input_scrollbar_one = ttk.Scrollbar(input_text,orient='vertical')
input_scrollbar_one.pack(side=tk.RIGHT,fill='y')
input_scrollbar_one.config(command=multiple_yview)
input_text.configure(yscrollcommand=input_scrollbar_one.set)

#Create middle frame
input_frame2 = tk.Frame(root, width=244.0, height=263.1805114746094, bg="white")  # Set width and height
input_frame2.place(x=664.0, y=97.9747314453125, width=290.0, height=600)  # Set position and dimensions
input_label = tk.Label(input_frame2, text="LEXEME", font=("Nexa Heavy", 15, "bold"), fg="#817ACD", bg="white")
input_label.pack(side=tk.TOP, pady=5)
output_text = tk.Listbox(input_frame2, selectmode=tk.SINGLE, height=34, width=40, font=("Nexa Heavy", 10), fg="white",bd=8)
output_text.configure(bg="#817ACD", relief="flat")
output_text.pack(fill="both", expand=True, side=tk.TOP, padx=10, pady=(0,10))
input_frame2.configure(bg="white")

input_scrollbar_two = ttk.Scrollbar(output_text,orient='vertical')
input_scrollbar_two.pack(side=tk.RIGHT,fill='y')
input_scrollbar_two.config(command=output_text.yview)
output_text.configure(yscrollcommand=input_scrollbar_two.set)

#create upper right frame
input_frame3 = tk.Frame(root, width=1089.0, height=249.5649871826172, bg="white")  # Set width and height
input_frame3.place(x=943.0, y=97.9747314453125, width=294.0, height=600)  # Set position and dimensions
input_label = tk.Label(input_frame3, text="TOKEN", font=("Nexa Heavy", 15, "bold"), fg="#817ACD", bg="white")
input_label.pack(side=tk.TOP, pady=5)
token_text = tk.Listbox(input_frame3, selectmode=tk.SINGLE, height=34, width=40, font=("Nexa Heavy", 10), fg="white",bd=8)
token_text.configure(bg="#817ACD", relief="flat")
token_text.pack(fill="both", expand=True, side=tk.TOP, padx=10, pady=(0,10))
input_frame3.configure(bg="white")

input_scrollbar_three = ttk.Scrollbar(token_text,orient='vertical')
input_scrollbar_three.pack(side=tk.RIGHT,fill='y')
input_scrollbar_three.config(command=token_text.yview)
token_text.configure(yscrollcommand=input_scrollbar_three.set)

#create lower frame for error
input_frame4 = tk.Frame(root, width=643.0, height=580.5000076293945, bg="white")  # Set width and height
input_frame4.place(x=45.0, y=488.3636474609375, width=607, height=210.27272033691406)  # Set position and dimensions
errors_text = tk.Listbox(input_frame4, selectmode=tk.SINGLE, font=("Nexa Heavy", 10), fg="white",bd=8)
errors_text.pack(fill="both", expand=True)
errors_text.configure(bg="#817ACD", relief="flat")
errors_text.pack(side=tk.TOP, padx=10, pady=10)
input_frame4.configure(bg="white")

input_scrollbar_four = ttk.Scrollbar(errors_text,orient='vertical')
input_scrollbar_four.pack(side=tk.RIGHT,fill='y')
input_scrollbar_four.config(command=errors_text.yview)
errors_text.configure(yscrollcommand=input_scrollbar_four.set)


# "Lexer" button on the lower left corner of the input frame
run_button = tk.Button(root, text="Lexer", font=("Nexa Heavy", 15), fg="#817ACD", bg="white", command=run_lexer)
run_button.place(x=50.0, y=437.0, width=127.0, height=40.0)
run_button.configure(relief="flat")

# "Semantic" button to the right of the "Lexer" button
semantic_button = tk.Button(root, text="Semantic", font=("Nexa Heavy", 15), fg="#817ACD", bg="white")
semantic_button.place(x=332.0, y=437.0, width=127.0, height=40.0)
semantic_button.configure(relief="flat")

# "Syntax" button to the right of the "Semantic" button
syntax_button = tk.Button(root, text="Syntax", font=("Nexa Heavy", 15), fg="#817ACD", bg="white", command=run_syntax)
syntax_button.place(x=192.0, y=437.0, width=127.0, height=40.0)
syntax_button.configure(relief="flat")

# Undo button to undo changes
clear_button = tk.Button(root, text="Clear", font=("Nexa Heavy", 15), fg="#817ACD", bg="white", command=clear)
clear_button.place(x=475.0, y=437.0, width=127.0, height=40.0)
clear_button.configure(relief="flat")

# Redirect error output to the errors window
class ErrorOutput(object):
    def write(self, message):
        errors_text.insert(tk.END, message)
        errors_text.see(tk.END)  # Automatically scroll to the latest message

sys.stderr = ErrorOutput()

root.mainloop()