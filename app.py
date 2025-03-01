#Modules and libs
from tkinter import * #A basic framework to build simple desktop apps
from tkinter.scrolledtext import ScrolledText #Lib for inserting a text box with scroll bar on the right
from tkinter.filedialog import askopenfilename, asksaveasfilename #Lib for managing files on the computer
from gtts import gTTS #Lib that allows you to convert texto to speech easly and fastly
import pygame #Lib for playing the sound into the app
import os #Lib that allows you to manage files and directories in the computer
import shutil #Lib that allows you to manage high-level files in the computer
from newspaper import Article #Extraer el contenido de las páginas webs
import re #Expresiones regulares




#Classes
class App():
    """Main class that create the main window of the app"""
    def __init__(self,window):
        self.window = window
        self.window.geometry("650x580") #Final: "650x580+645+225"
        self.window.title("Objects Oriented Programming")
        self.create_widgets()
        
        
    def create_widgets(self):
        """Create all the app widgets"""
        #Label
        """Create the title of the app using two labels to do it"""
        self.header_frame = Frame(self.window, pady=20)
        self.header_frame.pack()
        self.header = Label(self.header_frame, text="Text to voice", font=("Ubuntu", 24, "bold"))
        self.header.pack(side="top")
        self.subheader = Label(self.header_frame, text="Convert text to voice fastly", font=("Ubuntu",14, "bold"))
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

        
    def open_file(self):
        """Open text file from the computer with a file dialog"""
        filename = askopenfilename(filetypes=[("Archivo de texto", "*.txt"), ("Archivo PDF", "*.pdf")])
        if filename:
            with open(filename, "r") as f_objt:
                content = f_objt.read()
                self.text_box.delete(1.0, "end")
                self.text_box.insert(1.0, content)

        
    def convert(self):
        """Convert the text input to voice and save it to play into the app"""
        self.text = self.text_box.get(1.0, "end")

        #Check if the input is an url 
        self.pattern = "https://"
        self.url = self.text
        self.check_url = re.match(self.pattern, self.url)

        #Si es una url llama al método que convierte desde url
        if self.check_url:
            self.convert_from_url()
        #Sino llama al método que convierte desde texto introducido
        else: 
            self.convert_from_text()
        #Toplevel Popup Window 
        self.convert_finished()


    def convert_from_text(self):
        self.text_to_voice = gTTS(self.text, lang="es")
        self.text_to_voice.save("./temp/audio.mp3")


    def convert_from_url(self):
        article_obj = Article(self.url)
        article_obj.download()
        article_obj.parse()
        self.text_to_voice = gTTS(article_obj.text, lang="es")
        self.text_to_voice.save("./temp/audio.mp3")


    def save(self):
        """Save the final audio file. You can choise the path"""
        file_path = asksaveasfilename(defaultextension=".mp3", filetypes=[("Archivo de audio MP3", "*.mp3")])
        if file_path:
            shutil.copy("./temp/audio.mp3", file_path)


    def delete_text(self):
        """Clean the text box automatically"""
        self.text_box.delete(1.0, "end")


    def play_sound(self):
        """Play the audio"""
        pygame.init()
        pygame.mixer.init()
        audio = pygame.mixer.Sound("./temp/audio.mp3")
        audio.play()


    def stop_sound(self):
        """Pause the audio"""
        pygame.mixer.stop()
        

    def convert_finished(self):
        """Launch a popup that says you when the convertion has finished"""
        self.popup_finished = Toplevel(self.window)
        self.popup_finished.geometry("300x50") #Final: "200x100+900+490"
        self.popup_finished.title("")
        self.finished_label = Label(self.popup_finished, text="Convertion has finished!", font=("Ubuntu", 12, "bold"))
        self.finished_label.pack()
        self.popup_finished.after(1000, self.quit_popup)


    def quit_popup(self):
        """Quit the popup window automatically"""
        self.popup_finished.destroy()


    def quit_app(self):
        """Delete de temp file and close the app"""
        os.remove("./temp/audio.mp3")
        self.window.destroy()
    




#TARES:
#1.- Centrar ventana principal al iniciar
#2.- Centrar ventana pop up
#3.- Dar estilo a la ventana pop up
#4.- Dar estilo a la app (investigar ttkbootstrap)
#5.- Ver clase de CB donde habla de estilos en el código (buenas prácticas)
#6.- Subir a github
#7.- (Opcional) Mirar los acentos en la doc de gtts y el ritmo. 
#8.- (Opcional) Mirar qué haría nltk en este caso
#9.- 'Compilar y probar en windows' Problema con los paths?




app = App(Tk())
app.window.mainloop()

        