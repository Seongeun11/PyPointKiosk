#my_package\view\admin_menu_dialog_view.py

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, 
    QComboBox, QFormLayout, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QLabel, QSpinBox, QGroupBox, QFileDialog
)
from PySide6.QtCore import Qt, Signal


# ==============================================================================
# 마우스 휠 스크롤에 의한 값 변경을 방지하는 커스텀 ComboBox
# ==============================================================================
class NoScrollComboBox(QComboBox):
    """마우스 휠 이벤트를 무시하여 테이블 스크롤 시 의도치 않은 항목 변경을 방지하는 ComboBox"""
    def wheelEvent(self, event):
        event.ignore()


class AdminMenuDialogView(QDialog):
    export_excel_requested = Signal(str)  # 파일 저장 경로 전송 시그널

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        self.setWindowTitle("관리자 메뉴 - 상품 및 카테고리 관리")
        self.resize(720, 720)  # 스크롤바 및 다국어 필드 가독성을 고려한 크기 조정
        self.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.CustomizeWindowHint | 
            Qt.WindowType.WindowTitleHint | 
            Qt.WindowType.WindowMinimizeButtonHint | 
            Qt.WindowType.WindowMaximizeButtonHint | 
            Qt.WindowType.WindowCloseButtonHint
        )
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

        

        # 3. 상품 테이블 (횡 스크롤 지원 및 6개 컬럼 설정)
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "카테고리", "상품명(한국어)", "가격(원화)", "수련생 할인", "아카데미 할인", "상품명(일본어)", "가격(엔화)"
        ])
        
        # [핵심] 횡 스크롤바 활성화 및 테이블 열 설정
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        
        # 각 컬럼 기본 너비 설정
        self.table.setColumnWidth(0, 40)   # ID
        self.table.setColumnWidth(1, 100)  # 카테고리
        self.table.setColumnWidth(2, 130)  # 상품명(한국어)
        self.table.setColumnWidth(3, 80)   # 가격(원화)
        self.table.setColumnWidth(4, 90)   # 수련생 할인
        self.table.setColumnWidth(5, 90)   # 아카데미 할인
        self.table.setColumnWidth(6, 130)  # 상품명(일본어)
        self.table.setColumnWidth(7, 80)   # 가격(엔화)

        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        # 인라인 셀 수정 활성화 (더블클릭 가능)
        self.table.setEditTriggers(
            QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.EditKeyPressed
        )
        self.table.itemChanged.connect(self._on_table_item_changed)
        
        # [신규 추가] 셀 더블클릭 시그널 바인딩 (ID 열 클릭 감지용)
        self.table.itemDoubleClicked.connect(self._on_table_item_double_clicked)
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
        
        # 5. 신규 상품 추가 입력 폼 (다국어 및 엔화 지원)
        prod_group = QGroupBox("신규 상품 추가")
        form_layout = QFormLayout(prod_group)
        
        self.cb_category = QComboBox()
        self.le_name_ko = QLineEdit()
        self.le_name_ko.setPlaceholderText("예: 흑임자라떼")
        
        self.sb_price_ko = QSpinBox()
        self.sb_price_ko.setRange(0, 1000000)
        self.sb_price_ko.setSingleStep(500)
        self.sb_price_ko.setValue(3000)

        # [신규] 고정 할인 설정 폼
        self.sb_disc_student = QSpinBox()
        self.sb_disc_student.setRange(0, 1000000)
        self.sb_disc_student.setSingleStep(100)
        #self.sb_disc_student.setSuffix(" 원")

        self.sb_disc_academy = QSpinBox()
        self.sb_disc_academy.setRange(0, 1000000)
        self.sb_disc_academy.setSingleStep(100)
        #self.sb_disc_academy.setSuffix(" 원")


        self.le_name_ja = QLineEdit()
        self.le_name_ja.setPlaceholderText("예: 黒ごまラテ (비어 둘 경우 한국어 표기)")

        self.sb_price_ja = QSpinBox()
        self.sb_price_ja.setRange(0, 100000)
        self.sb_price_ja.setSingleStep(50)
        self.sb_price_ja.setValue(300)

        # [신규] 이미지 첨부 레이아웃
        img_layout = QHBoxLayout()
        self.le_image_path = QLineEdit()
        self.le_image_path.setReadOnly(True)
        self.le_image_path.setPlaceholderText("비어둘 경우 자동 생성(resources/images/{id}.png)")
        self.btn_select_image = QPushButton("이미지 선택")
        self.btn_select_image.clicked.connect(self._on_select_image)
        img_layout.addWidget(self.le_image_path)
        img_layout.addWidget(self.btn_select_image)


        form_layout.addRow("카테고리:", self.cb_category)
        form_layout.addRow("상품명(한국어):", self.le_name_ko)
        form_layout.addRow("가격(원화):", self.sb_price_ko)
        form_layout.addRow("수련생 고정 할인액:", self.sb_disc_student)
        form_layout.addRow("아카데미 고정 할인액:", self.sb_disc_academy)
        form_layout.addRow("상품명(일본어):", self.le_name_ja)
        form_layout.addRow("가격(엔화):", self.sb_price_ja)

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
                from my_package.repositories.excel_receipt_repository import ReceiptExcelExporter
                repo = ReceiptExcelExporter()
                repo.export_to_excel(file_path)
                QMessageBox.information(self, "성공", "엑셀 내보내기가 완료되었습니다.")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"엑셀 내보내기 중 오류가 발생했습니다:\n{e}")
                print(f"[Export Error] {e}")
                
    def refresh_all_data(self):
        self._update_category_comboboxes()
        self.load_product_table()

    def _update_category_comboboxes(self):
        self.cb_category.clear()
        self.cb_delete_category.clear()

        categories = self.model.get_categories()
        for cat in categories:
            self.cb_category.addItem(cat["name"], cat["title"])
            self.cb_delete_category.addItem(cat["name"], cat["title"])

    def load_product_table(self):
        self.table.blockSignals(True)
        self.table.setRowCount(0)

        raw_categories = self.model.categories
        cat_names = [cat.get("name") for cat in raw_categories]

        for cat in raw_categories:
            cat_name = cat.get("name")
            for p in cat.get("products", []):
                row = self.table.rowCount()
                self.table.insertRow(row)
                is_sold_out = p.get("is_sold_out", False)

                # 0: ID
                id_item = QTableWidgetItem(str(p.get("id")))
                id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.table.setItem(row, 0, id_item)

                # 1: 카테고리 콤보박스
                combo = NoScrollComboBox()
                combo.addItems(cat_names)
                combo.setCurrentText(cat_name)
                combo.currentTextChanged.connect(
                    lambda new_cat, p_id=str(p["id"]): self._on_category_combo_changed(p_id, new_cat)
                )
                self.table.setCellWidget(row, 1, combo)

                # 2: 상품명(한국어)
                name_ko = f"[품절] {p.get('name', '')}" if is_sold_out else str(p.get("name", ""))
                self.table.setItem(row, 2, QTableWidgetItem(name_ko))

                # 3: 가격(원화)
                self.table.setItem(row, 3, QTableWidgetItem(str(p.get("price", 0))))

                # 4: 수련생 할인액 [신규]
                self.table.setItem(row, 4, QTableWidgetItem(str(p.get("discount_student", 0))))

                # 5: 아카데미 할인액 [신규]
                self.table.setItem(row, 5, QTableWidgetItem(str(p.get("discount_academy", 0))))

                # 6: 상품명(일본어)
                self.table.setItem(row, 6, QTableWidgetItem(str(p.get("name_ja", ""))))

                # 7: 가격(엔화)
                self.table.setItem(row, 7, QTableWidgetItem(str(p.get("price_jpy", 0))))

                if is_sold_out:
                    for col in range(8):
                        item = self.table.item(row, col)
                        if item:
                            item.setForeground(Qt.GlobalColor.red)

        self.table.blockSignals(False)

    # ==========================================
    # 이벤트 핸들러
    # ==========================================
    def _on_category_combo_changed(self, product_id: str, new_cat_name: str):
        """테이블 셀 내 카테고리 ComboBox 변경 이벤트"""
        self.model.update_product_info(product_id, new_cat_name=new_cat_name)
        self.refresh_all_data()

    def _on_table_item_changed(self, item: QTableWidgetItem):
        row = item.row()
        col = item.column()

        p_id_item = self.table.item(row, 0)
        if not p_id_item: return
        p_id = p_id_item.text()
        new_val = item.text().strip()

        if col == 2:  # 한국어 상품명
            if not new_val:
                QMessageBox.warning(self, "경고", "상품명은 비어 둘 수 없습니다.")
                self.load_product_table()
                return
            self.model.update_product_info(p_id, new_name=new_val)

        elif col == 3:  # 원화 가격
            if not new_val.isdigit():
                QMessageBox.warning(self, "경고", "가격은 숫자만 입력해 주세요.")
                self.load_product_table()
                return
            self.model.update_product_info(p_id, new_price=int(new_val))

        elif col == 4:  # 수련생 할인액 수정 [신규]
            if not new_val.isdigit():
                QMessageBox.warning(self, "경고", "할인 금액은 숫자만 입력해 주세요.")
                self.load_product_table()
                return
            self.model.update_product_info(p_id, new_disc_student=int(new_val))

        elif col == 5:  # 아카데미 할인액 수정 [신규]
            if not new_val.isdigit():
                QMessageBox.warning(self, "경고", "할인 금액은 숫자만 입력해 주세요.")
                self.load_product_table()
                return
            self.model.update_product_info(p_id, new_disc_academy=int(new_val))

        elif col == 6:  # 일본어 상품명
            self.model.update_product_info(p_id, new_name_ja=new_val)

        elif col == 7:  # 엔화 가격
            if not new_val.isdigit():
                QMessageBox.warning(self, "경고", "엔화 가격은 숫자만 입력해 주세요.")
                self.load_product_table()
                return
            self.model.update_product_info(p_id, new_price_jpy=int(new_val))

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

    def _on_add_product(self):
            cat_id = self.cb_category.currentData()
            name_ko = self.le_name_ko.text().strip()
            price_ko = self.sb_price_ko.value()
            disc_student = self.sb_disc_student.value()
            disc_academy = self.sb_disc_academy.value()
            name_ja = self.le_name_ja.text().strip()
            price_ja = self.sb_price_ja.value()
    
            if not cat_id or not name_ko:
                QMessageBox.warning(self, "경고", "카테고리와 한국어 상품명은 필수 입력 항목입니다.")
                return
    
            if self.model.add_product(cat_id, name_ko, price_ko, name_ja, price_ja, "", disc_student, disc_academy):
                QMessageBox.information(self, "완료", "신규 상품이 등록되었습니다.")
                self.le_name_ko.clear()
                self.le_name_ja.clear()
                self.sb_disc_student.setValue(0)
                self.sb_disc_academy.setValue(0)
                self.refresh_all_data()
            else:
                QMessageBox.warning(self, "오류", "상품 등록 실패")

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
            reply = QMessageBox.question(
                self, "삭제 확인", "정말 삭제하시겠습니까?", 
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.model.remove_product(p_id)
                self.load_product_table()

    def _on_select_image(self):
        """이미지 파일 선택 핸들러"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "상품 이미지 선택", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.le_image_path.setText(file_path)

    def _on_table_item_double_clicked(self, item: QTableWidgetItem):
        """테이블 셀 더블클릭 이벤트 (0번 ID 열 더블클릭 시 해당 상품 이미지 파일 열기)"""
        if item.column() != 0:  # ID 열이 아닌 경우 스킵
            return

        product_id = item.text().strip()
        if not product_id:
            return

        # 1. 모델에서 ID에 해당하는 상품 데이터 조회
        target_product = None
        for cat in self.model.categories:
            for p in cat.get("products", []):
                if str(p.get("id")) == str(product_id):
                    target_product = p
                    break
            if target_product:
                break

        if not target_product:
            QMessageBox.warning(self, "경고", "해당 상품 정보를 찾을 수 없습니다.")
            return

        # 2. 최상위 프로젝트 루트 기준으로 보정된 절대 경로 추출 (Repository에서 생성한 image_abs_path 활용)
        import os
        from PySide6.QtCore import QUrl
        from PySide6.QtGui import QDesktopServices
        from my_package.utils.path_utils import get_project_root
        from my_package.utils.image_manager import ImageManager

        abs_image_path = target_product.get("image_abs_path", "")

        # 만약 image_abs_path가 없을 경우 최상위 project_root 기준으로 경로 재조합
        if not abs_image_path:
            rel_image_path = target_product.get("image", "")
            abs_image_path = ImageManager.get_absolute_image_path(get_project_root(), rel_image_path)
            parent_dir = os.path.dirname(os.path.abspath(abs_image_path))
            print(f"[Debug] 상품 ID {product_id} 이미지 절대 경로: {abs_image_path}, 상위 폴더: {parent_dir}")
        # 3. 파일 존재 여부 검증 및 이미지 파일 실행
        if os.path.exists(abs_image_path):
            try:
                # Cross-Platform 기본 이미지 뷰어 열기
                #url = QUrl.fromLocalFile(abs_image_path)
                #QDesktopServices.openUrl(url)
                parent_dir = os.path.dirname(os.path.abspath(abs_image_path))
                url = QUrl.fromLocalFile(parent_dir)
                QDesktopServices.openUrl(url)
                #print(f"[Debug] 상품 ID {product_id} 이미지 절대 경로: {abs_image_path}, 상위 폴더: {parent_dir}")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일을 열 수 없습니다:\n{e}")
        else:
            QMessageBox.warning(
                self, 
                "파일 없음", 
                f"등록된 파일을 찾을 수 없습니다.\n경로: {abs_image_path}\n이미지를 새로 생성합니다."
            )
            ImageManager.ensure_default_sample_image(abs_image_path, target_product.get("name", ""))