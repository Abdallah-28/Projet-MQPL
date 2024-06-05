import unittest
from datetime import datetime
from projet import Projet, Membre, Tache, Jalon, Risque, Changement
from notification_strategy import EmailNotificationStrategy, SMSNotificationStrategy

class TestProjet(unittest.TestCase):

    def setUp(self):
        self.projet = Projet("Projet A", "Description du projet A", datetime(2024, 6, 1), datetime(2024, 12, 31), 100000)
        self.membre1 = Membre("Samb", "Chef de projet")
        self.membre2 = Membre("Tandia", "Développeur")
        self.projet.ajouter_membre(self.membre1)
        self.projet.ajouter_membre(self.membre2)

    def test_ajouter_tache(self):
        tache = Tache("Tâche 1", "Description de la tâche 1", datetime(2024, 6, 1), datetime(2024, 7, 31), self.membre1, "En cours")
        self.projet.ajouter_tache(tache)
        self.assertIn(tache, self.projet.taches)
        self.assertEqual(len(self.projet.taches), 1)

    def test_ajouter_membre(self):
        membre3 = Membre("Ndao", "Designer")
        self.projet.ajouter_membre(membre3)
        self.assertIn(membre3, self.projet.equipe.obtenir_membres())
        self.assertEqual(len(self.projet.equipe.obtenir_membres()), 3)

    def test_ajouter_risque(self):
        risque = Risque("Risque 1", 0.5, "Élevé")
        self.projet.ajouter_risque(risque)
        self.assertIn(risque, self.projet.risques)
        self.assertEqual(len(self.projet.risques), 1)

    def test_ajouter_jalon(self):
        jalon = Jalon("Jalon 1", datetime(2024, 7, 1))
        self.projet.ajouter_jalon(jalon)
        self.assertIn(jalon, self.projet.jalons)
        self.assertEqual(len(self.projet.jalons), 1)

    def test_enregistrer_changement(self):
        self.projet.enregistrer_changement("Changement 1", 1)
        self.assertEqual(self.projet.version, 1)
        self.assertEqual(len(self.projet.changements), 1)
        self.assertEqual(self.projet.changements[0].description, "Changement 1")

    def test_notification_email(self):
        self.projet.set_notification_strategy(EmailNotificationStrategy())
        self.projet.notifier("Test Email", self.projet.equipe.obtenir_membres())

    def test_notification_sms(self):
        self.projet.set_notification_strategy(SMSNotificationStrategy())
        self.projet.notifier("Test SMS", self.projet.equipe.obtenir_membres())

    def test_calcul_chemin_critique(self):
        tache1 = Tache("Tâche 1", "Description de la tâche 1", datetime(2024, 6, 1), datetime(2024, 6, 30), self.membre1, "En cours")
        tache2 = Tache("Tâche 2", "Description de la tâche 2", datetime(2024, 7, 1), datetime(2024, 7, 31), self.membre2, "Pas commencée")
        tache3 = Tache("Tâche 3", "Description de la tâche 3", datetime(2024, 8, 1), datetime(2024, 8, 31), self.membre1, "Pas commencée")
        tache2.ajouter_dependance(tache1)
        tache3.ajouter_dependance(tache2)
        self.projet.ajouter_tache(tache1)
        self.projet.ajouter_tache(tache2)
        self.projet.ajouter_tache(tache3)

        chemin_critique = self.projet.calculer_chemin_critique()
        self.assertEqual(chemin_critique, [tache1, tache2, tache3])

    def test_generer_rapport(self):
        rapport = self.projet.generer_rapport()
        self.assertIn("Rapport du projet Projet A", rapport)
        self.assertIn("Description: Description du projet A", rapport)
        self.assertIn("Budget: 100000", rapport)

if __name__ == '__main__':
    unittest.main()
