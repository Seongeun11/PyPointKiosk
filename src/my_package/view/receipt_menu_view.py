#src\my_package\view\receipt_menu_view.py
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from ui.ui_receipt_menu import Ui_Form

class ReceiptMenuView(QWidget):
    """결제 완료 영수증 화면 View"""
    # 사용자가 화면 하단의 '확인/결제완료' 버튼을 눌렀을 때 발송
    confirm_clicked_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._connect_signals()

    def _connect_signals(self):
        # UI 파일의 btn_payment_completed 시그널 연결
        if hasattr(self.ui, 'btn_payment_completed'):
            self.ui.btn_payment_completed.clicked.connect(
                lambda: self.confirm_clicked_signal.emit()
            )

    def display_receipt_text(self, receipt_text: str):
        """영수증 텍스트를 PlainTextEdit에 렌더링"""
        if hasattr(self.ui, 'txt_payment_list'):
            self.ui.txt_payment_list.setPlainText(receipt_text)