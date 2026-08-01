from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Signal, Qt

class CartItemWidget(QWidget):
    """장바구니 QListWidget 내부 아이템 행(Row) 커스텀 위젯"""
    qty_changed_signal = Signal(str, int)  # (product_id, delta: +1 or -1)
    remove_requested_signal = Signal(str) # (product_id)

    def __init__(self, item_data: dict, parent=None):
        super().__init__(parent)
        self.product_id = item_data["id"]

        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 4, 6, 4)
        layout.setSpacing(8)

        # 1. 상품명 및 단가
        lbl_info = QLabel(f"{item_data['name']}\n{item_data['price']:,}원")
        lbl_info.setStyleSheet("font-size: 13px; font-weight: bold; color: #333333;")

        # 2. 수량 조절 버튼 및 표시
        btn_minus = QPushButton("-")
        btn_minus.setFixedSize(32, 32)
        btn_minus.setStyleSheet("font-size: 16px; font-weight: bold;")

        lbl_qty = QLabel(str(item_data["quantity"]))
        lbl_qty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_qty.setFixedWidth(28)
        lbl_qty.setStyleSheet("font-size: 14px; font-weight: bold;")

        btn_plus = QPushButton("+")
        btn_plus.setFixedSize(32, 32)
        btn_plus.setStyleSheet("font-size: 16px; font-weight: bold;")

        # 3. 삭제 버튼
        btn_del = QPushButton("X")
        btn_del.setFixedSize(32, 32)
        btn_del.setStyleSheet("background-color: #FF4D4D; color: white; font-weight: bold; font-size: 14px; border-radius: 4px;")

        # 레이아웃배치
        layout.addWidget(lbl_info, stretch=1)
        layout.addWidget(btn_minus)
        layout.addWidget(lbl_qty)
        layout.addWidget(btn_plus)
        layout.addWidget(btn_del)

        # 시그널 연결 (버튼 클릭시 이벤트 수집)
        btn_minus.clicked.connect(lambda: self.qty_changed_signal.emit(self.product_id, -1))
        btn_plus.clicked.connect(lambda: self.qty_changed_signal.emit(self.product_id, 1))
        btn_del.clicked.connect(lambda: self.remove_requested_signal.emit(self.product_id))