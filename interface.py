import sys
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget

class MainWindow(QWidget):
   def __init__(self):
       super().__init__()
       self.setWindowTitle("QPushButton Example")
       #taille fenetre
       self.setFixedSize(QSize(1500, 800))

       # creation QPushButton :
       button = QPushButton("Commencer la partie", self)
       button.clicked.connect(self.on_button_click) # Connect signal to slot

       #forme :
       font = button.font()
       font.setPointSize(30)
       button.setFont(font)

       #alignement :
       align_top_left = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop



       #layout
       layout = QVBoxLayout()
       layout.addWidget(button)
       self.setLayout(layout)

   def on_button_click(self):
       print("Bonne chance !")

if __name__ == "__main__":
   app = QApplication([])
   window = MainWindow()
   window.show()
   app.exec()