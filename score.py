from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QGroupBox
from PySide6.QtCore import QTimer
import sys

class GameScore(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Score")
        self.setFixedSize(300, 200)

        self.score = 0
        self.elapsed_seconds = 0
        self.game_over = False

        # Création du QGroupBox "Stats"
        self.stats_group = QGroupBox("Stats:")
        self.score_label = QLabel("Score : 0")
        self.score_label.setStyleSheet("font-size: 24px;")

        # Layout interne pour la groupbox
        stats_layout = QVBoxLayout()
        stats_layout.addWidget(self.score_label)
        self.stats_group.setLayout(stats_layout)

        self.status_label = QLabel("Jeu en cours...")
        self.status_label.setStyleSheet("font-size: 16px;")

        self.lose_button = QPushButton("Perdu")
        self.lose_button.clicked.connect(self.end_game)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stats_group)    # On ajoute la box "Stats"
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.lose_button)

        self.setLayout(main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_score)
        self.timer.start(1000)

    def update_score(self):
        if self.game_over:
            return

        self.elapsed_seconds += 1

        if self.elapsed_seconds <= 60:
            self.score += 10
        elif self.elapsed_seconds <= 120:
            self.score += 20
        elif self.elapsed_seconds <= 180:
            self.score += 30
        else:
            self.end_game()
            return

        self.score_label.setText(f"Score : {self.score}")
        self.status_label.setText(f"Temps écoulé : {self.elapsed_seconds} s")

    def end_game(self):
        if self.game_over:
            return

        self.elapsed_seconds += 1

        if self.elapsed_seconds <= 60:
            self.score += 10
        elif self.elapsed_seconds <= 120:
            self.score += 20
        elif self.elapsed_seconds <= 180:
            self.score += 30
        else:
            self.end_game()
            return

        self.score_label.setText(f"Score : {self.score}")
        self.status_label.setText(f"Temps écoulé : {self.elapsed_seconds} s")

    def end_game(self):
        if not self.game_over:
            self.game_over = True
            self.timer.stop()
            self.status_label.setText(f"Jeu terminé ! Score final : {self.score}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GameScore()
    window.show()
    sys.exit(app.exec())
