# recommencer.py
from collision_meteo import CollisionManager


class GameResetManager:
    """
    Gère la réinitialisation complète du jeu depuis l'état initial.
    """

    def __init__(self, main_window):
        self.main_window = main_window

    def restart_game(self):
        """
        Réinitialise le jeu :
        - Musique, score, avions
        - Pause et mode atterrissage
        - Interface et widgets de contrôle
        """
        self._reset_music()
        self._reset_score()
        self._remove_all_planes()
        self._add_initial_plane()
        self._reset_game_state()
        self._reset_interface()
        self.main_window.widget_carte.update()

    # Réinitialisation musique
    def _reset_music(self):
        """Arrête et relance la musique."""
        player = self.main_window.player
        player.stop()
        player.setPosition(0)
        player.play()

    # Réinitialisation score
    def _reset_score(self):
        """Réinitialise le score à 0."""
        self.main_window.score = 0
        self.main_window.score_label.setText("Score : 0")

    # Gestion des avions
    def _remove_all_planes(self):
        """Supprime tous les avions existants."""
        planes = list(self.main_window.widget_carte.planes)
        for plane in planes:
            try:
                self.main_window.widget_carte.remove_plane(plane)
            except Exception:
                # Retrait manuel si remove_plane échoue
                if plane in self.main_window.widget_carte.planes:
                    self.main_window.widget_carte.planes.remove(plane)

    def _add_initial_plane(self):
        """Ajoute l’avion initial ou l’état de départ."""
        if hasattr(self.main_window.widget_carte, "add_initial_plane"):
            self.main_window.widget_carte.add_initial_plane()

    # Réinitialisation des états du jeu
    def _reset_game_state(self):
        """Désactive pause et mode atterrissage, réactive les timers."""
        self.main_window.paused = False
        self.main_window.control_ground_mode = False
        self.main_window.widget_carte.set_paused(False)
        CollisionManager.paused = False

        if hasattr(self.main_window.meteo_manager, "set_paused"):
            self.main_window.meteo_manager.set_paused(False)

    # Réinitialisation interface
    def _reset_interface(self):
        """Met à jour tous les widgets affichant les stats et les avions."""
        self.main_window.update_stats()
        self.main_window.liste_avions.clearSelection()
        self.main_window.widget_carte.selected_plane = None
        self.main_window.landing_view.set_selected_plane(None)

        self.main_window.label_nom_avion.setText("Sélectionner un avion")
        self.main_window.bar_altitude.setValue(0)
        self.main_window.bar_vitesse.setValue(0)
        self.main_window.bar_fuel.setValue(0)

        # Réinitialisation de la boussole
        try:
            self.main_window.compass.set_cap(0)
        except Exception:
            pass
