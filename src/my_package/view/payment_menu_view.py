#src\my_package\view\payment_menu_view.py
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Signal
from ui.ui_payment_menu import Ui_Form

class PaymentMenuView(QWidget):
    """결제 메뉴 화면 View 클래스"""
    # 할인 선택 시그널
    discount_requested_signal = Signal(str)  # "student", "academy"
    # 결제 수단 선택 시그널
    pay_type_requested_signal = Signal(str)  # "cash", "bank", "point"
    # 취소/이전 시그널
    cancel_requested_signal = Signal()

    view_go_back_requested_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._connect_signals()

    def _connect_signals(self):
        # 할인 버튼
        self.ui.btn_student_discount.clicked.connect(
            lambda: self.discount_requested_signal.emit("student")
        )
        self.ui.le_academy_discount.clicked.connect(
            lambda: self.discount_requested_signal.emit("academy")
        )

        # 결제 수단 버튼
        self.ui.btn_cash_payment.clicked.connect(
            lambda: self.pay_type_requested_signal.emit("cash")
        )
        self.ui.btn_bank_transfer_payment.clicked.connect(
            lambda: self.pay_type_requested_signal.emit("bank")
        )
        self.ui.btn_academy_point_payment.clicked.connect(
            lambda: self.pay_type_requested_signal.emit("point")
        )
        self.ui.btn_back.clicked.connect(
            lambda: self.view_go_back_requested_signal.emit("goback")
        )

    # [수정] unit 매개변수 추가 및 dynamic format 적용
    def update_amounts(self, purchase_amt: int, discount_amt: int, final_pay_amt: int, unit: str = "원"):
        """금액 관련 UI 텍스트 동기화"""
        self.ui.le_purchase_amount_num.setText(f"{purchase_amt:,}{unit}")
        self.ui.le_discount_amount_num.setText(f"-{discount_amt:,}{unit}")
        self.ui.le_payment_amount_num.setText(f"{final_pay_amt:,}{unit}")