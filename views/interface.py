import tkinter as tk  # Importation du module Tkinter pour créer l'interface graphique
from tkinter import ttk, messagebox  # Importation des widgets avancés et des boîtes de dialogue
from controllers.stock_controller import StockController  # Importation du contrôleur gérant les produits

# Définition de la classe Interface pour la gestion de l'application
class Interface:
    def __init__(self):
        self.root = tk.Tk()  # Création de la fenêtre principale
        self.root.title("Gestion de Stock")  # Définition du titre de la fenêtre
        self.root.configure(bg="#e0f7fa")  # Couleur de fond de la fenêtre principale
        self.controller = StockController()  # Création d'une instance du contrôleur pour gérer les produits
        self.table = None
        self.afficher_produits()  # Appel de la méthode pour afficher les produits dès le lancement

    def afficher_produits(self):
        # Récupérer la liste des produits depuis le contrôleur
        produits = self.controller.lister_produits()

        # Supprimer tous les widgets existants pour rafraîchir l'affichage
        for widget in self.root.winfo_children():
            widget.destroy()

        # Création d'un cadre (Frame) pour contenir le tableau des produits
        frame_tableau = tk.Frame(self.root, bg="#e0f7fa")
        frame_tableau.pack(pady=10)  # Ajout d'un espace autour du cadre

        # Ajout d'un titre à la fenêtre
        tk.Label(self.root, text="Liste des Produits", font=("Helvetica", 16), bg="#e0f7fa").pack()

        # Création d'un tableau (Treeview) pour afficher les produits sous forme de tableau
        self.table = ttk.Treeview(frame_tableau, columns=("ID", "Nom", "Description", "Quantité", "Prix"), show="headings")
        self.table.heading("ID", text="ID")  # Définition des en-têtes de colonnes
        self.table.heading("Nom", text="Nom")
        self.table.heading("Description", text="Description")
        self.table.heading("Quantité", text="Quantité")
        self.table.heading("Prix", text="Prix (€)")
        self.table.pack()  # Affichage du tableau

        # Attacher l'événement de sélection
        self.table.bind("<<TreeviewSelect>>", self.remplir_champs_modification)

        # Remplissage du tableau avec les produits récupérés depuis la base de données
        for produit in produits:
            self.table.insert("", tk.END, values=(produit[0], produit[1], produit[2], produit[3], produit[4]))

        # Création d'un cadre pour contenir les champs de saisie des produits
        frame_formulaire = tk.Frame(self.root, bg="#e0f7fa")
        frame_formulaire.pack(pady=10)

        # Champs de saisie pour l'ajout/modification de produit
        tk.Label(frame_formulaire, text="Nom:", bg="#e0f7fa").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.nom_entry = tk.Entry(frame_formulaire)
        self.nom_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_formulaire, text="Description:", bg="#e0f7fa").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.description_entry = tk.Entry(frame_formulaire)
        self.description_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_formulaire, text="Quantité:", bg="#e0f7fa").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.quantite_entry = tk.Entry(frame_formulaire)
        self.quantite_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_formulaire, text="Prix:", bg="#e0f7fa").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.prix_entry = tk.Entry(frame_formulaire)
        self.prix_entry.grid(row=3, column=1, padx=5, pady=5)

        # Champs de saisie pour l'ID des produits à modifier ou supprimer
        tk.Label(frame_formulaire, text="ID Produit à Modifier:", bg="#e0f7fa").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.id_modifier_entry = tk.Entry(frame_formulaire)
        self.id_modifier_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(frame_formulaire, text="ID Produit à Supprimer:", bg="#e0f7fa").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.id_supprimer_entry = tk.Entry(frame_formulaire)
        self.id_supprimer_entry.grid(row=5, column=1, padx=5, pady=5)

        # Création d'un cadre pour les boutons d'action
        frame_buttons = tk.Frame(self.root, bg="#e0f7fa")
        frame_buttons.pack(pady=10)

        # Boutons pour ajouter, modifier et supprimer les produits
        tk.Button(frame_buttons, text="Ajouter Produit", command=self.ajouter_produit, bg="#4CAF50", fg="white").grid(row=0, column=0, padx=10)
        tk.Button(frame_buttons, text="Modifier Produit", command=self.modifier_produit, bg="#2196F3", fg="white").grid(row=0, column=1, padx=10)
        tk.Button(frame_buttons, text="Supprimer Produit", command=self.supprimer_produit, bg="#f44336", fg="white").grid(row=0, column=2, padx=10)

        # Création d'un cadre pour la gestion des mouvements de stock
        frame_mouvement = tk.Frame(self.root, bg="#e0f7fa")
        frame_mouvement.pack(pady=10)
        
        tk.Label(frame_mouvement, text="ID Produit:", bg="#e0f7fa").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.id_mouvement_entry = tk.Entry(frame_mouvement)
        self.id_mouvement_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(frame_mouvement, text="Quantité:", bg="#e0f7fa").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.quantite_mouvement_entry = tk.Entry(frame_mouvement)
        self.quantite_mouvement_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(frame_mouvement, text="Enregistrer Entrée", 
                  command=lambda: self.enregistrer_mouvement("entrée"), bg="#4CAF50", fg="white").grid(row=2, column=0, padx=5, pady=5)
        tk.Button(frame_mouvement, text="Enregistrer Sortie", 
                  command=lambda: self.enregistrer_mouvement("sortie"), bg="#f44336", fg="white").grid(row=2, column=1, padx=5, pady=5)

        self.ajouter_boutons_rapport()

    def ajouter_produit(self):
        """ Ajoute un produit à la base de données """
        # Récupération des valeurs entrées par l'utilisateur
        nom = self.nom_entry.get()
        description = self.description_entry.get()
        quantite = self.quantite_entry.get()
        prix = self.prix_entry.get()

        # Vérification que tous les champs sont remplis
        if not (nom and description and quantite and prix):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis!")
            return

        # Vérification du type des valeurs numériques
        try:
            quantite = int(quantite)
            prix = float(prix)
        except ValueError:
            messagebox.showerror("Erreur", "La quantité doit être un entier et le prix un nombre.")
            return
        
        # Ajout du produit via le contrôleur et actualisation de l'affichage
        self.controller.ajouter_produit(nom, description, quantite, prix)
        self.afficher_produits()

    def remplir_champs_modification(self, event):
        """ Remplit les champs de modification avec les informations du produit sélectionné """
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
        """ Modifie un produit existant """
        # Récupération des valeurs du formulaire
        id_produit = self.id_modifier_entry.get()
        nom = self.nom_entry.get()
        description = self.description_entry.get()
        quantite = self.quantite_entry.get()
        prix = self.prix_entry.get()

        # Vérification que tous les champs sont remplis
        if not (id_produit and nom and description and quantite and prix):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis!")
            return

        # Vérification du type des valeurs numériques
        try:
            id_produit = int(id_produit)
            quantite = int(quantite)
            prix = float(prix)
        except ValueError:
            messagebox.showerror("Erreur", "L'ID, la quantité et le prix doivent être des nombres valides.")
            return

        # Modification du produit via le contrôleur et actualisation de l'affichage
        self.controller.modifier_produit(id_produit, nom, description, quantite, prix)
        self.afficher_produits()

    def supprimer_produit(self):
        """ Supprime un produit de la base de données """
        # Récupération de l'ID du produit à supprimer
        id_produit = self.id_supprimer_entry.get()

        # Vérification que l'ID est bien renseigné
        if not id_produit:
            messagebox.showerror("Erreur", "Veuillez entrer l'ID du produit à supprimer!")
            return

        # Vérification du type de l'ID
        try:
            id_produit = int(id_produit)
        except ValueError:
            messagebox.showerror("Erreur", "L'ID doit être un nombre valide.")
            return
        
        # Demande de confirmation avant suppression
        confirmation = messagebox.askyesno("Confirmation", f"Êtes-vous sûr de vouloir supprimer le produit avec l'ID {id_produit} ?")
        if confirmation:
            self.controller.supprimer_produit(id_produit)
            self.afficher_produits()

    def enregistrer_mouvement(self, type_mouvement):
        """ Enregistre une entrée ou une sortie de stock """
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
    
        # Enregistrement du mouvement via le contrôleur
        message = self.controller.ajouter_mouvement_stock(id_produit, quantite, type_mouvement)
        messagebox.showinfo("Information", message)
        self.afficher_produits()
        print("verification.......")
        self.controller.verifier_et_envoyer_alerte(id_produit)

    def afficher_rapport_stock(self, periode="quotidien"):
        rapport = self.controller.generer_rapport_stock(periode)
        
        if not rapport:
            messagebox.showinfo("Rapport Stock", f"Aucun mouvement de stock pour la période {periode}.")
            return
    
        # Créer une nouvelle fenêtre popup pour afficher le rapport
        rapport_fenetre = tk.Toplevel(self.root)
        rapport_fenetre.title(f"Rapport {periode.capitalize()} du Stock")
    
        # Ajouter un tableau Treeview pour l'affichage des données
        colonnes = ("Produit", "Variation", "Stock Actuel", "Rupture", "Réapprovisionnement")
        table = ttk.Treeview(rapport_fenetre, columns=colonnes, show="headings")
    
        # Configuration des colonnes
        table.heading("Produit", text="Produit")
        table.heading("Variation", text="Variation de Stock")
        table.heading("Stock Actuel", text="Stock Actuel")
        table.heading("Rupture", text="Rupture ?")
        table.heading("Réapprovisionnement", text="Besoin de Réappro ?")
    
        table.pack(pady=10)
    
        # Ajouter les données dans le tableau
        for produit, variation, stock_actuel in rapport:
            rupture = "Oui" if stock_actuel <= 0 else "Non"
            besoin_reappro = "Oui" if stock_actuel < 5 else "Non"  # Seuil de 5 unités
    
            table.insert("", tk.END, values=(produit, variation, stock_actuel, rupture, besoin_reappro))

    # Ajouter les boutons pour afficher les rapports
    def ajouter_boutons_rapport(self):
        frame_rapport = tk.Frame(self.root, bg="#e0f7fa")
        frame_rapport.pack(pady=10)

        tk.Button(frame_rapport, text="Rapport Quotidien", command=lambda: self.afficher_rapport_stock("quotidien"), bg="#2196F3", fg="white").grid(row=0, column=0, padx=10)
        tk.Button(frame_rapport, text="Rapport Hebdomadaire", command=lambda: self.afficher_rapport_stock("hebdomadaire"), bg="#2196F3", fg="white").grid(row=0, column=1, padx=10)
        tk.Button(frame_rapport, text="Rapport Mensuel", command=lambda: self.afficher_rapport_stock("mensuel"), bg="#2196F3", fg="white").grid(row=0, column=2, padx=10)

    def run(self):
        """ Démarre l'interface graphique """
        self.root.mainloop()