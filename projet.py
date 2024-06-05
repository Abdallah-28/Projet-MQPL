from datetime import datetime, timedelta
from typing import List
from notification_strategy import NotificationContext, NotificationStrategy, EmailNotificationStrategy, SMSNotificationStrategy

class Membre:
    def __init__(self, nom: str, role: str):
        self.nom = nom
        self.role = role

class Tache:
    def __init__(self, nom: str, description: str, date_debut: datetime, date_fin: datetime, responsable: Membre, statut: str):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances: List['Tache'] = []

    def ajouter_dependance(self, tache: 'Tache'):
        self.dependances.append(tache)

    def mettre_a_jour_statut(self, statut: str):
        self.statut = statut

class Jalon:
    def __init__(self, nom: str, date: datetime):
        self.nom = nom
        self.date = date

class Risque:
    def __init__(self, description: str, probabilite: float, impact: str):
        self.description = description
        self.probabilite = probabilite
        self.impact = impact

class Changement:
    def __init__(self, description: str, version: int, date: datetime):
        self.description = description
        self.version = version
        self.date = date

class Equipe:
    def __init__(self):
        self.membres: List[Membre] = []

    def ajouter_membre(self, membre: Membre):
        self.membres.append(membre)

    def obtenir_membres(self):
        return self.membres

class Projet:
    def __init__(self, nom: str, description: str, date_debut: datetime, date_fin: datetime, budget: float):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.budget = budget
        self.taches: List[Tache] = []
        self.equipe = Equipe()
        self.risques: List[Risque] = []
        self.jalons: List[Jalon] = []
        self.version = 0
        self.changements: List[Changement] = []
        self.chemin_critique: List[Tache] = []
        self.notification_context = NotificationContext(EmailNotificationStrategy())

    def set_notification_strategy(self, strategy: NotificationStrategy):
        self.notification_context = NotificationContext(strategy)

    def ajouter_tache(self, tache: Tache):
        self.taches.append(tache)
        self.notifier(f"Tâche ajoutée: {tache.nom}", self.equipe.obtenir_membres())

    def ajouter_membre(self, membre: Membre):
        self.equipe.ajouter_membre(membre)
        self.notifier(f"Membre ajouté: {membre.nom}", [membre])

    def ajouter_risque(self, risque: Risque):
        self.risques.append(risque)
        self.notifier(f"Risque ajouté: {risque.description}", self.equipe.obtenir_membres())

    def ajouter_jalon(self, jalon: Jalon):
        self.jalons.append(jalon)
        self.notifier(f"Jalon ajouté: {jalon.nom}", self.equipe.obtenir_membres())

    def enregistrer_changement(self, description: str, version: int):
        changement = Changement(description, version, datetime.now())
        self.changements.append(changement)
        self.version = version
        self.notifier(f"Changement enregistré: {description}, version {version}", self.equipe.obtenir_membres())

    def notifier(self, message: str, destinataires: List[Membre]):
        if self.notification_context:
            self.notification_context.notifier(message, destinataires)

    def calculer_chemin_critique(self):
        if not self.taches:
            return []
        
        def calculer_duree(tache):
            return (tache.date_fin - tache.date_debut).days

        chemins = []
        for tache in self.taches:
            if not tache.dependances:
                chemin = self._explorer_chemin(tache, [])
                chemins.append(chemin)

        chemins = sorted(chemins, key=lambda x: sum(calculer_duree(t) for t in x), reverse=True)
        self.chemin_critique = chemins[0]
        return self.chemin_critique

    def _explorer_chemin(self, tache, chemin):
        chemin.append(tache)
        if not tache.dependances:
            return chemin
        chemins = []
        for dependance in tache.dependances:
            chemin_temp = chemin.copy()
            chemins.append(self._explorer_chemin(dependance, chemin_temp))
        chemins = sorted(chemins, key=lambda x: sum((t.date_fin - t.date_debut).days for t in x), reverse=True)
        return chemins[0]

    def generer_rapport(self):
        rapport = f"Rapport du projet {self.nom}:\n"
        rapport += f"Description: {self.description}\n"
        rapport += f"Dates: {self.date_debut} - {self.date_fin}\n"
        rapport += f"Budget: {self.budget}\n"
        rapport += "Équipe:\n"
        for membre in self.equipe.obtenir_membres():
            rapport += f"  - {membre.nom} ({membre.role})\n"
        rapport += "Tâches:\n"
        for tache in self.taches:
            rapport += f"  - {tache.nom}: {tache.description} [{tache.date_debut} - {tache.date_fin}]\n"
        rapport += "Risques:\n"
        for risque in self.risques:
            rapport += f"  - {risque.description}: {risque.probabilite * 100}% ({risque.impact})\n"
        rapport += "Jalons:\n"
        for jalon in self.jalons:
            rapport += f"  - {jalon.nom}: {jalon.date}\n"
        rapport += "Changements:\n"
        for changement in self.changements:
            rapport += f"  - {changement.description} (v{changement.version}, {changement.date})\n"
        rapport += "Chemin Critique:\n"
        for tache in self.chemin_critique:
            rapport += f"  - {tache.nom} [{tache.date_debut} - {tache.date_fin}]\n"
        return rapport
