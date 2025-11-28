from collision_meteo import CollisionManager



class GameResetManager:
    def __init__(self, main_window):
        self.main_window = main_window

    def restart_game(self):
        # Arrêter la musique et relancer depuis le début
        self.main_window.player.stop()
        self.main_window.player.setPosition(0)
        self.main_window.player.play()

        # Réinitialiser le score
        self.main_window.score = 0
        self.main_window.score_label.setText("Score : 0")

        # Supprimer tous les avions existants
        planes = list(self.main_window.widget_carte.planes)
        for plane in planes:
            try:
                self.main_window.widget_carte.remove_plane(plane)
            except Exception:
                if plane in self.main_window.widget_carte.planes:
                    self.main_window.widget_carte.planes.remove(plane)

        # Ajouter un avion de départ (ou l’état initial)
        # Attention : il faut que tu aies une méthode pour ajouter un avion initial, par exemple :
        self.main_window.widget_carte.add_initial_plane()

        # Désactiver pause et mode atterrissage
        self.main_window.paused = False
        self.main_window.control_ground_mode = False
        self.main_window.widget_carte.set_paused(False)
        CollisionManager.paused = False
        if hasattr(self.main_window.meteo_manager, 'set_paused'):
            self.main_window.meteo_manager.set_paused(False)

        # Mettre à jour l’interface
        self.main_window.update_stats()
        self.main_window.liste_avions.clearSelection()
        self.main_window.widget_carte.selected_plane = None
        self.main_window.landing_view.set_selected_plane(None)
        self.main_window.label_nom_avion.setText("Sélectionner un avion")
        self.main_window.bar_altitude.setValue(0)
        self.main_window.bar_vitesse.setValue(0)
        self.main_window.bar_fuel.setValue(0)
        try:
            self.main_window.compass.set_cap(0)
        except Exception:
            pass

        self.main_window.widget_carte.update()
