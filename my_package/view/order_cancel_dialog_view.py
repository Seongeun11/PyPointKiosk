# my_package\view\order_cancel_dialog_view.py
from PySide6.QtWidgets import (
    QTableWidgetItem, QHeaderView, 
    QMessageBox, QAbstractItemView
)
from PySide6.QtCore import QDate, Qt
from my_package.repositories.receipt_json_repository import ReceiptRepositoryModel
from my_package.ui.ui_order_cancel_dialog import Ui_Dialog
from my_package.utils.base_scaled_manager import BaseScaledDialog
class OrderCancelDialog(BaseScaledDialog):
    """주문 취소를 위한 영수증 조회 및 취소 처리 다이얼로그"""
    
    def __init__(self, receipt_repository: ReceiptRepositoryModel, parent=None):
        super().__init__(parent)
        
        # UI 파일에서 생성된 클래스 설정
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.CustomizeWindowHint | 
            Qt.WindowType.WindowTitleHint | 
            Qt.WindowType.WindowMinimizeButtonHint | 
            Qt.WindowType.WindowMaximizeButtonHint | 
            Qt.WindowType.WindowCloseButtonHint
            )    
        self.repository = receipt_repository
        self.selected_receipt_id = None
        
        self._init_ui()
        self._load_receipts()

    def _init_ui(self):
        """Ui_Dialog 위젯들의 속성 설정 및 시그널/슬롯 연결"""
        # 1. 날짜 선택 위젯 설정
        self.ui.dted_date.setCalendarPopup(True)
        self.ui.dted_date.setDate(QDate.currentDate())
        self.ui.dted_date.dateChanged.connect(self._load_receipts)

        # 2. 영수증 테이블 위젯 설정
        self.ui.tbw_table.setColumnCount(4)
        self.ui.tbw_table.setHorizontalHeaderLabels(["ID", "결제시간", "결제금액", "상태"])
        self.ui.tbw_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.ui.tbw_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.ui.tbw_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.ui.tbw_table.itemSelectionChanged.connect(self._on_receipt_selected)

        # 3. 영수증 상세 텍스트 설정
        self.ui.txt_detail.setReadOnly(True)

        # 4. 버튼 이벤트 및 스타일 연결
        self.ui.btn_cancel_order.setStyleSheet(
            "background-color: #FF4D4D; color: white; font-weight: bold; padding: 6px 12px;"
        )
        self.ui.btn_cancel_order.clicked.connect(self._handle_cancel_order)
        self.ui.btn_close.clicked.connect(self.reject)

    def _get_selected_date_str(self) -> str:
        return self.ui.dted_date.date().toString("yyyy-MM-dd")

    def _load_receipts(self):
        """선택된 일자의 영수증 목록 로드"""
        date_str = self._get_selected_date_str()
        receipts = self.repository.get_receipts_by_date(date_str)
        
        self.ui.tbw_table.setRowCount(0)
        self.ui.txt_detail.clear()
        self.selected_receipt_id = None

        for r in receipts:
            row = self.ui.tbw_table.rowCount()
            self.ui.tbw_table.insertRow(row)

            rcpt_id = r.get("id")
            time_str = r.get("timestamp", "").split(" ")[-1] if " " in r.get("timestamp", "") else r.get("timestamp", "")
            amount = f"{r.get('final_amount', 0):,}원"
            is_canceled = r.get("is_canceled", False)
            status_str = "취소됨" if is_canceled else "정상"

            item_id = QTableWidgetItem(str(rcpt_id))
            item_id.setData(Qt.ItemDataRole.UserRole, r) # 영수증 원본 객체 바인딩

            self.ui.tbw_table.setItem(row, 0, item_id)
            self.ui.tbw_table.setItem(row, 1, QTableWidgetItem(time_str))
            self.ui.tbw_table.setItem(row, 2, QTableWidgetItem(amount))
            
            status_item = QTableWidgetItem(status_str)
            if is_canceled:
                status_item.setForeground(Qt.GlobalColor.red)
            self.ui.tbw_table.setItem(row, 3, status_item)

    def _on_receipt_selected(self):
        """테이블 선택 변경 시 영수증 텍스트 바인딩"""
        selected_rows = self.ui.tbw_table.selectedItems()
        if not selected_rows:
            self.selected_receipt_id = None
            self.ui.txt_detail.clear()
            return

        first_item = self.ui.tbw_table.item(selected_rows[0].row(), 0)
        if first_item is None:
            self.selected_receipt_id = None
            self.ui.txt_detail.clear()
            return

        receipt_data = first_item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(receipt_data, dict):
            self.selected_receipt_id = None
            self.ui.txt_detail.clear()
            return
        
        self.selected_receipt_id = receipt_data.get("id")
        self.ui.txt_detail.setPlainText(receipt_data.get("receipt_text", "영수증 텍스트 없음"))

    def _handle_cancel_order(self):
        """선택된 영수증 주문 취소 처리"""
        if self.selected_receipt_id is None:
            QMessageBox.warning(self, "경고", "취소할 영수증 내역을 선택해주세요.")
            return

        date_str = self._get_selected_date_str()
        receipts = self.repository.get_receipts_by_date(date_str)
        target = next((r for r in receipts if r.get("id") == self.selected_receipt_id), None)

        if not target:
            QMessageBox.critical(self, "오류", "선택된 영수증 정보가 존재하지 않습니다.")
            return

        if target.get("is_canceled", False):
            QMessageBox.information(self, "안내", "이미 취소된 주문입니다.")
            return

        confirm = QMessageBox.question(
            self, "주문 취소 확인", 
            f"영수증 No. {self.selected_receipt_id} 주문을 정말 취소하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            success = self.repository.cancel_receipt(self.selected_receipt_id, date_str)
            if success:
                QMessageBox.information(self, "성공", "주문이 성공적으로 취소되었습니다.")
                self._load_receipts() # 데이터 재로드
            else:
                QMessageBox.critical(self, "실패", "주문 취소 처리에 실패했습니다.")