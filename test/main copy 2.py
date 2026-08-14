#src\my_package\main_test.py
import sys
from PySide6.QtWidgets import QApplication
from src.my_package.model.order_menu_model import OrderMenuModel
from src.my_package.view.payment_menu_view import PaymentMenuView
from src.my_package.controller.order_menu_controller import OrderMenuController

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # MVC 구성요소 생성 및 연결
    #model = OrderMenuModel("resources/products.json")
    view = PaymentMenuView()
    #controller = OrderMenuController(model, view)

    view.show()
    sys.exit(app.exec())