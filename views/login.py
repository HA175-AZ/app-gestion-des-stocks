import tkinter as tk
from tkinter import messagebox, font

class LoginWindow:
    def __init__(self, on_success):
        self.root = tk.Tk()
        self.root.title("Connexion Admin")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f4f7")

        # Police personnalisée
        title_font = font.Font(family="Helvetica", size=18, weight="bold")
        label_font = font.Font(family="Helvetica", size=12)

        # Cadre central
        frame = tk.Frame(self.root, bg="#ffffff", bd=2, relief=tk.RIDGE)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=220)

        tk.Label(frame, text="Connexion Admin", bg="#ffffff", fg="#2c3e50", font=title_font).pack(pady=(10, 20))

        tk.Label(frame, text="Identifiant:", bg="#ffffff", font=label_font).pack(anchor="w", padx=30)
        self.username_entry = tk.Entry(frame, font=label_font)
        self.username_entry.pack(padx=30, pady=(0, 10), fill="x")

        tk.Label(frame, text="Mot de passe:", bg="#ffffff", font=label_font).pack(anchor="w", padx=30)
        self.password_entry = tk.Entry(frame, show="*", font=label_font)
        self.password_entry.pack(padx=30, pady=(0, 20), fill="x")

        tk.Button(frame, text="Se connecter", bg="#2980b9", fg="#fff", font=label_font, command=self.check_login).pack(pady=(0, 10))

        self.on_success = on_success

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username == "admin" and password == "admin":
            self.root.destroy()
            self.on_success()
        else:
            messagebox.showerror("Erreur", "Identifiants incorrects")

    def run(self):
        self.root.mainloop()