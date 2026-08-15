#my_package\view\discount_dialog_view.py
#------
#
# 이 뷰는 사용하지 않음. not used
#------
from PySide6.QtWidgets import (
    QDialog, QSizePolicy, QVBoxLayout, QHBoxLayout, QLabel, 
    QSpinBox, QPushButton, QGroupBox, QMessageBox
)
from PySide6.QtCore import Qt

class DiscountDialog(QDialog):
    """금액 할인 선택 및 누적 다이얼로그 (버퍼링 적용)"""
    
    PRESETS_KRW = [1000, 3000, 5000, 10000]
    PRESETS_JPY = [100, 300, 500, 1000]

    def __init__(self, title: str, purchase_amount: int, current_discount: int = 0, currency: str = "KRW", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setMinimumSize(720, 720)
        self.setModal(True)

        self.purchase_amount = purchase_amount
        self.accumulated_discount = current_discount  # 버퍼링용 임시 할인 금액
        self.currency = currency
        self.unit = "¥" if currency == "JPY" else "원"

        self._init_ui()
        self._update_display()

    def _init_ui(self):
        
        layout = QVBoxLayout(self)

        # 1. 구매 금액 & 누적 할인 금액 표시 레이블
        info_group = QGroupBox("할인 누적 현황")
        info_layout = QVBoxLayout()
        
        self.lbl_purchase_info = QLabel(f"총 주문 금액: {self.purchase_amount:,} {self.unit}")
        self.lbl_purchase_info.setSizePolicy(
                            QSizePolicy.Policy.Expanding, 
                            QSizePolicy.Policy.Expanding
                        )
        self.lbl_discount_info = QLabel(f"현재 누적 할인: -{self.accumulated_discount:,} {self.unit}")
        self.lbl_final_info = QLabel(f"예상 결제 금액: {max(0, self.purchase_amount - self.accumulated_discount):,} {self.unit}")

        self.lbl_discount_info.setSizePolicy(
                            QSizePolicy.Policy.Expanding, 
                            QSizePolicy.Policy.Expanding
                        )
        self.lbl_final_info.setSizePolicy(
                            QSizePolicy.Policy.Expanding, 
                            QSizePolicy.Policy.Expanding
                        )
        self.lbl_discount_info.setStyleSheet("font-weight: bold; color: #D32F2F; font-size: 14px;")
        self.lbl_final_info.setStyleSheet("font-weight: bold; color: #1976D2; font-size: 14px;")

        info_layout.addWidget(self.lbl_purchase_info)
        info_layout.addWidget(self.lbl_discount_info)
        info_layout.addWidget(self.lbl_final_info)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # 2. 빠른 금액 누적 프리셋 버튼
        preset_group = QGroupBox("빠른 금액 추가 (+)")
        
        preset_layout = QHBoxLayout()
        amounts = self.PRESETS_JPY if self.currency == "JPY" else self.PRESETS_KRW

        for amt in amounts:
            btn = QPushButton(f"+{amt:,}{self.unit}")
            btn.setSizePolicy(
                                                QSizePolicy.Policy.Expanding, 
                                                QSizePolicy.Policy.Expanding
                                            )
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #E3F2FD; border: 1px solid #2196F3;
                    border-radius: 4px; font-weight: bold; padding: 8px;
                }
                QPushButton:hover { background-color: #BBDEFB; }
            """)
            btn.clicked.connect(lambda checked, a=amt: self._add_discount(a))
            preset_layout.addWidget(btn)

        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)

        # 3. 임의 금액 직접 추가
        custom_group = QGroupBox("직접 금액 추가")
        custom_layout = QHBoxLayout()
        
        self.sb_custom = QSpinBox()
        self.sb_custom.setRange(0, 10000000)
        self.sb_custom.setSingleStep(500)
        self.sb_custom.setSuffix(f" {self.unit}")
        self.sb_custom.setSizePolicy(
                                    QSizePolicy.Policy.Expanding, 
                                    QSizePolicy.Policy.Expanding
                                )
        btn_add_custom = QPushButton("금액 추가")
        btn_add_custom.setSizePolicy(
                                    QSizePolicy.Policy.Expanding, 
                                    QSizePolicy.Policy.Expanding
                                )
        btn_add_custom.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold;")
        btn_add_custom.clicked.connect(self._on_add_custom_clicked)

        custom_layout.addWidget(self.sb_custom)
        custom_layout.addWidget(btn_add_custom)
        custom_group.setLayout(custom_layout)
        layout.addWidget(custom_group)

        # 4. 하단 제어 버튼 (초기화 / 적용 / 취소)
        action_layout = QHBoxLayout()
        
        btn_reset = QPushButton("할인 초기화 (0원)")
        btn_reset.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
        #btn_reset.setMinimumSize(200, 200)
        btn_reset.setSizePolicy(
                    QSizePolicy.Policy.Expanding, 
                    QSizePolicy.Policy.Expanding
                )
        btn_reset.clicked.connect(self._reset_discount)

        btn_apply = QPushButton("적용 완료")
        btn_apply.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 6px;")
        #btn_apply.setMinimumSize(200, 200)
        btn_apply.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        btn_apply.clicked.connect(self.accept)  # QDialog.Accepted 반환

        btn_cancel = QPushButton("닫기/취소")
        #btn_cancel.setMinimumSize(200, 200)
        btn_cancel.setSizePolicy(
                    QSizePolicy.Policy.Expanding, 
                    QSizePolicy.Policy.Expanding
                )
        btn_cancel.clicked.connect(self.reject)  # QDialog.Rejected 반환

        action_layout.addWidget(btn_reset)
        action_layout.addStretch()
        action_layout.addWidget(btn_apply)
        action_layout.addWidget(btn_cancel)

        layout.addLayout(action_layout)

    def _add_discount(self, amount: int):
        """금액 누적 차감 로직 (총 금액 초과 방지)"""
        new_total = self.accumulated_discount + amount
        if new_total > self.purchase_amount:
            QMessageBox.warning(self, "경고", f"할인 금액이 총 주문 금액({self.purchase_amount:,}{self.unit})을 초과할 수 없습니다.")
            self.accumulated_discount = self.purchase_amount
        else:
            self.accumulated_discount = new_total
        self._update_display()

    def _on_add_custom_clicked(self):
        val = self.sb_custom.value()
        if val > 0:
            self._add_discount(val)
            self.sb_custom.setValue(0)

    def _reset_discount(self):
        """다이얼로그 내부 임시 할인 초기화"""
        self.accumulated_discount = 0
        self._update_display()

    def _update_display(self):
        """다이얼로그 텍스트 동기화"""
        self.lbl_discount_info.setText(f"현재 누적 할인: -{self.accumulated_discount:,} {self.unit}")
        final_amt = max(0, self.purchase_amount - self.accumulated_discount)
        self.lbl_final_info.setText(f"예상 결제 금액: {final_amt:,} {self.unit}")

    def get_discount_amount(self) -> int:
        """최종 선택된 할인 금액 반환"""
        return self.accumulated_discount