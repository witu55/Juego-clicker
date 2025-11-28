import sys
from PyQt5.QtWidgets import QApplication
from frist_win import FirstWin
from second_win import SecondWin
from third_win import ThirdWin
from final_win import FinalWin  

def main():
    # Crear la aplicación
    app = QApplication(sys.argv)

    # Iniciar en la primera ventana
    ventana = FirstWin()
    ventana.show()

    # Ejecutar el loop principal
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
