import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyttsx3
import random
import pandas as pd

def load_data(vocabulary_file, sentences_file):
    try:
        vocab_df = pd.read_excel(vocabulary_file)
        sentences_df = pd.read_excel(sentences_file)
        vocabulary = dict(zip(vocab_df['German'], vocab_df['Turkish']))
        sentences = dict(zip(sentences_df['German'], sentences_df['Turkish']))
        return vocabulary, sentences
    except Exception as e:
        raise FileNotFoundError("Error loading files: " + str(e))

def save_to_excel(vocabulary, sentences, vocabulary_file, sentences_file):
    vocab_df = pd.DataFrame(list(vocabulary.items()), columns=['German', 'Turkish'])
    vocab_df.to_excel(vocabulary_file, index=False)
    sentences_df = pd.DataFrame(list(sentences.items()), columns=['German', 'Turkish'])
    sentences_df.to_excel(sentences_file, index=False)

class LanguageLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Language Learning Program")

        # Remove fullscreen attributes
        self.root.attributes('-fullscreen', False)
        
        # Set window size and position
        self.root.geometry("1920x1080")  # Adjust as needed
        self.root.resizable(True, True)
        
        # Set background color
        self.root.configure(bg="black")

        # File paths
        self.vocabulary_file = 'C:\\Users\\ynsem\\OneDrive\\Masaüstü\\Python Projects\\Language Education\\vocabulary.xlsx'
        self.sentences_file = 'C:\\Users\\ynsem\\OneDrive\\Masaüstü\\Python Projects\\Language Education\\sentence.xlsx'
        self.background_image_file = 'C:\\Users\\ynsem\\OneDrive\\Masaüstü\\Python Projects\\Language Education\\background.jpg'

        # Load and set background image with transparency
        self.bg_image = Image.open(self.background_image_file).convert("RGBA")
        alpha = self.bg_image.split()[3]
        alpha = alpha.point(lambda p: p * 0.3)  # Set opacity to 30%
        self.bg_image.putalpha(alpha)
        self.bg_image = self.bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.place(relwidth=1, relheight=1)

        # Mode selection
        self.mode = tk.StringVar(value="v")
        self.translation_direction = tk.StringVar(value="g2t")

        mode_frame = tk.Frame(root, highlightthickness=0)
        mode_frame.place(relx=0.05, rely=0.05, anchor=tk.NW)

        tk.Label(mode_frame, text="Choose mode:", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Radiobutton(mode_frame, text="Vocabulary", variable=self.mode, value="v", font=("Arial", 14)).pack()
        tk.Radiobutton(mode_frame, text="Sentences", variable=self.mode, value="s", font=("Arial", 14)).pack()

        tk.Label(mode_frame, text="Translation direction:", bg="#f5f5f5", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Radiobutton(mode_frame, text="German to Turkish", variable=self.translation_direction, value="g2t", font=("Arial", 14), bg="#f5f5f5", selectcolor="#dcdcdc").pack()
        tk.Radiobutton(mode_frame, text="Turkish to German", variable=self.translation_direction, value="t2g", font=("Arial", 14), bg="#f5f5f5", selectcolor="#dcdcdc").pack()

        # Display area
        self.display_label = tk.Label(root, text="", font=("Arial", 22, "bold"), bg="#f5f5f5", wraplength=1200, justify="center")
        self.display_label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        # User feedback label
        self.feedback_label = tk.Label(root, text="", font=("Arial", 16), bg="#f5f5f5", fg="#007bff", wraplength=1200, justify="center")
        self.feedback_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Entry for user input
        self.user_input = tk.Entry(root, font=("Arial", 16), width=50, borderwidth=0, relief="flat")
        self.user_input.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.user_input.bind('<FocusIn>', self.clear_default_text)
        self.user_input.bind('<FocusOut>', self.restore_default_text)
        self.user_input.bind("<Return>", self.handle_enter_key)

        # Button Frame
        button_frame = tk.Frame(root, bg="#f5f5f5", highlightthickness=0)
        button_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Button styles
        button_style = {"font": ("Arial", 14, "bold"), "bg": "#007bff", "fg": "white", "relief": "flat", "bd": 0, "width": 15}

        # Submit button
        tk.Button(button_frame, text="Submit", command=self.check_answer, **button_style).pack(side=tk.LEFT, padx=0)

        # Next button
        tk.Button(button_frame, text="Next", command=self.next_question, **button_style).pack(side=tk.LEFT, padx=5)

        # Hint button
        tk.Button(button_frame, text="Hint", command=self.give_hint, **button_style).pack(side=tk.LEFT, padx=5)

        # Add new data section
        add_data_frame = tk.Frame(root, bg="#f5f5f5", highlightthickness=0)
        add_data_frame.place(relx=0.05, rely=0.7, anchor=tk.NW)

        tk.Label(add_data_frame, text="Add New Data:", font=("Arial", 14, "bold"), bg="#f5f5f5").pack(pady=5)

        # Select data type
        self.data_type = tk.StringVar(value="v")

        tk.Radiobutton(add_data_frame, text="Add Vocabulary", variable=self.data_type, value="v", font=("Arial", 12), bg="#f5f5f5", selectcolor="#dcdcdc").pack(pady=2)
        tk.Radiobutton(add_data_frame, text="Add Sentence", variable=self.data_type, value="s", font=("Arial", 12), bg="#f5f5f5", selectcolor="#dcdcdc").pack(pady=2)

        self.german_entry = tk.Entry(add_data_frame, font=("Arial", 12), width=25, borderwidth=0, relief="flat")
        self.german_entry.pack(pady=3)
        self.german_entry.insert(0, "German")

        self.turkish_entry = tk.Entry(add_data_frame, font=("Arial", 12), width=25, borderwidth=0, relief="flat")
        self.turkish_entry.pack(pady=3)
        self.turkish_entry.insert(0, "Turkish")

        tk.Button(add_data_frame, text="Add to List", command=self.add_to_list, font=("Arial", 12, "bold"), bg="#007bff", fg="white", relief="flat", bd=0, width=20).pack(pady=5)

        # Speak button
        tk.Button(button_frame, text="Speak", command=self.speak_text, **button_style).pack(side=tk.LEFT, padx=0)

        # Initialize the vocabulary and sentences
        self.vocabulary = {}
        self.sentences = {}
        self.correct_answers = []

        try:
            self.vocabulary, self.sentences = load_data(self.vocabulary_file, self.sentences_file)
        except FileNotFoundError as e:
            self.display_message("File Not Found", str(e), "error")

        # Initialize the first question
        self.next_question()

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()

    def resize_bg_image(self, event=None):
        if event:
            width, height = event.width, event.height
        else:
            width, height = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        
        self.bg_image = Image.open(self.background_image_file).convert("RGBA")
        self.bg_image = self.bg_image.resize((width, height), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label.config(image=self.bg_photo)
        self.bg_label.image = self.bg_photo

    def clear_default_text(self, event=None):
        if self.user_input.get() == "":
            self.user_input.config(fg="black")

    def restore_default_text(self, event=None):
        if not self.user_input.get():
            self.user_input.config(fg="black")

    def next_question(self):
        self.enter_key_press_count = 0
        self.available_hints = []
        self.hints = []

        if self.mode.get() == "v":
            if not self.vocabulary:
                self.display_message("Data Error", "No vocabulary data available.", "warning")
                return
            if self.translation_direction.get() == "g2t":
                self.current_question, self.current_answer = random.choice(list(self.vocabulary.items()))
                self.display_label.config(text=f"What is the Turkish translation for '{self.current_question}'?")
            else:
                self.current_answer, self.current_question = random.choice(list(self.vocabulary.items()))
                self.display_label.config(text=f"What is the German translation for '{self.current_question}'?")

            self.hints = [
                f"The answer starts with '{self.current_answer[0]}'.",
                f"The answer has {len(self.current_answer)} letters.",
                f"The answer ends with '{self.current_answer[-1]}'."
            ]
        else:
            if not self.sentences:
                self.display_message("Data Error", "No sentences data available.", "warning")
                return
            if self.translation_direction.get() == "g2t":
                self.current_question, self.current_answer = random.choice(list(self.sentences.items()))
                self.display_label.config(text=f"What is the Turkish translation for '{self.current_question}'?")
                self.hints = [
                    f"The answer starts with '{self.current_answer.split()[0]}'.",
                    f"The answer includes the word '{self.current_answer.split()[1]}'.",
                    f"The answer has {len(self.current_answer.split())} words."
                ]
            else:
                self.current_answer, self.current_question = random.choice(list(self.sentences.items()))
                self.display_label.config(text=f"What is the German translation for '{self.current_question}'?")
                self.hints = [
                    f"The answer starts with '{self.current_answer.split()[0]}'.",
                    f"The answer includes the word '{self.current_answer.split()[1]}'.",
                    f"The answer has {len(self.current_answer.split())} words."
                ]

        self.available_hints = self.hints.copy()
        self.feedback_label.config(text="")
        self.user_input.delete(0, tk.END)
        self.user_input.config(fg="black")

    def handle_enter_key(self, event=None):
        self.enter_key_press_count = getattr(self, 'enter_key_press_count', 0) + 1

        if self.enter_key_press_count % 2 == 1:
            self.check_answer()
        else:
            self.next_question()

    def give_hint(self):
        if self.available_hints:
            hint = self.available_hints.pop(0)
            self.feedback_label.config(text=f"Hint: {hint}", fg="blue")
        else:
            self.feedback_label.config(text="No more hints available.", fg="blue")

    def add_to_list(self):
        data_type = self.data_type.get()
        german_word = self.german_entry.get().strip()
        turkish_word = self.turkish_entry.get().strip()

        if data_type == "v":
            if german_word and turkish_word:
                self.vocabulary[german_word] = turkish_word
                save_to_excel(self.vocabulary, self.sentences, self.vocabulary_file, self.sentences_file)
                self.display_message("Success", "Vocabulary added successfully.", "info")
            else:
                self.display_message("Input Error", "Please enter both German and Turkish words.", "warning")
        else:
            if german_word and turkish_word:
                self.sentences[german_word] = turkish_word
                save_to_excel(self.vocabulary, self.sentences, self.vocabulary_file, self.sentences_file)
                self.display_message("Success", "Sentence added successfully.", "info")
            else:
                self.display_message("Input Error", "Please enter both German and Turkish sentences.", "warning")

    def speak_text(self):
        if self.mode.get() == "v":
            text = self.current_question
        else:
            text = self.current_question  
        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.setProperty('rate', 150)

    def check_answer(self):
        user_answer = self.user_input.get().strip()
        correct_answer = self.current_answer.strip()
        if user_answer.lower() == correct_answer.lower():
            self.feedback_label.config(text="Correct! Well done.", fg="green")
        else:
            self.feedback_label.config(text=f"Incorrect. The correct answer is: {correct_answer}", fg="red")

    def display_message(self, title, message, msg_type):
        if msg_type == "info":
            messagebox.showinfo(title, message)
        elif msg_type == "warning":
            messagebox.showwarning(title, message)
        elif msg_type == "error":
            messagebox.showerror(title, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = LanguageLearningApp(root)
    root.bind("<Configure>", app.resize_bg_image)
    root.mainloop()
