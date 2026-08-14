from PySide6.QtWidgets import QWidget, QPushButton, QMessageBox
from PySide6.QtCore import Signal
from ui.ui_payment_menu import Ui_Form

class PaymentMenuView(QWidget):
    """결제 메뉴 화면 View 클래스"""
    # 할인 다이얼로그 오픈 요청 시그널 ("student", "academy")
    open_discount_dialog_signal = Signal(str)
    # 할인 취소 시그널
    clear_discount_signal = Signal()
    # 결제 수단 선택 시그널
    pay_type_requested_signal = Signal(str)  # "cash", "bank", "point"
    # 뒤로가기 시그널
    view_go_back_requested_signal = Signal(str)

    # 버튼 활성화(선택 상태) 스타일시트 정의
    DISCOUNT_BTN_STYLE = """
        QPushButton {
            background-color: #F0F0F0;
            border: 1px solid #CCCCCC;
            border-radius: 4px;
            padding: 8px;
            font-weight: normal;
        }
        QPushButton:hover {
            background-color: #E0E0E0;
        }
        QPushButton:checked {
            background-color: #2196F3;
            color: white;
            font-weight: bold;
            border: 2px solid #1976D2;
        }
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
  
        self._setup_button_styles()
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):

        self.ui.btn_academy_point_payment.setEnabled(False)  # 초기에는 아카데미 포인트 결제 버튼 비활성화

    def _setup_button_styles(self):
        """할인 버튼을 Checkable 속성으로 설정 및 스타일시트 적용"""
        for btn_name in ["btn_student_discount", "btn_academy_discount"]:
            if hasattr(self.ui, btn_name):
                btn = getattr(self.ui, btn_name)
                btn.setCheckable(True)
                btn.setStyleSheet(self.DISCOUNT_BTN_STYLE)

  

    def update_discount_button_states(self, active_discount_type: str):
        """현재 선택된 할인 종류에 따라 버튼 Checked 상태를 제어"""
        if hasattr(self.ui, "btn_student_discount"):
            self.ui.btn_student_discount.setChecked(active_discount_type == "student")

        if hasattr(self.ui, "btn_academy_discount"):
            self.ui.btn_academy_discount.setChecked(active_discount_type == "academy")

    def _connect_signals(self):
        # 할인 버튼 -> 다이얼로그 호출 시그널 연결
        if hasattr(self.ui, "btn_student_discount"):
            self.ui.btn_student_discount.clicked.connect(
                lambda: self.open_discount_dialog_signal.emit("student")
            )
        if hasattr(self.ui, "btn_academy_discount"):
            self.ui.btn_academy_discount.clicked.connect(
                lambda: self.open_discount_dialog_signal.emit("academy")
            )

        # 할인 취소 버튼
        if hasattr(self.ui, "btn_all_clear_discount"):
            self.ui.btn_all_clear_discount.clicked.connect(
                lambda: self.clear_discount_signal.emit()
            )
       

        # 결제 수단 버튼
        # 결제 수단 버튼 -> 다이얼로그 확인 후 결제 진행 메서드로 연결
        if hasattr(self.ui, "btn_cash_payment"):
            self.ui.btn_cash_payment.clicked.connect(
                lambda: self._confirm_and_emit_payment("cash")
            )
        if hasattr(self.ui, "btn_bank_transfer_payment"):
            self.ui.btn_bank_transfer_payment.clicked.connect(
                lambda: self._confirm_and_emit_payment("bank")
            )
        if hasattr(self.ui, "btn_academy_point_payment"):
            self.ui.btn_academy_point_payment.clicked.connect(
                lambda: self._confirm_and_emit_payment("point")
            )

        # 뒤로가기 버튼
        if hasattr(self.ui, "btn_back"):
            self.ui.btn_back.clicked.connect(
                lambda: self.view_go_back_requested_signal.emit("goback")
            )

    def _confirm_and_emit_payment(self, pay_type: str):
        """
        [새로 추가된 로직]
        결제 수단 선택 시 다이얼로그(예/아니오) 출력 후 '예'를 누르면 시그널 발행
        """
        # 현재 화면에 표시된 최종 결제 금액 텍스트 가져오기 (있는 경우)
        final_price_text = self.ui.le_payment_amount_num.text() if hasattr(self.ui, "le_payment_amount_num") else ""

        # 결제 수단 한글/일어 라벨 매핑 (View 자체 UI 단어)
        pay_type_names = {
            "cash": "현금" if "원" in final_price_text or not final_price_text else "現金",
            "bank": "계좌이체" if "원" in final_price_text or not final_price_text else "銀行振込",
            "point": "아카데미 포인트" if "원" in final_price_text or not final_price_text else "アカデミーポイント"
        }
        pay_str = pay_type_names.get(pay_type, pay_type)

        # 언어 판단 (엔화 표시 기준)
        if "¥" in final_price_text:
            title = "決済の確認"
            message = f"[{pay_str}] で決済を進行しますか？\n最終決済金額: {final_price_text}"
        else:
            title = "결제 확인"
            message = f"[{pay_str}] (으)로 결제를 진행하시겠습니까?\n최종 결제 금액: {final_price_text}"

        # 확인 다이얼로그(QMessageBox) 생성
        reply = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No  # 기본 선택은 안전하게 '아니오'
        )

        # '예(Yes)' 선택 시에만 Controller로 결제 진행 시그널 전달
        if reply == QMessageBox.StandardButton.Yes:
            self.pay_type_requested_signal.emit(pay_type)