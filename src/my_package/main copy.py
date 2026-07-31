import sys
from PySide6.QtWidgets import QApplication
from model.order_menu_model import OrderMenuModel
from view.order_menu_view import OrderMenuView
from controller.order_menu_controller import OrderMenuController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # MVC 구성요소 생성 및 연결
    model = OrderMenuModel("resources/products.json")
    view = OrderMenuView()
    controller = OrderMenuController(model, view)

    view.show()
    sys.exit(app.exec())