import tkinter as tk
from tkinter import ttk, messagebox, font
from controllers.stock_controller import StockController

class Interface:
    def __init__(self, on_logout=None):
        self.root = tk.Tk()
        self.root.title("Gestion de Stock - Moderne")
        self.root.geometry("950x700")
        self.root.configure(bg="#f5f6fa")
        self.controller = StockController()
        self.table = None
        self.on_logout = on_logout
        self.afficher_interface()

    def afficher_interface(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        # Bouton Déconnexion
        tk.Button(self.root, text="Déconnexion", bg="#e84118", fg="white", font=("Segoe UI", 10, "bold"),
                  command=self.deconnexion).pack(anchor="ne", padx=20, pady=10)

        # Titre principal
        title_font = font.Font(family="Segoe UI", size=22, weight="bold")
        tk.Label(self.root, text="Gestion de Stock", bg="#f5f6fa", fg="#273c75", font=title_font).pack(pady=(20, 10))

        # --- Section Tableau Produits ---
        frame_tableau = tk.LabelFrame(self.root, text="Produits", bg="#ffffff", fg="#273c75", font=("Segoe UI", 12, "bold"), bd=2, relief=tk.GROOVE)
        frame_tableau.pack(pady=10, padx=30, fill="x")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#273c75", foreground="#fff")
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="#f5f6fa", fieldbackground="#f5f6fa")
        style.map("Treeview", background=[("selected", "#dff9fb")])

        self.table = ttk.Treeview(frame_tableau, columns=("ID", "Nom", "Description", "Quantité", "Prix"), show="headings", height=7)
        for col in ("ID", "Nom", "Description", "Quantité", "Prix"):
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=120)
        self.table.pack(fill="x", padx=10, pady=10)
        self.table.bind("<<TreeviewSelect>>", self.remplir_champs_modification)

        self.afficher_produits()

        # --- Section Formulaire Produit ---
        frame_form = tk.LabelFrame(self.root, text="Ajouter / Modifier / Supprimer un produit", bg="#f5f6fa", fg="#273c75", font=("Segoe UI", 12, "bold"))
        frame_form.pack(pady=10, padx=30, fill="x")

        label_font = font.Font(family="Segoe UI", size=11)
        entry_width = 22

        champs = [
            ("Nom:", "nom_entry"),
            ("Description:", "description_entry"),
            ("Quantité:", "quantite_entry"),
            ("Prix:", "prix_entry"),
            ("ID à Modifier:", "id_modifier_entry"),
            ("ID à Supprimer:", "id_supprimer_entry"),
        ]
        for i, (label, attr) in enumerate(champs):
            tk.Label(frame_form, text=label, bg="#f5f6fa", font=label_font).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = tk.Entry(frame_form, font=label_font, width=entry_width)
            entry.grid(row=i, column=1, padx=5, pady=5)
            setattr(self, attr, entry)

        # Boutons d'action stylisés
        frame_btn = tk.Frame(frame_form, bg="#ffffff")
        frame_btn.grid(row=0, column=2, rowspan=6, padx=20)
        btn_style = {"font": label_font, "width": 18, "bd": 0, "relief": tk.RIDGE, "activebackground": "#ffffff"}

        tk.Button(frame_btn, text="Ajouter Produit", bg="#44bd32", fg="white", command=self.ajouter_produit, **btn_style).pack(pady=5)
        tk.Button(frame_btn, text="Modifier Produit", bg="#0097e6", fg="white", command=self.modifier_produit, **btn_style).pack(pady=5)
        tk.Button(frame_btn, text="Supprimer Produit", bg="#e84118", fg="white", command=self.supprimer_produit, **btn_style).pack(pady=5)

        # --- Section Entrée / Sortie de Stock ---
        frame_mv = tk.LabelFrame(self.root, text="Entrée / Sortie de Stock", bg="#f5f6fa", fg="#273c75", font=("Segoe UI", 12, "bold"))
        frame_mv.pack(pady=15, padx=30, fill="x")
        tk.Label(frame_mv, text="ID Produit:", bg="#f5f6fa", font=label_font).grid(row=0, column=0, padx=5, pady=5)
        self.id_mouvement_entry = tk.Entry(frame_mv, font=label_font, width=entry_width)
        self.id_mouvement_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(frame_mv, text="Quantité:", bg="#f5f6fa", font=label_font).grid(row=1, column=0, padx=5, pady=5)
        self.quantite_mouvement_entry = tk.Entry(frame_mv, font=label_font, width=entry_width)
        self.quantite_mouvement_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(frame_mv, text="Entrée Stock", bg="#00b894", fg="white",
                  command=lambda: self.enregistrer_mouvement("entrée"), **btn_style).grid(row=2, column=0, padx=10, pady=5)
        tk.Button(frame_mv, text="Sortie Stock", bg="#fdcb6e", fg="#2d3436",
                  command=lambda: self.enregistrer_mouvement("sortie"), **btn_style).grid(row=2, column=1, padx=10, pady=5)

        self.ajouter_boutons_rapport()

    def deconnexion(self):
        self.root.destroy()
        if self.on_logout:
            self.on_logout()

    def afficher_produits(self):
        produits = self.controller.lister_produits()
        for row in self.table.get_children():
            self.table.delete(row)
        for produit in produits:
            self.table.insert("", tk.END, values=(produit[0], produit[1], produit[2], produit[3], produit[4]))

    def ajouter_produit(self):
        nom = self.nom_entry.get()
        description = self.description_entry.get()
        quantite = self.quantite_entry.get()
        prix = self.prix_entry.get()
        if not (nom and description and quantite and prix):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis!")
            return
        try:
            quantite = int(quantite)
            prix = float(prix)
        except ValueError:
            messagebox.showerror("Erreur", "La quantité doit être un entier et le prix un nombre.")
            return
        self.controller.ajouter_produit(nom, description, quantite, prix)
        self.afficher_produits()

    def remplir_champs_modification(self, event):
        selected_item = self.table.selection()
        if selected_item:
            item = self.table.item(selected_item)
            produit = item['values']
            self.id_modifier_entry.delete(0, tk.END)
            self.id_modifier_entry.insert(0, produit[0])
            self.nom_entry.delete(0, tk.END)
            self.nom_entry.insert(0, produit[1])
            self.description_entry.delete(0, tk.END)
            self.description_entry.insert(0, produit[2])
            self.quantite_entry.delete(0, tk.END)
            self.quantite_entry.insert(0, produit[3])
            self.prix_entry.delete(0, tk.END)
            self.prix_entry.insert(0, produit[4])

    def modifier_produit(self):
        id_produit = self.id_modifier_entry.get()
        nom = self.nom_entry.get()
        description = self.description_entry.get()
        quantite = self.quantite_entry.get()
        prix = self.prix_entry.get()
        if not (id_produit and nom and description and quantite and prix):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis!")
            return
        try:
            id_produit = int(id_produit)
            quantite = int(quantite)
            prix = float(prix)
        except ValueError:
            messagebox.showerror("Erreur", "L'ID, la quantité et le prix doivent être des nombres valides.")
            return
        self.controller.modifier_produit(id_produit, nom, description, quantite, prix)
        self.afficher_produits()

    def supprimer_produit(self):
        id_produit = self.id_supprimer_entry.get()
        if not id_produit:
            messagebox.showerror("Erreur", "Veuillez entrer l'ID du produit à supprimer!")
            return
        try:
            id_produit = int(id_produit)
        except ValueError:
            messagebox.showerror("Erreur", "L'ID doit être un nombre valide.")
            return
        confirmation = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer le produit avec l'ID {id_produit} ?")
        if confirmation:
            self.controller.supprimer_produit(id_produit)
            self.afficher_produits()

    def enregistrer_mouvement(self, type_mouvement):
        id_produit = self.id_mouvement_entry.get()
        quantite = self.quantite_mouvement_entry.get()
        if not (id_produit and quantite):
            messagebox.showerror("Erreur", "Veuillez renseigner l'ID et la quantité.")
            return
        try:
            id_produit = int(id_produit)
            quantite = int(quantite)
        except ValueError:
            messagebox.showerror("Erreur", "L'ID et la quantité doivent être des nombres.")
            return
        message = self.controller.ajouter_mouvement_stock(id_produit, quantite, type_mouvement)
        messagebox.showinfo("Information", message)
        self.afficher_produits()
        self.controller.verifier_et_envoyer_alerte(id_produit)

    def afficher_rapport_stock(self, periode="quotidien"):
        rapport = self.controller.generer_rapport_stock(periode)
        if not rapport:
            messagebox.showinfo("Rapport Stock", f"Aucun mouvement de stock pour la période {periode}.")
            return
        rapport_fenetre = tk.Toplevel(self.root)
        rapport_fenetre.title(f"Rapport {periode.capitalize()} du Stock")
        colonnes = ("Produit", "Variation", "Stock Actuel", "Rupture", "Réapprovisionnement")
        table = ttk.Treeview(rapport_fenetre, columns=colonnes, show="headings")
        for col in colonnes:
            table.heading(col, text=col)
        table.pack(pady=10)
        for produit, variation, stock_actuel in rapport:
            rupture = "Oui" if stock_actuel <= 0 else "Non"
            besoin_reappro = "Oui" if stock_actuel < 5 else "Non"
            table.insert("", tk.END, values=(produit, variation, stock_actuel, rupture, besoin_reappro))

    def ajouter_boutons_rapport(self):
        frame_rapport = tk.Frame(self.root, bg="#f5f6fa")
        frame_rapport.pack(pady=10)
        btn_style = {"font": ("Segoe UI", 11), "width": 18, "bd": 0, "relief": tk.RIDGE, "activebackground": "#dff9fb"}
        tk.Button(frame_rapport, text="Rapport Quotidien", command=lambda: self.afficher_rapport_stock("quotidien"),
                  bg="#0097e6", fg="white", **btn_style).grid(row=0, column=0, padx=10)
        tk.Button(frame_rapport, text="Rapport Hebdomadaire", command=lambda: self.afficher_rapport_stock("hebdomadaire"),
                  bg="#0097e6", fg="white", **btn_style).grid(row=0, column=1, padx=10)
        tk.Button(frame_rapport, text="Rapport Mensuel", command=lambda: self.afficher_rapport_stock("mensuel"),
                  bg="#0097e6", fg="white", **btn_style).grid(row=0, column=2, padx=10)

    def run(self):
        self.root.mainloop()