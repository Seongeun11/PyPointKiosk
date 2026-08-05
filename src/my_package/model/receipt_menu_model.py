#src\my_package\model\receipt_menu_model.py
class ReceiptMenuModel:
    """영수증 화면 데이터 상태 관리 Model"""
    def __init__(self):
        self._receipt_text = ""

    def set_receipt_text(self, text: str):
        self._receipt_text = text

    def get_receipt_text(self) -> str:
        return self._receipt_text