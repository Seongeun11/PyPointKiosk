#src\my_package\view\main_view.py
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt

class MainView(QWidget):
    #main_model = MainModel()  # MainModel 인스턴스 생성
    # 로그인 시도 이벤트를 외부(Controller/Service)로 전송하는 Signal
    start_requested = Signal(str)
    #main_model = Signal(str)  # MainModel 인스턴스를 외부에서 주입받도록 변경

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(640, 360)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.showMaximized()
        self.title_label = QLabel("환영합니다", self)
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.order_button = QPushButton("시작하기", self)
        self.order_button.setFixedSize(160, 40)
        self.order_button.clicked.connect(self._on_button_clicked)
        
        layout.addWidget(self.title_label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(20)
        layout.addWidget(self.order_button, alignment=Qt.AlignmentFlag.AlignCenter)
    def _on_button_clicked  (self):
        self.start_requested.emit("주문하기 버튼 클릭됨")