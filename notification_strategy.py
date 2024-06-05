from typing import List
from projet import Membre
class NotificationStrategy:
    def envoyer(self, message: str, destinataires: List['Membre']):
        raise NotImplementedError

class EmailNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataires: List['Membre']):
        for destinataire in destinataires:
            print(f"Envoyer un email à {destinataire.nom}: {message}")

class SMSNotificationStrategy(NotificationStrategy):
    def envoyer(self, message: str, destinataires: List['Membre']):
        for destinataire in destinataires:
            print(f"Envoyer un SMS à {destinataire.nom}: {message}")

class NotificationContext:
    def __init__(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def notifier(self, message: str, destinataires: List['Membre']):
        self.strategy.envoyer(message, destinataires)
