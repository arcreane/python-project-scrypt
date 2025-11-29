# game_level_manager.py

class GameLevelManager:
    """
    Gère le système de niveaux basé sur le nombre d'avions dans le jeu.

    Règles :
        - Chaque niveau correspond à l'apparition de 5 avions supplémentaires.
        - Le niveau maximal atteint ne peut jamais diminuer.
    """

    def __init__(self, main_window):
        """
        Args:
            main_window: Instance de la fenêtre principale contenant le widget de la carte
                         et le QLabel de niveau.
        """
        self.main_window = main_window
        self.niveau = 1  # Niveau actuel
        self.max_niveau_atteint = 1  # Niveau maximal jamais atteint

    # Accès au widget de niveau
    def get_widget(self):
        """
        Retourne le QLabel affichant le niveau,
        déjà configuré pour être utilisé dans le layout.
        """
        return self.main_window.niveau_label

    # Calcul du niveau
    def calcul_niveau(self):
        """
        Calcule le niveau actuel en fonction du nombre d'avions
        présents sur la carte et met à jour le QLabel si nécessaire.
        """
        nb_avions = len(self.main_window.widget_carte.planes)
        niveau_actuel = (nb_avions // 5) + 1

        # Le niveau ne peut jamais diminuer
        if niveau_actuel > self.max_niveau_atteint:
            self.max_niveau_atteint = niveau_actuel
            self.niveau = niveau_actuel
            self.main_window.niveau_label.setText(f"Niveau : {self.niveau}")
