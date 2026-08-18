#my_package\view\payment_menu_view.py
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import Signal
from PySide6.QtGui import QColor, QPalette
from my_package.ui.ui_payment_menu import Ui_Form
from my_package.utils.base_scaled_manager import BaseScaledWidget

class PaymentMenuView(BaseScaledWidget):
    """결제 메뉴 화면 View 클래스"""
    # 할인 다이얼로그 오픈 요청 시그널 ("student", "academy")
    open_discount_dialog_signal = Signal(str)
    open_amount_received_dialog_signal = Signal() # [신규] 받은금액 다이얼로그 요구 시그널
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
        self.lang_mode = "ko_krw" # 기본값 설정
        self._setup_button_styles()
        self._update_text_color()
        self._init_ui()
        self._connect_signals()

    def _init_ui(self):
        self.setMinimumSize(720, 720)
        self.ui.btn_academy_point_payment.setEnabled(False)  # 초기에는 아카데미 포인트 결제 버튼 비활성화
        #self.ui.btn_coupon_discount.setEnabled(False)
        open_amount_received_dialog_signal = Signal() # [신규] 받은금액 다이얼로그 요구 시그널

    def set_bank_transfer_state(self, is_jpy: bool, is_ja: bool = False):
        """
        [핵심 요구사항 반영]
        엔화(JPY) 선택 시 계좌이체 버튼을 비활성화하고 빨간색 안내 문구 출력
        """
        if hasattr(self.ui, "btn_academy_discount"):
                    if is_jpy:
                        # 엔화 모드: 버튼 비활성화 및 안내 문구 노출
                        self.ui.btn_academy_discount.setEnabled(False)
                        self.ui.btn_student_discount.setEnabled(False)
                        notice_text = "엔화는 할인 미지원" if not is_ja else "円は研修生のみ支援"
                        self.ui.btn_academy_discount.setText(notice_text)
                        self.ui.btn_student_discount.setText(notice_text)
                        #self.lbl_bank_notice.setVisible(True)
                    else:
                        # 원화 모드: 버튼 활성화 및 안내 문구 비동기화/숨김
                        self.ui.btn_academy_discount.setEnabled(True)
                        self.ui.btn_academy_discount.setText("아카데미 할인" if not is_ja else "アカデミー割引")
                        self.ui.btn_student_discount.setEnabled(True)
                        self.ui.btn_student_discount.setText("수련생 할인" if not is_ja else "稽古生割引")
                        #self.lbl_bank_notice.setVisible(False)
        if hasattr(self.ui, "btn_bank_transfer_payment"):
            if is_jpy:
                # 엔화 모드: 버튼 비활성화 및 안내 문구 노출
                self.ui.btn_bank_transfer_payment.setEnabled(False)
                notice_text = "엔화는 현금만 지원" if not is_ja else "円決済は現金のみ対応"
                self.ui.btn_bank_transfer_payment.setText(notice_text)
                #self.lbl_bank_notice.setVisible(True)
            else:
                # 원화 모드: 버튼 활성화 및 안내 문구 비동기화/숨김
                self.ui.btn_bank_transfer_payment.setEnabled(True)
                self.ui.btn_bank_transfer_payment.setText("계좌이체" if not is_ja else "銀行振込")
                #self.lbl_bank_notice.setVisible(False)
    def _update_text_color(self):
        if hasattr(self.ui, "lb_discount_amount_num"):
        # font-weight 및 font-size를 CSS에서 제외하여 폰트 상속 유지
        # CSS 대신 QPalette를 통해 색상 적용 (폰트 스케일링 유지를 위함)
            palette_green = self.ui.lb_discount_amount_num.palette()
            palette_green.setColor(QPalette.ColorRole.WindowText, QColor("#FF3300"))
            self.ui.lb_discount_amount_num.setPalette(palette_green)
        if hasattr(self.ui, "lb_payment_amount_num"):
                # font-weight 및 font-size를 CSS에서 제외하여 폰트 상속 유지
                # CSS 대신 QPalette를 통해 색상 적용 (폰트 스케일링 유지를 위함)
                    palette_green = self.ui.lb_payment_amount_num.palette()
                    palette_green.setColor(QPalette.ColorRole.WindowText, QColor("#0026FF"))
                    self.ui.lb_payment_amount_num.setPalette(palette_green)

    def _setup_button_styles(self):
        """할인 버튼을 Checkable 속성으로 설정 및 스타일시트 적용"""
        for btn_name in ["btn_student_discount", "btn_academy_discount","btn_coupon_discount"]:
            if hasattr(self.ui, btn_name):
                btn = getattr(self.ui, btn_name)
                btn.setCheckable(True)
                #btn.setStyleSheet(self.DISCOUNT_BTN_STYLE)
                #btn_color = QPalette()
                #btn_color.setColor(QPalette.ColorRole.Button, QColor("#00A2FF"))
                #btn.setPalette(btn_color)

  

    def update_discount_button_states(self, active_discount_type: str):
        """현재 선택된 할인 종류에 따라 버튼 Checked 상태를 제어"""
        if hasattr(self.ui, "btn_student_discount"):
            self.ui.btn_student_discount.setChecked(active_discount_type == "student")

        if hasattr(self.ui, "btn_academy_discount"):
            self.ui.btn_academy_discount.setChecked(active_discount_type == "academy")

        if hasattr(self.ui,"btn_coupon_discount"):
            self.ui.btn_coupon_discount.setChecked(active_discount_type == "coupon")



    def update_payment_summary(self, purchase_amt: int, discount_amt: int, final_pay_amt: int,
                               cash_rec: int, coupon_rec: int, change_amt: int, prefix: str, unit: str):
        """[핵심] 현금(lb_amount_received_num) 및 쿠폰(lb_received_coupon_num)을 각각 분리 표기"""
        fmt = f"¥{{:,}}" if unit == "¥" else f"{{:,}}{unit}"

        if hasattr(self.ui, "lb_purchase_amount_num"):
            self.ui.lb_purchase_amount_num.setText(fmt.format(purchase_amt))
        if hasattr(self.ui, "lb_discount_amount_num"):
            disc_str = f"{prefix}-¥{discount_amt:,}" if unit == "¥" else f"{prefix}-{discount_amt:,}{unit}"
            self.ui.lb_discount_amount_num.setText(disc_str)
        if hasattr(self.ui, "lb_payment_amount_num"):
            self.ui.lb_payment_amount_num.setText(fmt.format(final_pay_amt))
        
        # 현금 분리 표기
        if hasattr(self.ui, "lb_amount_received_num"):
            self.ui.lb_amount_received_num.setText(fmt.format(cash_rec))
        # 쿠폰 분리 표기
        if hasattr(self.ui, "lb_received_coupon_num"):
            self.ui.lb_received_coupon_num.setText(fmt.format(coupon_rec))
        #거스름돈    
        if hasattr(self.ui, "lb_remaining_amount_num"):
            self.ui.lb_remaining_amount_num.setText(fmt.format(change_amt))
            btn_color = QPalette()
            btn_color.setColor(QPalette.ColorRole.WindowText, QColor("#0000FF"))
            self.ui.lb_remaining_amount_num.setPalette(btn_color)

    def _connect_signals(self):
        if hasattr(self.ui, "btn_student_discount"):
            self.ui.btn_student_discount.clicked.connect(lambda: self.open_discount_dialog_signal.emit("student"))
            
            
        if hasattr(self.ui, "btn_academy_discount"):
            self.ui.btn_academy_discount.clicked.connect(lambda: self.open_discount_dialog_signal.emit("academy"))
        if hasattr(self.ui, "btn_coupon_discount"):
            self.ui.btn_coupon_discount.clicked.connect(lambda: self.open_discount_dialog_signal.emit("coupon"))
        if hasattr(self.ui, "btn_all_clear_discount"):
            self.ui.btn_all_clear_discount.clicked.connect(lambda: self.clear_discount_signal.emit())

        if hasattr(self.ui, "btn_cash_payment"):
            self.ui.btn_cash_payment.clicked.connect(lambda: self._confirm_and_emit_payment("cash"))
            btn_color1 = QPalette()
            btn_color1.setColor(QPalette.ColorRole.Button, QColor("#7CF16C"))
            self.ui.btn_cash_payment.setPalette(btn_color1)

        if hasattr(self.ui, "btn_bank_transfer_payment"):
            self.ui.btn_bank_transfer_payment.clicked.connect(lambda: self._confirm_and_emit_payment("bank"))
            btn_color2 = QPalette()
            btn_color2.setColor(QPalette.ColorRole.Button, QColor("#6CAAF1"))
            self.ui.btn_bank_transfer_payment.setPalette(btn_color2)
        
        if hasattr(self.ui, "btn_academy_point_payment"):
            self.ui.btn_academy_point_payment.clicked.connect(lambda: self._confirm_and_emit_payment("point"))

        if hasattr(self.ui, "btn_amount_received"):
            self.ui.btn_amount_received.clicked.connect(lambda: self.open_amount_received_dialog_signal.emit())
            btn_color3 = QPalette()
            btn_color3.setColor(QPalette.ColorRole.Button, QColor("#2BB839"))
            self.ui.btn_amount_received.setPalette(btn_color3)
                            

        if hasattr(self.ui, "btn_back"):
            self.ui.btn_back.clicked.connect(lambda: self.view_go_back_requested_signal.emit("goback"))

    def set_lang_mode(self, lang_mode: str):
        """Controller로부터 lang_mode 전달받음"""
        self.lang_mode = lang_mode if lang_mode else "ko_krw"

    def _confirm_and_emit_payment(self, pay_type: str):
        """
        결제 진행 전 검증 및 확인 팝업
        - is_jpy: 통화 기호 (¥) 결정
        - is_ja: ja_jpy 인 경우에만 일본어 문구 출력
        """
        try:
            def parse_amt(text: str) -> int:
                clean = ''.join(c for c in text if c.isdigit())
                return int(clean) if clean else 0

            final_pay = parse_amt(self.ui.lb_payment_amount_num.text()) if hasattr(self.ui, "lb_payment_amount_num") else 0
            cash_rec = parse_amt(self.ui.lb_amount_received_num.text()) if hasattr(self.ui, "lb_amount_received_num") else 0
            coupon_rec = parse_amt(self.ui.lb_received_coupon_num.text()) if hasattr(self.ui, "lb_received_coupon_num") else 0
            
            total_rec = cash_rec + coupon_rec
            final_price_text = self.ui.lb_payment_amount_num.text() if hasattr(self.ui, "lb_payment_amount_num") else ""
            
            # 판단 기준 적용
            is_jpy = "jpy" in self.lang_mode
            is_ja = (self.lang_mode == "ja_jpy")

            # 1. 금액 부족 검증 팝업
            if total_rec < final_pay:
                shortage = final_pay - total_rec
                unit_symbol = "¥" if is_jpy else "원"
                
                if is_ja: # ja_jpy 인 경우만 일본어
                    title = "金額不足"
                    msg = f"お預かり金額が不足しています。\n不足金額: ¥{shortage:,}\n\n[預かり金] ボタンを押して金額を入力してください。"
                else: # ko_krw, ko_jpy 는 한국어
                    title = "금액 부족 경고"
                    msg = f"받은 금액이 결제 금액보다 부족합니다.\n부족 금액: {shortage:,}{unit_symbol}\n\n[받은 금액] 버튼을 눌러 금액을 입력해주세요."

                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Icon.Warning)
                msg_box.setWindowTitle(title)
                msg_box.setText(msg)
                #msg_box_color = QPalette()
                #msg_box_color.setColor(QPalette.ColorRole.WindowText, QColor("#C20000"))
                #msg_box.setPalette(msg_box_color)
                
                msg_box.setStyleSheet("""
                    QMessageBox { background-color: #FFFFFF; }
                    QLabel { font-size: 18px; font-weight: bold; color: #D32F2F; padding: 10px; }
                    QPushButton { min-width: 90px; min-height: 35px; font-size: 14px; font-weight: bold; }
                """)
                msg_box.exec()
                return

        except Exception as e:
            print(f"[View Validation Error] {e}")

        # 2. 결제 진행 확인 팝업
        if is_ja:
            pay_type_names = {"cash": "現金", "bank": "銀行振込", "point": "アカデミーポイント"}
            pay_str = pay_type_names.get(pay_type, pay_type)
            title = "決済の確認"
            message = f"[{pay_str}] で決済を進行しますか？\n最終決済金額: {final_price_text}"
            yes_btn_text = "はい"
            no_btn_text = "いいえ"
        else:
            pay_type_names = {"cash": "현금", "bank": "계좌이체", "point": "아카데미 포인트"}
            pay_str = pay_type_names.get(pay_type, pay_type)
            title = "결제 확인"
            message = f"[{pay_str}] (으)로 결제를 진행하시겠습니까?\n최종 결제 금액: {final_price_text}"
            yes_btn_text = "예"
            no_btn_text = "아니오"

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setStyleSheet("""
                            QMessageBox { background-color: #FFFFFF; }
                            QLabel { font-size: 18px; font-weight: bold; padding: 10px; }
                            QPushButton { min-width: 90px; min-height: 35px; font-size: 14px; font-weight: bold; }
                        """)
        msg_box.setIcon(QMessageBox.Icon.Question)

        yes_button = msg_box.addButton(yes_btn_text, QMessageBox.ButtonRole.YesRole)
        no_button = msg_box.addButton(no_btn_text, QMessageBox.ButtonRole.NoRole)
        msg_box.setDefaultButton(no_button)
        msg_box.exec()

        if msg_box.clickedButton() == yes_button:
            self.pay_type_requested_signal.emit(pay_type)