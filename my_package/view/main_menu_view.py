#my_package\view\main_menu_view.py
from PySide6.QtCore import Signal
# 자동 생성된 UI 클래스 import
from my_package.ui.ui_main_menu_widget import Ui_Form
from my_package.utils.base_scaled_manager import BaseScaledWidget

class MainMenuView(BaseScaledWidget):
    #main_model = MainModel()  # MainModel 인스턴스 생성
    #이벤트를 외부(Controller)로 전송하는 Signal
    start_requested = Signal(str)
    language_signal= Signal(str)
    cancel_my_order_signal=  Signal(str)
    
    #main_model = Signal(str)  # MainModel 인스턴스를 외부에서 주입받도록 변경

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setMinimumSize(720, 720)
        #self.setMinimumSize(640, 360)
        self._init_ui()

    def _init_ui(self):
        
        # 버튼 별 시그널 슬롯 개별 연결
        self.ui.btn_start_main_menu.clicked.connect(self._handle_start_clicked)
        self.ui.btn_korean.clicked.connect(self.handle_korean_clicked)
        self.ui.btn_korean_ja_cash.clicked.connect(self.handle_korean_ja_cash_clicked)
        #self.ui.btn_japanese.clicked.connect(self.handle_japanese_clicked)
        self.ui.btn_cencel_my_order.clicked.connect(self.handle_cencle_myorder_clicked)

        
    def _handle_start_clicked(self):
        self.start_requested.emit("주문하기 버튼 클릭됨")

    def handle_cencle_myorder_clicked(self):
        self.cancel_my_order_signal.emit("cencel_my_order")

    def handle_japanese_clicked(self):
        self.language_signal.emit("ja_jpy")      # [수정] 일본어 + 엔화

    def handle_korean_ja_cash_clicked(self):
        self.language_signal.emit("ko_jpy")      # [수정] 한국어 + 엔화

    def handle_korean_clicked(self):
        self.language_signal.emit("ko_krw")      # [수정] 한국어 + 원화

    def update_btn_text(self,text):
        self.ui.btn_start_main_menu.setText(text)
