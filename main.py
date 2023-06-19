import customtkinter as ctk
import time
import threading
from random import choice

# setting the appearance mode to react with system theme
ctk.set_appearance_mode("System")

# using a built-in customtkinter theme for colors that won't need changes
ctk.set_default_color_theme("dark-blue")


class SpeedTypingApp:

    def __init__(self):
        self.root = ctk.CTk()
        # title
        self.root.title("Speed Typing App")
        # default window size
        self.root.geometry("1280x720")
        # font that will be used the most
        self.my_font = ctk.CTkFont(family="Roboto", size=24)

        # texts used for testing
        self.texts = open("texts.txt", "r").read().split("\n")
        # frame
        self.frame = ctk.CTkFrame(self.root)

        self.welcome_text_label = ctk.CTkLabel(self.frame, text="Rewrite the following text as fast as you can:", font=("Roboto", 28))
        self.welcome_text_label.pack(padx=10, pady=40)

        self.sample_label = ctk.CTkLabel(self.frame, text=choice(self.texts), font=self.my_font)
        self.sample_label.pack(padx=10, pady=20)

        self.user_input = ctk.CTkEntry(self.frame, width=800, font=self.my_font)
        self.user_input.pack(padx=10, pady=80)
        self.user_input.bind("<KeyRelease>", self.start)

        self.speed_label = ctk.CTkLabel(self.frame, text="Speed: \n0.00 WPS\n0.00 WPM", font=self.my_font)
        self.speed_label.pack(padx=10, pady=20)

        self.reset_button = ctk.CTkButton(self.frame, text="Reset", command=self.reset, font=self.my_font)
        self.reset_button.pack(padx=10, pady=20)

        self.frame.pack(padx=40, pady=40, fill="both", expand=True)

        # counter
        self.counter = 0
        self.running = False

        self.root.mainloop()

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
            self.speed_label.configure(text=f"Speed: \n{wps: .2f} WPS\n{wpm: .2f}WPM")

    # resetting the test
    def reset(self):
        self.running = False
        self.counter = 0
        self.speed_label.configure(text="Speed: \n0.00 WPS\n0.00 WPM")
        self.sample_label.configure(text=choice(self.texts))
        self.user_input.delete(0, ctk.END)


SpeedTypingApp()
