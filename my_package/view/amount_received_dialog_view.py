from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, 
    QSpinBox, QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from my_package.utils.base_scaled_manager import BaseScaledDialog
class AmountReceivedDialog(BaseScaledDialog):
    """현금 + 쿠폰 복합 입력 및 거스름돈 계산 다이얼로그"""
    
    PRESETS_KRW = [10,100,1000, 5000, 10000, 50000]
    PRESETS_JPY = [1,10,100, 500, 1000, 5000]
    # [신규] 쿠폰 금액 빠른 추가 프리셋 정의
    COUPON_PRESETS_KRW = [1000, 3000, 5000, 10000]
    COUPON_PRESETS_JPY = [100, 300, 500, 1000]

    def __init__(self, title: str, final_amount: int, current_cash: int = 0, current_coupon: int = 0, 
                 currency: str = "KRW", lang_mode: str = "ko_krw", parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.resize(480, 720)
        self.setWindowFlags(
                    Qt.WindowType.Window | 
                    Qt.WindowType.CustomizeWindowHint | 
                    Qt.WindowType.WindowTitleHint | 
                    Qt.WindowType.WindowMinimizeButtonHint | 
                    Qt.WindowType.WindowMaximizeButtonHint | 
                    Qt.WindowType.WindowCloseButtonHint
                )
        self.final_amount = final_amount
        self.cash_amount = current_cash
        self.coupon_amount = current_coupon
        self.currency = currency
        self.lang_mode = lang_mode
        
        # 판단 기준 분리
        self.is_jpy = (currency == "JPY" or "jpy" in lang_mode)
        self.is_ja = (lang_mode == "ja_jpy")  # ja_jpy 일 때만 일본어 표기
        self.unit = "¥" if self.is_jpy else "원"

        self._init_ui()
        self._update_display()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # ja_jpy 조건일 때만 일본어 문구 세팅
        if self.is_ja:
            txt_status_group = "決済およびお支払い状況"
            txt_cash_group = "現金追加 (+)"
            txt_coupon_group = "クーポン追加 (+)"
            txt_reset = " clear "
            txt_apply = "入力完了"
        else:
            txt_status_group = "결제 및 지불 현황"
            txt_cash_group = "현금 추가 (+)"
            txt_coupon_group = "쿠폰 추가 (+)"
            txt_reset = "전체 초기화"
            txt_apply = "입력 완료"

        # 1. 현황 표시 그룹
        info_group = QGroupBox(txt_status_group)
        info_layout = QVBoxLayout()
        
        self.lbl_final_info = QLabel()
        self.lbl_cash_info = QLabel()
        self.lbl_coupon_info = QLabel()
        self.lbl_total_info = QLabel()
        self.lbl_change_info = QLabel()

        # 색상 강조
        p_blue = QPalette()
        p_blue.setColor(QPalette.ColorRole.WindowText, QColor("#1976D2"))
        self.lbl_total_info.setPalette(p_blue)

        p_red = QPalette()
        p_red.setColor(QPalette.ColorRole.WindowText, QColor("#D32F2F"))
        self.lbl_change_info.setPalette(p_red)

        info_layout.addWidget(self.lbl_final_info)
        info_layout.addWidget(self.lbl_cash_info)
        info_layout.addWidget(self.lbl_coupon_info)
        info_layout.addWidget(self.lbl_total_info)
        info_layout.addWidget(self.lbl_change_info)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # 2. 현금 빠른 추가
        preset_group = QGroupBox("현금 추가 (+)")
        preset_layout = QHBoxLayout()
        amounts = self.PRESETS_JPY if self.currency == "JPY" else self.PRESETS_KRW

        for amt in amounts:
            btn = QPushButton(f"+{amt:,}{self.unit}")
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            p_b_background = QPalette()
            p_b_background.setColor(QPalette.ColorRole.Button, QColor("#FFaa00"))
            btn.setPalette(p_b_background)
            #btn.setStyleSheet("background-color: #E8F5E9; border: 1px solid #4CAF50; padding: 6px;")
            btn.clicked.connect(lambda checked, a=amt: self._add_cash(a))
            preset_layout.addWidget(btn)

        preset_group.setLayout(preset_layout)
        layout.addWidget(preset_group)

        # 3. 쿠폰 빠른 추가 [개편: 버튼 방식]
        coupon_group = QGroupBox("쿠폰 추가 (+)")
        coupon_layout = QHBoxLayout()
        coupon_amounts = self.COUPON_PRESETS_JPY if self.currency == "JPY" else self.COUPON_PRESETS_KRW

        for amt in coupon_amounts:
            btn_coupon_discount = QPushButton(f"+{amt:,}{self.unit}")
            btn_coupon_discount.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            p_b_c_background = QPalette()
            p_b_c_background.setColor(QPalette.ColorRole.Button, QColor("#5EE022"))
            btn_coupon_discount.setPalette(p_b_c_background)
            btn_coupon_discount.clicked.connect(lambda checked, a=amt: self._add_coupon(a))
            coupon_layout.addWidget(btn_coupon_discount)

        coupon_group.setLayout(coupon_layout)
        layout.addWidget(coupon_group)

        # 4. 하단 버튼
        action_layout = QHBoxLayout()
        btn_reset = QPushButton("전체 초기화")
        btn_reset.setSizePolicy(
                                    QSizePolicy.Policy.Expanding, 
                                    QSizePolicy.Policy.Expanding
                                )
        p_b_r_background = QPalette()
        p_b_r_background.setColor(QPalette.ColorRole.Button, QColor("#EE532D"))
        btn_reset.setPalette(p_b_r_background)
        #btn_reset.setStyleSheet("background-color: #FF9800; color: white; font-weight: bold;")
        btn_reset.clicked.connect(self._reset_all)

        btn_apply = QPushButton("입력 완료")
        btn_apply.setSizePolicy(
                                            QSizePolicy.Policy.Expanding, 
                                            QSizePolicy.Policy.Expanding
                                        )
        
        p_b_aply_background = QPalette()
        p_b_aply_background.setColor(QPalette.ColorRole.Button, QColor("#3394E4"))
        btn_apply.setPalette(p_b_aply_background)
        #btn_apply.setStyleSheet("background-color: #2196F3; color: white; font-weight: bold; padding: 8px;")
        btn_apply.clicked.connect(self.accept)

        action_layout.addWidget(btn_reset)
        action_layout.addStretch()
        action_layout.addWidget(btn_apply)
        layout.addLayout(action_layout)

    def _add_cash(self, amount: int):
        self.cash_amount += amount
        self._update_display()
    #쿠폰 금액 추가 핸들러
    def _add_coupon(self, amount: int):
        self.coupon_amount += amount
        self._update_display()
    #def _on_add_coupon_clicked(self):
    #    val = self.sb_coupon.value()
    #    if val > 0:
    #        self.coupon_amount += val
    #        self.sb_coupon.setValue(0)
    #        self._update_display()

    def _reset_all(self):
        self.cash_amount = 0
        self.coupon_amount = 0
        self._update_display()

    def _update_display(self):
        total_received = self.cash_amount + self.coupon_amount
        change = max(0, total_received - self.final_amount)

        # ja_jpy 일 때만 일본어 출력
        if self.is_ja:
            self.lbl_final_info.setText(f"最終決済金額: ¥{self.final_amount:,}")
            self.lbl_cash_info.setText(f"お預かり(現金): ¥{self.cash_amount:,}")
            self.lbl_coupon_info.setText(f"お預かり(クーポン): ¥{self.coupon_amount:,}")
            self.lbl_total_info.setText(f"お預かり合計: ¥{total_received:,}")
            self.lbl_change_info.setText(f"お釣り: ¥{change:,}")
        else:
            # ko_krw 및 ko_jpy는 모두 한국어로 출력 (단위만 원/¥ 변경)
            self.lbl_final_info.setText(f"최종 결제 금액: {self.lbl_format(self.final_amount)}")
            self.lbl_cash_info.setText(f"받은 현금: {self.lbl_format(self.cash_amount)}")
            self.lbl_coupon_info.setText(f"받은 쿠폰: {self.lbl_format(self.coupon_amount)}")
            self.lbl_total_info.setText(f"총 받은 금액: {self.lbl_format(total_received)}")
            self.lbl_change_info.setText(f"거스름돈 (현금 반환): {self.lbl_format(change)}")

    def lbl_format(self, amount: int) -> str:
        return f"¥{amount:,}" if self.is_jpy else f"{amount:,}원"

    def get_payment_values(self):
        return self.cash_amount, self.coupon_amount