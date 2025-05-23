from database import Database
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class StockController:
    def __init__(self):
        self.database = Database()

    def lister_produits(self):
        return self.database.lister_produits()

    def ajouter_produit(self, nom, description, quantite, prix):
        self.database.ajouter_produit(nom, description, quantite, prix)

    def modifier_produit(self, id_produit, nom, description, quantite, prix):
        self.database.modifier_produit(id_produit, nom, description, quantite, prix)

    def supprimer_produit(self, id_produit):
        self.database.supprimer_produit(id_produit)
   
   
   
    def ajouter_mouvement_stock(self, id_produit, quantite, type_mouvement):
        # Vérification que l'ID et la quantité sont valides
        if not isinstance(id_produit, int) or not isinstance(quantite, int) or quantite <= 0:
            return "ID produit et quantité doivent être des entiers positifs."

        # Enregistrement du mouvement
        self.database.enregistrer_mouvement(id_produit, type_mouvement, quantite)
        self.database.mettre_a_jour_stock(id_produit, quantite, type_mouvement)
        return "Mouvement enregistré avec succès."
    

    def generer_rapport_stock(self, periode="quotidien"):
        return self.database.generer_rapport_stock(periode)
    




    def envoyer_notification_stock_bas(self, produit_nom, stock_actuel, email_gestionnaire):
        """ Envoie un e-mail au gestionnaire si le stock est bas """
        sender_email = "radjihalil8@gmail.com"
        sender_password = "nhdjsnrbgaigarlf"
        recipient_email = email_gestionnaire

        subject = f"Alerte Stock Bas : {produit_nom}"
        body = f"Attention, le stock du produit '{produit_nom}' est faible.\nStock actuel : {stock_actuel}\nMerci de procéder au réapprovisionnement."

        # Configuration du mail
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Connexion au serveur SMTP
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            print(f"Email envoyé à {recipient_email}")
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email : {e}")

    def verifier_et_envoyer_alerte(self, id_produit):
        """ Vérifie si un produit atteint son seuil et envoie une alerte """
        query = "SELECT nom, quantite, seuil_alerte FROM produit WHERE id = ?"
        produit = self.database.fetch_one(query, (id_produit,))

        if produit:
            nom_produit, quantite, seuil_alerte = produit
            if quantite <= seuil_alerte:
                email_gestionnaire = "radjihalil8@gmail.com"  # À remplacer par l'email réel
                self.envoyer_notification_stock_bas(nom_produit, quantite, email_gestionnaire)

