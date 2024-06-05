from datetime import datetime
from projet import Projet, Membre, Tache, Jalon, Risque, Changement
from notification_strategy import EmailNotificationStrategy, SMSNotificationStrategy

# Création du projet
projet = Projet(
    "Projet A",
    "Description du projet A",
    datetime(2024, 6, 1),
    datetime(2024, 12, 31),
    100000,
)

# Ajout des membres de l'équipe
membre1 = Membre("Samb", "Chef de projet")
membre2 = Membre("Tandia", "Développeur")
projet.ajouter_membre(membre1)
projet.ajouter_membre(membre2)

# Ajout de tâches
tache1 = Tache(
    "Tâche 1",
    "Description de la tâche 1",
    datetime(2024, 6, 1),
    datetime(2024, 7, 31),
    membre1,
    "En cours",
)
tache2 = Tache(
    "Tâche 2",
    "Description de la tâche 2",
    datetime(2024, 8, 1),
    datetime(2024, 9, 30),
    membre2,
    "Pas commencée",
)
projet.ajouter_tache(tache1)
projet.ajouter_tache(tache2)

# Ajout d'un jalon
jalon1 = Jalon("Jalon 1", datetime(2024, 7, 1))
projet.ajouter_jalon(jalon1)

# Ajout d'un risque
risque1 = Risque("Risque 1", 0.5, "Élevé")
projet.ajouter_risque(risque1)

# Ajout d'un changement
projet.enregistrer_changement("Changement 1", 1)

# Stratégies de notification
email_strategy = EmailNotificationStrategy()
sms_strategy = SMSNotificationStrategy()

# Définir la stratégie de notification et notifier
projet.set_notification_strategy(email_strategy)
projet.notifier("Message important", projet.equipe.obtenir_membres())

projet.set_notification_strategy(sms_strategy)
projet.notifier("Message urgent", projet.equipe.obtenir_membres())

# Calcul du chemin critique
chemin_critique = projet.calculer_chemin_critique()
print("Chemin Critique:")
for tache in chemin_critique:
    print(f"  - {tache.nom} [{tache.date_debut} - {tache.date_fin}]")

# Générer un rapport des activités du projet
rapport = projet.generer_rapport()
print(rapport)
