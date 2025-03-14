#Modules and libs
from tkinter import * #A basic framework to build simple desktop apps
from ttkbootstrap import Style #To add a beautifull look to the app
from tkinter.scrolledtext import ScrolledText #Lib for inserting a text box with scroll bar on the right
from tkinter.filedialog import askopenfilename, asksaveasfilename #Lib for managing files on the computer
from gtts import gTTS #Lib that allows you to convert texto to speech easly and fastly
import pygame #Lib for playing the sound into the app
import os #Lib that allows you to manage files and directories in the computer
from pathlib import Path
import shutil #Lib that allows you to manage high-level files in the computer
from newspaper import Article #To extract the content from web pages
import re #Regular expressions

#Funciones
def on_close():
    """Check the operating system and return the Desktop path"""
    system_type = os.name
    if system_type == "nt":
        desktop_path = Path(os.environ["USERPROFILE"]) / "Desktop"
    else: 
        desktop_path = Path.home() / "Desktop"

    #If the file exists, delete it and close the app
    if os.path.isfile(desktop_path / "temp_audio.mp3"):
        os.remove(desktop_path / "temp_audio.mp3")
        app.window.destroy()
    #Otherwise, close the app.
    else: 
        app.window.destroy()


#Classes
class App():
    """Main class that create the main window of the app"""
    def __init__(self,window):
        self.style = Style(theme="morph")
        self.window = window
        self.window.geometry("650x650+645+225")
        self.window.title("Text to voice")
        #Check the operating system
        self.check_os()
        #Create all the main widgets
        self.create_widgets()
        
        
        
    def create_widgets(self):
        """Create all the app widgets"""
        #Label
        """Create the title of the app using two labels to do it"""
        self.header_frame = Frame(self.window, pady=20)
        self.header_frame.pack()
        self.header = Label(self.header_frame, text="TEXT TO VOICE", font=("Roboto Condensed", 32, "bold"))
        self.header.pack(side="top")
        self.subheader = Label(self.header_frame, text="Convert text to voice fastly", font=("Roboto Condensed",14, "bold"))
        self.subheader.pack(side="top")
        
        #Top Buttons
        """Create all the buttons over the text box"""
        self.buttons_frame1 = Frame(self.window, padx=10, pady=10)
        self.buttons_frame1.pack(fill="both")
        self.boton_open_file = Button(self.buttons_frame1, text="Open file", command=self.open_file)
        self.boton_open_file.pack(side="left")
        self.boton_convert = Button(self.buttons_frame1, text="Convert", command=self.convert)
        self.boton_convert.pack(side="left")
        self.boton_save = Button(self.buttons_frame1, text="Save", command=self.save)
        self.boton_save.pack(side="left")
        self.boton_delete_text = Button(self.buttons_frame1, text="Delete text", command=self.delete_text)
        self.boton_delete_text.pack(side="left")
        self.boton_stop = Button(self.buttons_frame1, text="Stop", command=self.stop_sound)
        self.boton_stop.pack(side="right")
        self.boton_play = Button(self.buttons_frame1, text="Play", command=self.play_sound)
        self.boton_play.pack(side="right")
        
        #Text-box
        """Create de scrolled text box and the label frame around it"""
        self.text_box_frame = Frame(self.window, padx=10, pady=10)
        self.text_box_frame.pack(fill="both")
        self.label_text_box = LabelFrame(self.text_box_frame, text="Paste or type your text/url here", font=("Ubuntu", 10), padx=10, pady=10)
        self.label_text_box.pack(fill="both")
        self.text_box = ScrolledText(self.label_text_box, wrap="word")
        self.text_box.pack(fill="both")
        
        #Bottom Buttons
        """Create the button 'quit' to close the app"""
        self.boton_quit = Button(self.window, text="Quit!", command=self.quit_app)
        self.boton_quit.pack()


    def check_os(self):
        """Check the operating system into the class and return the Desktop path.
           It allows to close the app from the button 'quit' """
        self.system_type = os.name
        if self.system_type == "nt":
            self.desktop_path = Path(os.environ["USERPROFILE"]) / "Desktop"
        else: 
            self.desktop_path = Path.home() / "Desktop"

        
    def open_file(self):
        """Open text file from the computer with a file dialog"""
        filename = askopenfilename(filetypes=[("Archivo de texto", "*.txt"), ("Archivo PDF", "*.pdf")])
        if filename:
            with open(filename, "r") as f_objt:
                content = f_objt.read()
                #Clean the tex-box
                self.text_box.delete(1.0, "end")
                #Insert the file content into the text-box
                self.text_box.insert(1.0, content)

        
    def convert(self):
        """Convert the text input to voice and save it to play into the app"""
        self.text = self.text_box.get(1.0, "end")

        #Check if the input is an url 
        self.pattern = "https://"
        self.url = self.text
        self.check_url = re.match(self.pattern, self.url)

        #If it's an url call the correct function
        if self.check_url:
            self.convert_from_url()
        #Otherwise, call the other function
        else: 
            self.convert_from_text()

        #Toplevel Popup Window 
        self.convert_finished()


    def convert_from_text(self):
        '''Convert text from typing or file to voice'''
        self.text_to_voice = gTTS(self.text, lang="es")
        self.text_to_voice.save(self.desktop_path / "temp_audio.mp3")


    def convert_from_url(self):
        '''Convert text from an url to voice'''
        article_obj = Article(self.url)
        article_obj.download()
        article_obj.parse()
        self.text_to_voice = gTTS(article_obj.text, lang="es")
        self.text_to_voice.save(self.desktop_path / "temp_audio.mp3")


    def save(self):
        """Save the final audio file. You can choise the path"""
        file_path = asksaveasfilename(defaultextension=".mp3", filetypes=[("Archivo de audio MP3", "*.mp3")])
        if file_path:
            shutil.copy(self.desktop_path / "temp_audio.mp3", file_path)


    def delete_text(self):
        """Clean the text box automatically"""
        self.text_box.delete(1.0, "end")


    def play_sound(self):
        """Play the audio"""
        pygame.init()
        pygame.mixer.init()
        audio = pygame.mixer.Sound(self.desktop_path / "temp_audio.mp3")
        audio.play()


    def stop_sound(self):
        """Stop the audio"""
        pygame.mixer.stop()
        

    def convert_finished(self):
        """Launch a popup that shows when the convertion has finished"""
        self.popup_finished = Toplevel(self.window)
        self.popup_finished.geometry("250x100+900+490")
        self.popup_finished.title("")
        self.finished_label = Label(self.popup_finished, text="Convertion has finished!", font=("Ubuntu", 12, "bold"))
        self.finished_label.pack()
        self.popup_finished.after(1000, self.quit_popup)


    def quit_popup(self):
        """Quit the popup window automatically"""
        self.popup_finished.destroy()


    def quit_app(self):
        """Delete de temp file and close the app"""
        #If the file exists, delete it and close the app
        if os.path.isfile(self.desktop_path / "temp_audio.mp3"):
            os.remove(self.desktop_path / "temp_audio.mp3")
            self.window.destroy()
        #Otherwise close the app
        else: 
            self.window.destroy()
    

app = App(Tk())
#Before closing the app from the 'x' button, call the on_close function.
app.window.protocol("WM_DELETE_WINDOW", on_close)
app.window.mainloop()


        