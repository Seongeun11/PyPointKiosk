from PySide6.QtWidgets import (
    QDialog, QSizePolicy, QVBoxLayout, QHBoxLayout, QLabel, 
    QSpinBox, QPushButton, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from my_package.utils.base_scaled_manager import BaseScaledDialog

class DiscountDialog(BaseScaledDialog):
    """금액/퍼센트 할인 선택 다이얼로그"""
    BASE_WIDTH = 720.0
    BASE_HEIGHT = 720.0
    BASE_FONT_SIZE = 28
    MIN_FONT_SIZE = 24
    MAX_FONT_SIZE = 34

    PRESETS_KRW = [1000, 3000, 5000, 10000]
    PRESETS_JPY = [100, 300, 500, 1000]
    PRESETS_PERCENT = [5, 10, 15, 20, 30, 50]  # 퍼센트 할인 프리셋 추가

    def __init__(self, title: str, discount_type: str, purchase_amount: int, current_discount: int = 0, currency: str = "KRW", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(720, 720)
        self.setModal(True)
        self.discount_type = discount_type  # 'student', 'academy', 'coupon'
        self.purchase_amount = purchase_amount
        self.accumulated_discount = current_discount  # 최종 할인 금액
        self.currency = currency
        self.unit = "¥" if currency == "JPY" else "원"
        
        # 퍼센트 모드 여부 판단 (coupon 타입일 경우 퍼센트 할인으로 동작)
        self.is_percent_mode = (discount_type == "coupon")
        self.setWindowFlags(
                            Qt.WindowType.Window | 
                            Qt.WindowType.CustomizeWindowHint | 
                            Qt.WindowType.WindowTitleHint | 
                            Qt.WindowType.WindowMinimizeButtonHint | 
                            Qt.WindowType.WindowMaximizeButtonHint | 
                            Qt.WindowType.WindowCloseButtonHint
                        )
        self._init_ui()
        self._update_display()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # 1. 구매 금액 & 누적 할인 금액 표시 레이블
        info_group = QGroupBox("할인 누적 현황")
        info_layout = QVBoxLayout()
        
        self.lbl_purchase_info = QLabel(f"총 주문 금액: {self.purchase_amount:,} {self.unit}")
        self.lbl_purchase_info.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        self.lbl_discount_info = QLabel(f"현재 누적 할인: -{self.accumulated_discount:,} {self.unit}")
        self.lbl_final_info = QLabel(f"예상 결제 금액: {max(0, self.purchase_amount - self.accumulated_discount):,} {self.unit}")

        self.lbl_discount_info.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.lbl_final_info.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        palette_red = self.lbl_discount_info.palette()
        palette_red.setColor(QPalette.ColorRole.WindowText, QColor("#D32F2F"))
        self.lbl_discount_info.setPalette(palette_red)

        palette_blue = self.lbl_final_info.palette()
        palette_blue.setColor(QPalette.ColorRole.WindowText, QColor("#1976D2"))
        self.lbl_final_info.setPalette(palette_blue)

        info_layout.addWidget(self.lbl_purchase_info)
        info_layout.addWidget(self.lbl_discount_info)
        info_layout.addWidget(self.lbl_final_info)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # 2. 빠른 할인 추가 (퍼센트 모드 vs 금액 모드)
        preset_title = "빠른 퍼센트 할인 선택 (%)" if self.is_percent_mode else "빠른 금액 추가 (+)"
        preset_group = QGroupBox(preset_title)
        preset_layout = QHBoxLayout()

        if self.is_percent_mode:
            for pct in self.PRESETS_PERCENT:
                btn = QPushButton(f"{pct}%")
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #E8F5E9; border: 1px solid #4CAF50;
                        border-radius: 4px; padding: 8px; font-weight: bold;
                    }
                    QPushButton:hover { background-color: #C8E6C9; }
                """)
                btn.clicked.connect(lambda checked, p=pct: self._apply_percent_discount(p))
                preset_layout.addWidget(btn)
        else:
            amounts = self.PRESETS_JPY if self.currency == "JPY" else self.PRESETS_KRW
            for amt in amounts:
                btn = QPushButton(f"+{amt:,}{self.unit}")
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #E3F2FD; border: 1px solid #2196F3;
                        border-radius: 4px; padding: 8px;
                    }
                    QPushButton:hover { background-color: #BBDEFB; }
                """)
                btn.clicked.connect(lambda checked, a=amt: self._add_discount(a))
                preset_layout.addWidget(btn)

        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)

        # 3. 직접 입력 (퍼센트 모드 vs 금액 모드)
        custom_title = "직접 퍼센트 입력 (%)" if self.is_percent_mode else "직접 금액 추가"
        custom_group = QGroupBox(custom_title)
        custom_layout = QHBoxLayout()
        
        self.sb_custom = QSpinBox()
        self.sb_custom.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        if self.is_percent_mode:
            self.sb_custom.setRange(0, 100)
            self.sb_custom.setSingleStep(5)
            self.sb_custom.setSuffix(" %")
            btn_add_custom = QPushButton("퍼센트 할인 적용")
        else:
            self.sb_custom.setRange(0, 10000000)
            self.sb_custom.setSingleStep(500)
            self.sb_custom.setSuffix(f" {self.unit}")
            btn_add_custom = QPushButton("금액 추가")

        btn_add_custom.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn_add_custom.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        btn_add_custom.clicked.connect(self._on_add_custom_clicked)

        custom_layout.addWidget(self.sb_custom)
        custom_layout.addWidget(btn_add_custom)
        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)

        # 4. 하단 제어 버튼
        action_layout = QHBoxLayout()
        
        btn_reset = QPushButton("할인 초기화")
        btn_reset.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
        btn_reset.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn_reset.clicked.connect(self._reset_discount)

        btn_apply = QPushButton("적용 완료")
        btn_apply.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 6px;")
        btn_apply.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        btn_apply.clicked.connect(self.accept)

        action_layout.addWidget(btn_reset)
        action_layout.addStretch()
        action_layout.addWidget(btn_apply)

        layout.addLayout(action_layout)

    def _apply_percent_discount(self, percent: int):
        """구매 금액에서 퍼센트 할인액 계산 적용"""
        calculated_discount = int(self.purchase_amount * (percent / 100.0))
        self.accumulated_discount = calculated_discount
        self._update_display()

    def _add_discount(self, amount: int):
        """금액 누적 차감 로직"""
        new_total = self.accumulated_discount + amount
        if new_total > self.purchase_amount:
            QMessageBox.warning(self, "경고", f"할인 금액이 총 주문 금액({self.purchase_amount:,}{self.unit})을 초과할 수 없습니다.")
            self.accumulated_discount = self.purchase_amount
        else:
            self.accumulated_discount = new_total
        self._update_display()

    def _on_add_custom_clicked(self):
        val = self.sb_custom.value()
        if self.is_percent_mode:
            self._apply_percent_discount(val)
        else:
            if val > 0:
                self._add_discount(val)
                self.sb_custom.setValue(0)

    def _reset_discount(self):
        self.accumulated_discount = 0
        if hasattr(self, 'sb_custom'):
            self.sb_custom.setValue(0)
        self._update_display()

    def _update_display(self):
        self.lbl_discount_info.setText(f"현재 누적 할인: -{self.accumulated_discount:,} {self.unit}")
        final_amt = max(0, self.purchase_amount - self.accumulated_discount)
        self.lbl_final_info.setText(f"예상 결제 금액: {final_amt:,} {self.unit}")

    def get_discount_amount(self) -> int:
        return self.accumulated_discount