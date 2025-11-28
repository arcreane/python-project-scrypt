# game_level_manager.py

class GameLevelManager:
    """
    Gère le système de niveaux basé sur le nombre d'avions.
    - Chaque niveau correspond à +5 avions.
    - Le niveau ne redescend jamais.
    """

    def __init__(self, main_window):
        self.main_window = main_window
        self.niveau = 1
        self.max_niveau_atteint = 1

    def get_widget(self):
        """Retourne le QLabel déjà configuré pour être affiché dans le layout."""
        return self.main_window.niveau_label

    def calcul_niveau(self):
        """Calcule le niveau selon le nombre d'avions."""
        nb_avions = len(self.main_window.widget_carte.planes)

        niveau_actuel = (nb_avions // 5) + 1

        # Le niveau ne peut jamais diminuer
        if niveau_actuel > self.max_niveau_atteint:
            self.max_niveau_atteint = niveau_actuel
            self.niveau = niveau_actuel
            self.main_window.niveau_label.setText(f"Niveau : {self.niveau}")
