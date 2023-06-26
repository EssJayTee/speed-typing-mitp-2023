import customtkinter as ctk
import time
import threading
from random import choice
from PIL import Image

# setting the appearance mode to react with system theme
ctk.set_appearance_mode("System")

# using a built-in customtkinter theme for colors that won't need changes
ctk.set_default_color_theme("dark-blue")

# read saved results
saved_results = []
try:
    with open("results.txt", "r") as file:
        for line in file:
            username, result, date = line.strip().split("\t")
            saved_results.append((username, result, date))
except FileNotFoundError:
    pass


class WelcomeScreen:
    def __init__(self, root):
        self.root = root
        # title
        self.root.title("Speed Typing App")
        # default window size
        self.root.geometry("1280x720")
        # frame
        self.frame = ctk.CTkFrame(self.root)

        # welcome message
        welcome_label = ctk.CTkLabel(self.frame,
                                     text="Welcome to the Speed Typing App!",
                                     font=("Roboto", 46))
        welcome_label.place(relx=0.5, rely=0.1, anchor="center")

        # image
        image = ctk.CTkImage(dark_image=Image.open("keyboard.png"), size=(200, 200))
        image_label = ctk.CTkLabel(self.frame, image=image, text="")
        image_label.place(relx=0.5, rely=0.7, anchor="center")

        # start button
        start_button = ctk.CTkButton(self.frame,
                                     text="Start",
                                     command=self.open_main_screen,
                                     font=("Roboto", 32))
        start_button.place(relx=0.5, rely=0.3, anchor="center")

        # select difficulty
        difficulty_label = ctk.CTkLabel(self.frame,
                                        text='Choose your desired difficulty',
                                        font=("Roboto", 24))
        difficulty_label.place(relx=0.5, rely=0.4, anchor="center")

        self.optionmenu_var = ctk.StringVar(value="Medium")

        difficulty_options = ctk.CTkOptionMenu(
            self.frame,
            values=["Easy", "Medium", "Hard"],
            font=("Roboto", 24),
            command=self.optionmenu_callback,
            variable=self.optionmenu_var
        )
        difficulty_options.place(relx=0.5, rely=0.5, anchor="center")

        self.frame.pack(padx=50, pady=50, fill="both", expand=True)

        # exit button
        exit_button = ctk.CTkButton(self.frame,
                                    text="Exit",
                                    fg_color="red",
                                    command=self.root.destroy,
                                    font=("Roboto", 16))
        exit_button.pack(side="bottom", anchor="e", padx=10, pady=10)

    def open_main_screen(self):
        self.frame.destroy()  # destroy the welcome screen frame

        # create and display the main screen
        SpeedTypingApp(self.root, self.optionmenu_var.get())

    def optionmenu_callback(self, difficulty_choice):
        print("optionmenu dropdown clicked:", difficulty_choice)


class SpeedTypingApp:

    def __init__(self, root, difficulty):
        self.root = root
        # title
        self.root.title("Speed Typing App")
        # default window size
        self.root.geometry("1280x720")
        # font that will be used the most
        self.my_font = ctk.CTkFont(family="Roboto", size=24)
        # difficulty
        self.difficulty = difficulty
        # results
        self.results = []

        # texts used for testing
        self.texts = []
        if difficulty == "Easy":
            with open("easy.txt", "r") as text_file:
                self.texts = text_file.read().split("\n")
        elif difficulty == "Medium":
            with open("medium.txt", "r") as text_file:
                self.texts = text_file.read().split("\n")
        elif difficulty == "Hard":
            with open("hard.txt", "r") as text_file:
                self.texts = text_file.read().split("\n")

        # frame
        self.frame = ctk.CTkFrame(self.root)

        self.welcome_text_label = ctk.CTkLabel(self.frame,
                                               text="Rewrite the following text as fast as you can:",
                                               font=("Roboto", 28))
        self.welcome_text_label.place(relx=0.5, rely=0.1, anchor="center")

        self.sample_label = ctk.CTkLabel(self.frame,
                                         text=choice(self.texts),
                                         font=self.my_font,
                                         )
        self.sample_label.place(relx=0.5, rely=0.2, anchor="center")

        self.user_input = ctk.CTkEntry(self.frame,
                                       width=1000,
                                       font=self.my_font)
        self.user_input.place(relx=0.5, rely=0.35, anchor="center")
        self.user_input.bind("<KeyRelease>", self.start)

        self.speed_label = ctk.CTkLabel(self.frame,
                                        text="Speed: \n0.00 WPS\n0.00 WPM",
                                        font=self.my_font)
        self.speed_label.place(relx=0.5, rely=0.5, anchor="center")

        self.reset_button = ctk.CTkButton(self.frame,
                                          text="Reset",
                                          command=self.reset,
                                          font=self.my_font)
        self.reset_button.place(relx=0.5, rely=0.65, anchor="center")

        results_button = ctk.CTkButton(self.frame,
                                       text="View Results",
                                       command=self.open_results_window,
                                       font=self.my_font)
        results_button.place(relx=0.5, rely=0.75, anchor="center")

        back_button = ctk.CTkButton(self.frame,
                                    text="Back",
                                    command=self.open_welcome_screen,
                                    font=self.my_font)
        back_button.place(relx=0.5, rely=0.9, anchor="center")

        # exit button
        exit_button = ctk.CTkButton(self.frame,
                                    text="Exit",
                                    fg_color="red",
                                    command=self.root.destroy,
                                    font=("Roboto", 16))
        exit_button.pack(side="bottom", anchor="e", padx=10, pady=10)

        self.frame.pack(padx=40, pady=40, fill="both", expand=True)

        # counter
        self.counter = 0
        self.running = False

    # starting the test
    def start(self, event):
        # making sure that function buttons do not start the test
        if not self.running:
            if not event.keycode in [9, 16, 17, 18, 27, 112, 113, 114, 115, 37, 38, 39, 40, 13, 20, 116, 117, 118, 119, 120, 121, 122, 123]:
                self.running = True
                t = threading.Thread(target=self.time_thread)
                t.start()

        if not self.sample_label.cget("text").startswith(self.user_input.get()):
            self.user_input.configure(fg_color="#ba1904")
        else:
            self.user_input.configure(fg_color="black")

        if self.user_input.get() == self.sample_label.cget("text"):
            self.running = False
            self.user_input.configure(fg_color="#05631e")

    # timing
    def time_thread(self):
        while self.running:
            time.sleep(0.1)
            self.counter += 0.1
            wps = len(self.user_input.get().split(" ")) / self.counter
            wpm = wps * 60
            self.speed_label.configure(text=f"Speed: \n{wps:.2f} WPS\n{wpm:.2f} WPM")
            if not self.running:
                current_date = time.strftime("%H:%M %d-%m-%Y")
                self.results.append(("", f"{wpm:.2f} WPM", current_date))

    # resetting the test
    def reset(self):
        self.running = False
        self.counter = 0
        self.speed_label.configure(text="Speed: \n0.00 WPS\n0.00 WPM")
        self.sample_label.configure(text=choice(self.texts))
        self.user_input.delete(0, ctk.END)

    def open_welcome_screen(self):
        self.frame.destroy()  # destroy the main screen frame
        WelcomeScreen(self.root)  # create and display the welcome screen

    def open_results_window(self):
        self.frame.destroy()  # destroy the main screen frame
        ResultsWindow(self.root, saved_results + self.results, self.difficulty)  # create and display the results window


class ResultsWindow:
    def __init__(self, root, results, difficulty):
        self.root = root
        self.results = results
        self.difficulty = difficulty
        # title
        self.root.title("Speed Typing App - Results")
        # default window size
        self.root.geometry("1280x720")
        # font that will be used the most
        self.my_font = ctk.CTkFont(family="Roboto", size=24)

        # frame
        self.frame = ctk.CTkFrame(self.root)

        # table
        table_text = "Username\tResult\t\tDate\n"
        for res in results:
            table_text += f"{res[0]}\t\t{res[1]}\t{res[2]}\n"
        self.table = ctk.CTkLabel(self.frame, text=table_text, font=self.my_font, justify="left")
        self.table.place(relx=0.5, rely=0.3, anchor="center")

        # save button
        save_button = ctk.CTkButton(self.frame, text="Save", command=self.save_results, font=self.my_font)
        save_button.place(relx=0.5, rely=0.75, anchor="center")

        # back button
        back_button = ctk.CTkButton(self.frame, text="Back", command=self.open_main_screen, font=self.my_font)
        back_button.place(relx=0.5, rely=0.9, anchor="center")

        # exit button
        exit_button = ctk.CTkButton(self.frame,
                                    text="Exit",
                                    fg_color="red",
                                    command=self.root.destroy,
                                    font=("Roboto", 16))
        exit_button.pack(side="bottom", anchor="e", padx=10, pady=10)

        self.frame.pack(padx=40, pady=40, fill="both", expand=True)

    def open_main_screen(self):
        self.frame.destroy()  # destroy the results window frame
        SpeedTypingApp(self.root, self.difficulty)  # create and display the main screen

    def save_results(self):
        result_username = ctk.CTkInputDialog(title="Username", text="Enter your username:")
        result_username = result_username.get_input()
        if result_username:
            user_result = self.results[-1][1]
            result_date = time.strftime("%H:%M %d-%m-%Y")
            self.table.configure(text=self.table.cget("text") + f"{result_username}\t\t{user_result}\t\t{result_date}\n")
            with open("results.txt", "a") as results_file:
                results_file.write(f"{result_username}\t{user_result}\t{result_date}\n")


app = ctk.CTk()

WelcomeScreen(app)

app.mainloop()
