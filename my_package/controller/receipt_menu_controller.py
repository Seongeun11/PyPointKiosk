#my_package\controller\receipt_menu_controller.py
from PySide6.QtCore import QObject, Signal

class ReceiptMenuController(QObject):
    """영수증 화면 Controller"""
    # 최상위 MainController로 완료 처리를 알리는 시그널
    complete_requested_signal = Signal()

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        # View 이벤트 바인딩
        self.view.confirm_clicked_signal.connect(self.handle_confirm)

    def handle_confirm(self):
        """확인 버튼 클릭 시 처리"""
        self.complete_requested_signal.emit()

    def set_receipt_text(self, receipt_text: str):
        """View에 영수증 텍스트 전달"""
        self.view.display_receipt_text(receipt_text)