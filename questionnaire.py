import os
import json

# Classe Question
class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    @staticmethod
    def from_dict(data):
        """Créer une instance Question à partir d'un dictionnaire."""
        return Question(
            data["titre"],
            [c[0] for c in data["choix"]],
            next(c[0] for c in data["choix"] if c[1])  # Trouver la bonne réponse
        )

    def poser(self):
        print("QUESTION")
        print("  " + self.titre)
        for i, choix in enumerate(self.choix):
            print(f"  {i+1} - {choix}")

        print()
        reponse_correcte = False
        reponse_int = Question.demander_reponse_numerique_utilisateur(1, len(self.choix))
        if self.choix[reponse_int - 1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            reponse_correcte = True
        else:
            print("Mauvaise réponse")
        print()
        return reponse_correcte

    @staticmethod
    def demander_reponse_numerique_utilisateur(min, max):
        """Demander une réponse numérique à l'utilisateur."""
        while True:
            try:
                reponse = int(input(f"Votre réponse (entre {min} et {max}) : "))
                if min <= reponse <= max:
                    return reponse
                else:
                    print("ERREUR : Vous devez entrer un nombre valide.")
            except ValueError:
                print("ERREUR : Veuillez entrer uniquement des chiffres.")


# Classe Questionnaire
class Questionnaire:
    def __init__(self, questions):
        self.questions = questions

    def lancer(self):
        """Lancer le questionnaire et afficher le score."""
        score = 0
        for question in self.questions:
            if question.poser():
                score += 1
        print(f"Score final : {score} sur {len(self.questions)}")

    @staticmethod
    def from_json(directory_path):
        """Créer un questionnaire à partir d'un répertoire contenant des fichiers JSON."""
        if not os.path.exists(directory_path):
            print(f"ERREUR : Le dossier '{directory_path}' n'existe pas.")
            return None

        # Liste pour stocker les questions chargées
        questions = []

        # Charger tous les fichiers JSON du dossier
        fichiers_json = [f for f in os.listdir(directory_path) if f.endswith(".json")]
        if not fichiers_json:
            print(f"Aucun fichier JSON trouvé dans le dossier '{directory_path}'.")
            return None

        print(f"{len(fichiers_json)} fichier(s) JSON trouvé(s) dans '{directory_path}'.\n")

        # Lire chaque fichier JSON
        for fichier in fichiers_json:
            chemin_complet = os.path.join(directory_path, fichier)
            print(f"Chargement du fichier : {fichier}")
            with open(chemin_complet, "r", encoding="utf-8") as file:
                data = json.load(file)
                questions += [Question.from_dict(q) for q in data["questions"]]

        return Questionnaire(questions)


# Programme principal
if __name__ == "__main__":
    # Spécifiez le répertoire contenant les fichiers JSON
    chemin_dossier = "./"  # Utilisez le dossier actuel où se trouve votre script

    # Charger les questions depuis les fichiers JSON
    questionnaire = Questionnaire.from_json(chemin_dossier)

    if questionnaire:
        # Lancer le questionnaire
        questionnaire.lancer()
