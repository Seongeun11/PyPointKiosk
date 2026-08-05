#src\my_package\main_test.py
import sys
from PySide6.QtWidgets import QApplication
from model.main_menu_model import MainMenuModel
from view.main_menu_view import MainMenuView
from controller.main_menu_controller import MainMenuController
from controller.main_controller import MainController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # MVC 구성요소 생성 및 연결
    model = MainMenuModel()
    view = MainMenuView()
    controller = MainMenuController(model, view)
    
    view.show()
    sys.exit(app.exec())