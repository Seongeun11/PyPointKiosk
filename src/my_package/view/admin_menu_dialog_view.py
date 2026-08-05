#src\my_package\view\admin_menu_dialog_view.py
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QComboBox, QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QSpinBox, QGroupBox,QFileDialog
)
from PySide6.QtCore import Qt, Signal


# ==============================================================================
# [신규 추가] 마우스 휠 스크롤에 의한 값 변경을 방지하는 커스텀 ComboBox
# ==============================================================================
class NoScrollComboBox(QComboBox):
    """마우스 휠 이벤트를 무시하여 테이블 스크롤 시 의도치 않은 항목 변경을 방지하는 ComboBox"""
    def wheelEvent(self, event):
        # 휠 이벤트를 소비하지 않고 부모 위젯(QTableWidget)으로 전달
        event.ignore()


class AdminMenuDialogView(QDialog):
    export_excel_requested = Signal(str) # 파일 저장 경로 전송 시그널

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.setWindowTitle("관리자 메뉴 - 상품 및 카테고리 관리")
        #self.resize(750, 700)
        self._init_ui()
        self.refresh_all_data()

    def _init_ui(self):
        layout = QVBoxLayout(self)

        # 1. 타이틀
        title = QLabel("관리자 상품 및 카테고리 설정")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 5px;")
        layout.addWidget(title)

        
        self.btn_export_excel = QPushButton("일일 매출 엑셀 내보내기", self)
        self.btn_export_excel.setStyleSheet("padding: 12px; font-size: 14px; font-weight: bold;")
        
        self.btn_export_excel.clicked.connect(self._on_export_clicked)
        layout.addWidget(self.btn_export_excel)

        # 2. 카테고리 관리 그룹박스
        cat_group = QGroupBox("카테고리 관리")
        cat_layout = QHBoxLayout(cat_group)

        self.le_new_category = QLineEdit()
        self.le_new_category.setPlaceholderText("새 카테고리명 입력")
        self.btn_add_category = QPushButton("카테고리 추가")
        self.btn_add_category.clicked.connect(self._on_add_category)

        self.cb_delete_category = QComboBox()
        self.btn_delete_category = QPushButton("카테고리 삭제")
        self.btn_delete_category.setStyleSheet("background-color: #f44336; color: white;")
        self.btn_delete_category.clicked.connect(self._on_delete_category)

        cat_layout.addWidget(self.le_new_category)
        cat_layout.addWidget(self.btn_add_category)
        cat_layout.addWidget(QLabel(" | "))
        cat_layout.addWidget(self.cb_delete_category)
        cat_layout.addWidget(self.btn_delete_category)
        
        layout.addWidget(cat_group)

        # 3. 상품 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "카테고리", "상품명", "가격", "상태"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # 인라인 셀 수정 활성화 (더블클릭 가능)
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.EditKeyPressed
        )
        self.table.itemChanged.connect(self._on_table_item_changed)
        
        layout.addWidget(self.table)

        # 4. 상태 변경 / 삭제 버튼 영역
        btn_layout = QHBoxLayout()
        self.btn_toggle_soldout = QPushButton("판매/품절 전환")
        self.btn_toggle_soldout.clicked.connect(self._on_toggle_soldout)
        self.btn_delete = QPushButton("선택 상품 삭제")
        self.btn_delete.clicked.connect(self._on_delete_product)

        btn_layout.addWidget(self.btn_toggle_soldout)
        btn_layout.addWidget(self.btn_delete)
        layout.addLayout(btn_layout)

        # 5. 상품 추가 폼
        prod_group = QGroupBox("신규 상품 추가")
        form_group = QFormLayout(prod_group)
        
        self.cb_category = QComboBox()
        self.le_name = QLineEdit()
        self.le_name.setPlaceholderText("상품명 입력")
        
        self.sb_price = QSpinBox()
        self.sb_price.setRange(0, 1000000)
        self.sb_price.setSingleStep(500)
        self.sb_price.setValue(3000)

        form_group.addRow("카테고리:", self.cb_category)
        form_group.addRow("상품명:", self.le_name)
        form_group.addRow("가격:", self.sb_price)

        layout.addWidget(prod_group)

        # 6. 하단 버튼
        bottom_layout = QHBoxLayout()
        self.btn_add = QPushButton("상품 추가")
        self.btn_add.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 6px;")
        self.btn_add.clicked.connect(self._on_add_product)

        self.btn_close = QPushButton("닫기")
        self.btn_close.clicked.connect(self.accept)

        bottom_layout.addWidget(self.btn_add)
        bottom_layout.addWidget(self.btn_close)
        layout.addLayout(bottom_layout)

    def _on_export_clicked(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "엑셀 정산 파일 저장", "카페팀_일일_판매_보고서.xlsx", "Excel Files (*.xlsx)"
        )
        if file_path:
            try:
                from model.receipt_repository_model import ReceiptRepositoryModel
                repo = ReceiptRepositoryModel()
                repo.export_to_excel(file_path)
                QMessageBox.information(self, "성공", "엑셀 내보내기가 완료되었습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"엑셀 내보내기 중 오류가 발생했습니다:\n{e}")
                
    def refresh_all_data(self):
        """카테고리 콤보박스 및 상품 테이블 전체 갱신"""
        self._update_category_comboboxes()
        self.load_product_table()

    def _update_category_comboboxes(self):
        self.cb_category.clear()
        self.cb_delete_category.clear()

        categories = self.model.get_categories()
        for cat in categories:
            self.cb_category.addItem(cat["name"], cat["id"])
            self.cb_delete_category.addItem(cat["name"], cat["id"])

    def load_product_table(self):
        """테이블 데이터 로드 및 휠 스크롤 차단 ComboBox 적용"""
        self.table.blockSignals(True)
        self.table.setRowCount(0)

        categories = self.model.get_categories()
        cat_names = [cat["name"] for cat in categories]

        for cat in categories:
            cat_name = cat["name"]
            for p in cat.get("products", []):
                row = self.table.rowCount()
                self.table.insertRow(row)

                is_sold_out = p.get("is_sold_out", False)
                status_str = "품절" if is_sold_out else "판매중"

                # 0: ID (수정 불가)
                id_item = QTableWidgetItem(str(p["id"]))
                id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, 0, id_item)

                # 1: 카테고리 [핵심 변경] NoScrollComboBox를 사용하여 마우스 휠 스크롤 방지
                combo = NoScrollComboBox()
                combo.addItems(cat_names)
                combo.setCurrentText(cat_name)
                
                # 콤보박스 클릭 후 값 변경 시에만 이벤트 발동
                combo.currentTextChanged.connect(
                    lambda new_cat, p_id=str(p["id"]): self._on_category_combo_changed(p_id, new_cat)
                )
                self.table.setCellWidget(row, 1, combo)

                # 2: 상품명 (수정 가능)
                self.table.setItem(row, 2, QTableWidgetItem(str(p["name"])))

                # 3: 가격 (수정 가능)
                self.table.setItem(row, 3, QTableWidgetItem(str(p['price'])))

                # 4: 상태 (수정 불가)
                status_item = QTableWidgetItem(status_str)
                status_item.setFlags(status_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                if is_sold_out:
                    status_item.setForeground(Qt.GlobalColor.red)
                else:
                    status_item.setForeground(Qt.GlobalColor.blue)
                self.table.setItem(row, 4, status_item)

        self.table.blockSignals(False)

    # ==========================================
    # 이벤트 핸들러
    # ==========================================
    def _on_category_combo_changed(self, product_id: str, new_cat_name: str):
        """테이블 셀 내 카테고리 ComboBox 변경 이벤트"""
        self.model.update_product_info(product_id, new_cat_name=new_cat_name)
        self.refresh_all_data()

    def _on_table_item_changed(self, item: QTableWidgetItem):
        """상품명(Col 2) 및 가격(Col 3) 텍스트 변경 처리"""
        row = item.row()
        col = item.column()

        p_id_item = self.table.item(row, 0)
        if not p_id_item:
            return

        p_id = p_id_item.text()
        new_val = item.text().strip()

        if col == 2:  # 상품명 수정
            if not new_val:
                QMessageBox.warning(self, "경고", "상품명은 비어 둘 수 없습니다.")
                self.load_product_table()
                return

            self.model.update_product_info(p_id, new_name=new_val)

        elif col == 3:  # 가격 수정
            clean_val = new_val.replace("원", "").replace(",", "").strip()
            if not clean_val.isdigit():
                QMessageBox.warning(self, "경고", "가격은 숫자만 입력해 주세요.")
                self.load_product_table()
                return

            self.model.update_product_info(p_id, new_price=int(clean_val))
            self.load_product_table()

    def _on_add_category(self):
        cat_name = self.le_new_category.text().strip()
        if not cat_name:
            QMessageBox.warning(self, "경고", "추가할 카테고리명을 입력해주세요.")
            return

        if self.model.add_category(cat_name):
            QMessageBox.information(self, "완료", f"'{cat_name}' 카테고리가 추가되었습니다.")
            self.le_new_category.clear()
            self.refresh_all_data()
        else:
            QMessageBox.warning(self, "오류", "카테고리 추가에 실패했습니다.")

    def _on_delete_category(self):
        cat_id = self.cb_delete_category.currentData()
        cat_name = self.cb_delete_category.currentText()

        if not cat_id:
            QMessageBox.warning(self, "경고", "삭제할 카테고리를 선택해주세요.")
            return

        reply = QMessageBox.question(
            self, "삭제 확인", f"'{cat_name}' 카테고리를 정말 삭제하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            success, msg = self.model.remove_category(cat_id)
            if success:
                QMessageBox.information(self, "성공", msg)
                self.refresh_all_data()
            else:
                QMessageBox.warning(self, "삭제 불가", msg)

    def _get_selected_product_id(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "경고", "상품을 선택해주세요.")
            return None

        row = selected_rows[0].row()
        item = self.table.item(row, 0)
        return item.text() if item else None

    def _on_toggle_soldout(self):
        p_id = self._get_selected_product_id()
        if p_id:
            self.model.toggle_sold_out(p_id)
            self.load_product_table()

    def _on_delete_product(self):
        p_id = self._get_selected_product_id()
        if p_id:
            reply = QMessageBox.question(self, "삭제 확인", "정말 삭제하시겠습니까?", 
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.model.remove_product(p_id)
                self.load_product_table()

    def _on_add_product(self):
        cat_id = self.cb_category.currentData()
        name = self.le_name.text().strip()
        price = self.sb_price.value()

        if not cat_id:
            QMessageBox.warning(self, "경고", "카테고리를 선택해주세요.")
            return

        if not name:
            QMessageBox.warning(self, "경고", "상품명을 입력해주세요.")
            return

        self.model.add_product(cat_id, name, price)
        self.le_name.clear()
        self.load_product_table()
        QMessageBox.information(self, "완료", "상품이 성공적으로 추가되었습니다.")