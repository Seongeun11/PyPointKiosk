#src\my_package\view\main_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt

# 자동 생성된 UI 클래스 import
from ui.ui_main_menu import Ui_Form

class MainMenuView(QWidget):
    #main_model = MainModel()  # MainModel 인스턴스 생성
    # 로그인 시도 이벤트를 외부(Controller/Service)로 전송하는 Signal
    start_requested = Signal(str)
    #main_model = Signal(str)  # MainModel 인스턴스를 외부에서 주입받도록 변경

    def __init__(self, parent=None):
        super().__init__(parent)
        
        #self.setMinimumSize(640, 360)
        self._init_ui()

    def _init_ui(self):
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.btn_start_main_menu.clicked.connect(self._on_button_clicked)
        
        
    def _on_button_clicked  (self):
        self.start_requested.emit("주문하기 버튼 클릭됨")