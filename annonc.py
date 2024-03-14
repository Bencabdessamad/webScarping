import feedparser
from bs4 import BeautifulSoup
import time

urls_flux_rss = [
    "https://www.est.um5.ac.ma/feed",
    "http://ensias.um5.ac.ma/taxonomy/term/27/feed",
]

def charger_annonces_traitees(fichier_enregistrement):
    try:
        with open(fichier_enregistrement, "r") as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def enregistrer_annonces_traitees(fichier_enregistrement, nouveaux_identifiants):
    with open(fichier_enregistrement, "a") as f:
        for identifiant in nouveaux_identifiants:
            f.write(identifiant + "\n")

def est_annonce_concours(annonce):
    mots_cles_concours = ["concours","sélection"]  # Mots-clés indiquant une annonce de concours
    titre = annonce.title.lower()
    description = annonce.description.lower() if hasattr(annonce, 'description') else ""  # Certains flux RSS peuvent ne pas avoir de description

    for mot_cle in mots_cles_concours:
        if mot_cle in titre or mot_cle in description:
            return True
    return False

while True:
    try:
        aucune_annonce_trouvee = True

        for url_flux_rss in urls_flux_rss:
            fichier_enregistrement = url_flux_rss.split("/")[-1] + "_annonces_traitees.txt"
            annonces_traitees = charger_annonces_traitees(fichier_enregistrement)
            flux = feedparser.parse(url_flux_rss)

            nouvelles_annonces = []
            for annonce in flux.entries:
                identifiant = annonce.guid  

                # Vérifier si l'annonce est liée à un concours et si elle n'a pas déjà été traitée
                if est_annonce_concours(annonce) and identifiant not in annonces_traitees:
                    titre = annonce.title
                    lien = annonce.link
                    published = annonce.published
                    description = BeautifulSoup(annonce.description, "html.parser").get_text()
                    print("Annonce pour", url_flux_rss)
                    print("Titre:", titre)
                    print("Lien:", lien)
                    print("published:", published)
                    print("description:", description)
                    print("\n")

                    nouvelles_annonces.append(identifiant)

                    aucune_annonce_trouvee = False

            enregistrer_annonces_traitees(fichier_enregistrement, nouvelles_annonces)

        if aucune_annonce_trouvee:
            print("Aucune nouvelle annonce correspondant aux critères n'a été trouvée.")

    except Exception as e:
        print("Une erreur s'est produite:", e)

    time.sleep(100)