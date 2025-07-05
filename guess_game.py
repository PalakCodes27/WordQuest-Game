import tkinter as tk
from tkinter import messagebox
import random
import time
import winsound

# Category words
categories = {
    "Nature": ['air', 'water', 'land', 'ocean', 'forest', 'desert', 'river', 'lake'],
    "Animals": ['tiger', 'elephant', 'giraffe', 'rabbit', 'lion', 'panda', 'zebra'],
    "Sports": ['cricket', 'football', 'tennis', 'hockey', 'kabaddi', 'boxing']
}

class WordQuest:
    def __init__(self, master):
        self.master = master
        self.master.title("🧠 Word Quest - Guess the Word!")
        self.master.geometry("700x600")
        self.master.configure(bg="#f1f6f9")
        self.master.resizable(False, False)
        self.setup_start_screen()

    def setup_start_screen(self):
        self.clear_window()

        title = tk.Label(self.master, text="🎮 Word Quest", font=("Comic Sans MS", 36, "bold"), fg="#008080", bg="#f1f6f9")
        title.pack(pady=20)

        self.category = tk.StringVar(value="Nature")
        self.difficulty = tk.StringVar(value="Medium")

        frame = tk.Frame(self.master, bg="#f1f6f9")
        frame.pack()

        tk.Label(frame, text="Select Category:", font=("Arial", 14), bg="#f1f6f9").pack(pady=5)
        for cat in categories.keys():
            tk.Radiobutton(frame, text=cat, variable=self.category, value=cat, font=("Arial", 12), bg="#f1f6f9").pack()

        tk.Label(frame, text="Select Difficulty:", font=("Arial", 14), bg="#f1f6f9").pack(pady=10)
        for level in ["Easy", "Medium", "Hard"]:
            tk.Radiobutton(frame, text=level, variable=self.difficulty, value=level, font=("Arial", 12), bg="#f1f6f9").pack()

        tk.Button(self.master, text="🚀 Start Game", font=("Arial", 16, "bold"),
                  bg="#28a745", fg="white", width=15, command=self.start_game).pack(pady=30)

    def start_game(self):
        self.word = random.choice(categories[self.category.get()])
        self.guesses = ""
        self.start_time = time.time()
        level = self.difficulty.get().lower()
        self.turns = 10 if level == "easy" else 7 if level == "medium" else 4

        self.clear_window()

        tk.Label(self.master, text="🧠 Word Quest", font=("Comic Sans MS", 28, "bold"), fg="#4b0082", bg="#f1f6f9").pack(pady=10)

        self.status_label = tk.Label(self.master, text=f"Category: {self.category.get()} | Difficulty: {self.difficulty.get()}",
                                     font=("Arial", 12), bg="#f1f6f9", fg="#333")
        self.status_label.pack()

        self.word_label = tk.Label(self.master, text="", font=("Courier", 32, "bold"), bg="#f1f6f9", fg="#111")
        self.word_label.pack(pady=20)

        self.turns_label = tk.Label(self.master, text=f"❤️ Turns Left: {self.turns}", font=("Arial", 14, "bold"), fg="#dc3545", bg="#f1f6f9")
        self.turns_label.pack()

        self.timer_label = tk.Label(self.master, text="⏱️ Time: 0.0s", font=("Arial", 12), bg="#f1f6f9")
        self.timer_label.pack(pady=5)

        self.update_displayed_word()

        self.buttons_frame = tk.Frame(self.master, bg="#f1f6f9")
        self.buttons_frame.pack(pady=10)

        self.letter_buttons = {}
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            btn = tk.Button(self.buttons_frame, text=letter, width=4, height=2, font=("Arial", 12, "bold"),
                            bg="#dee2e6", fg="#000", activebackground="#c3e6cb", relief="raised",
                            command=lambda l=letter: self.guess_letter(l))
            btn.grid(row=i // 9, column=i % 9, padx=4, pady=4)
            self.letter_buttons[letter] = btn

        self.restart_btn = tk.Button(self.master, text="🔁 Restart", command=self.setup_start_screen,
                                     font=("Arial", 12, "bold"), bg="#ffc107", fg="#111")
        self.restart_btn.pack(pady=20)

        self.update_timer()

    def guess_letter(self, letter):
        if letter in self.guesses:
            return

        self.guesses += letter
        self.letter_buttons[letter]['state'] = "disabled"

        if letter.lower() not in self.word:
            self.turns -= 1
            winsound.Beep(500, 300)
        else:
            winsound.MessageBeep()

        self.update_displayed_word()
        self.turns_label.config(text=f"❤️ Turns Left: {self.turns}")

        if self.turns == 0:
            self.end_game(win=False)

    def update_displayed_word(self):
        display = ""
        failed = 0
        for ch in self.word:
            if ch.upper() in self.guesses or ch.lower() in self.guesses:
                display += ch + " "
            else:
                display += "_ "
                failed += 1
        self.word_label.config(text=display.strip())

        if failed == 0:
            self.end_game(win=True)

    def end_game(self, win):
        end_time = time.time()
        elapsed = round(end_time - self.start_time, 2)

        for btn in self.letter_buttons.values():
            btn.config(state="disabled")

        if win:
            winsound.MessageBeep()
            messagebox.showinfo("🎉 Victory!", f"Well done! The word was '{self.word}'.\nTime: {elapsed} seconds")
        else:
            winsound.Beep(300, 500)
            messagebox.showinfo("😞 Game Over", f"You lost! The word was: '{self.word}'\nTime: {elapsed} seconds")

        self.timer_label.config(text=f"⏱️ Final Time: {elapsed} seconds")

    def update_timer(self):
        if self.turns > 0:
            now = round(time.time() - self.start_time, 2)
            self.timer_label.config(text=f"⏱️ Time: {now} seconds")
            self.master.after(1000, self.update_timer)

    def clear_window(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    app = WordQuest(root)
    root.mainloop()
