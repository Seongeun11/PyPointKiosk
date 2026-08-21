# my_package/view/admin_menu_dialog_view.py

import os
from PySide6.QtWidgets import (
    QMessageBox, QTableWidget, QTableWidgetItem,QLineEdit,
    QHeaderView, QInputDialog, QFileDialog, QComboBox
)
from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtGui import QDesktopServices

from my_package.utils.base_scaled_manager import BaseScaledDialog
from my_package.utils.path_utils import get_project_root
from my_package.utils.image_manager import ImageManager

# 디자이너에서 생성된 UI 클래스 임포트
from my_package.ui.ui_order_menu_admin_dialog import Ui_Dialog


class NoScrollComboBox(QComboBox):
    """마우스 휠 이벤트를 무시하여 테이블 스크롤 시 의도치 않은 항목 변경을 방지하는 ComboBox"""
    def wheelEvent(self, event):
        event.ignore()


class AdminMenuDialogView(BaseScaledDialog):
    export_excel_requested = Signal(str)

    def __init__(self, model, parent=None):
        super().__init__(parent)
        self.model = model
        
        # 디자이너 UI 연동
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setWindowTitle("관리자 메뉴 - 상품 및 카테고리 관리")
        
        self.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.CustomizeWindowHint | 
            Qt.WindowType.WindowTitleHint | 
            Qt.WindowType.WindowMinimizeButtonHint | 
            Qt.WindowType.WindowMaximizeButtonHint | 
            Qt.WindowType.WindowCloseButtonHint
        )

        self._setup_ui_settings()
        self._bind_signals()
        self.refresh_all_data()

    def _setup_ui_settings(self):
        """UI 기본 환경 및 테이블 컬럼 설정"""
        # 테이블 컬럼 정의 (상품명(일본어) 삭제 / 엔화 할인액 추가)
        self.ui.tbw_table.setColumnCount(8)
        self.ui.tbw_table.setHorizontalHeaderLabels([
            "ID", "카테고리", "상품명(한국어)", "가격(원화)", 
            "수련생 할인", "아카데미 할인", "가격(엔화)", "엔화 할인액"
        ])
        
        self.ui.tbw_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.ui.tbw_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.ui.tbw_table.setColumnWidth(0, 50)
        self.ui.tbw_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.ui.tbw_table.setEditTriggers(
            QTableWidget.EditTrigger.DoubleClicked | QTableWidget.EditTrigger.EditKeyPressed
        )

        # QSpinBox 범위 세팅
        self.ui.sb_proce_ko.setRange(0, 1000000)
        self.ui.sb_proce_ko.setSingleStep(500)
        self.ui.sb_proce_ko.setValue(3000)

        self.ui.sb_disc_student.setRange(0, 1000000)
        self.ui.sb_disc_student.setSingleStep(100)

        self.ui.sb_disc_academy.setRange(0, 1000000)
        self.ui.sb_disc_academy.setSingleStep(100)

        self.ui.sb_price_ja.setRange(0, 100000)
        self.ui.sb_price_ja.setSingleStep(50)
        self.ui.sb_price_ja.setValue(300)

        self.ui.sb_disc_ja.setRange(0, 100000)
        self.ui.sb_disc_ja.setSingleStep(50)

    def _bind_signals(self):
        """새로운 Designer ID에 맞춘 이벤트 시그널 바인딩"""
        # 상단 기능 버튼
        self.ui.btn_export_excel.clicked.connect(self._on_export_clicked)
        self.ui.btn_toggle_soldout.clicked.connect(self._on_toggle_soldout)
        self.ui.btn_delete.clicked.connect(self._on_delete_product)

        # 테이블 시그널
        self.ui.tbw_table.itemChanged.connect(self._on_table_item_changed)
        self.ui.tbw_table.itemDoubleClicked.connect(self._on_table_item_double_clicked)

        # 카테고리 관리 버튼
        self.ui.btn_add_category.clicked.connect(self._on_add_category)
        self.ui.btn_edit_category.clicked.connect(self._on_edit_category)
        self.ui.btn_move_up.clicked.connect(self._on_move_category_up)
        self.ui.btn_move_down.clicked.connect(self._on_move_category_down)
        self.ui.btn_delete_category.clicked.connect(self._on_delete_category)

        # 하단 상품 관리 버튼
        self.ui.btn_add.clicked.connect(self._on_add_product)
        self.ui.btn_close.clicked.connect(self.accept)

    def refresh_all_data(self):
        self._update_category_comboboxes()
        self.load_product_table()

    def _update_category_comboboxes(self):
        self.ui.cb_category.clear()
        self.ui.cb_delete_category.clear()

        categories = self.model.get_categories()
        for cat in categories:
            self.ui.cb_category.addItem(cat["name"], cat["title"])
            self.ui.cb_delete_category.addItem(cat["name"], cat["title"])

    def load_product_table(self):
        self.ui.tbw_table.blockSignals(True)
        self.ui.tbw_table.setRowCount(0)

        raw_categories = self.model.categories
        cat_names = [cat.get("name") for cat in raw_categories]

        for cat in raw_categories:
            cat_name = cat.get("name")
            for p in cat.get("products", []):
                row = self.ui.tbw_table.rowCount()
                self.ui.tbw_table.insertRow(row)
                is_sold_out = p.get("is_sold_out", False)

                # 0: ID
                id_item = QTableWidgetItem(str(p.get("id")))
                id_item.setFlags(id_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.ui.tbw_table.setItem(row, 0, id_item)

                # 1: 카테고리 콤보박스
                combo = NoScrollComboBox()
                combo.addItems(cat_names)
                combo.setCurrentText(cat_name)
                combo.currentTextChanged.connect(
                    lambda new_cat, p_id=str(p["id"]): self._on_category_combo_changed(p_id, new_cat)
                )
                self.ui.tbw_table.setCellWidget(row, 1, combo)

                # 2: 상품명(한국어)
                name_ko = f"[품절] {p.get('name', '')}" if is_sold_out else str(p.get("name", ""))
                self.ui.tbw_table.setItem(row, 2, QTableWidgetItem(name_ko))

                # 3: 가격(원화)
                self.ui.tbw_table.setItem(row, 3, QTableWidgetItem(str(p.get("price", 0))))

                # 4: 수련생 할인액
                self.ui.tbw_table.setItem(row, 4, QTableWidgetItem(str(p.get("discount_student", 0))))

                # 5: 아카데미 할인액
                self.ui.tbw_table.setItem(row, 5, QTableWidgetItem(str(p.get("discount_academy", 0))))

                # 6: 가격(엔화)
                self.ui.tbw_table.setItem(row, 6, QTableWidgetItem(str(p.get("price_jpy", 0))))

                # 7: 엔화 할인액
                self.ui.tbw_table.setItem(row, 7, QTableWidgetItem(str(p.get("discount_jpy", 0))))

                if is_sold_out:
                    for col in range(8):
                        item = self.ui.tbw_table.item(row, col)
                        if item:
                            item.setForeground(Qt.GlobalColor.red)

        self.ui.tbw_table.blockSignals(False)

    # ==========================================
    # 이벤트 핸들러
    # ==========================================
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

    def _on_category_combo_changed(self, product_id: str, new_cat_name: str):
        self.model.update_product_info(product_id, new_cat_name=new_cat_name)
        self.refresh_all_data()

    def _on_table_item_changed(self, item: QTableWidgetItem):
        row = item.row()
        col = item.column()

        p_id_item = self.ui.tbw_table.item(row, 0)
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

        elif col == 4:  # 수련생 할인액
            if not new_val.isdigit():
                QMessageBox.warning(self, "경고", "할인 금액은 숫자만 입력해 주세요.")
                self.load_product_table()
                return
            self.model.update_product_info(p_id, new_disc_student=int(new_val))

        elif col == 5:  # 아카데미 할인액
            if not new_val.isdigit():
                QMessageBox.warning(self, "경고", "할인 금액은 숫자만 입력해 주세요.")
                self.load_product_table()
                return
            self.model.update_product_info(p_id, new_disc_academy=int(new_val))

        elif col == 6:  # 엔화 가격
            if not new_val.isdigit():
                QMessageBox.warning(self, "경고", "엔화 가격은 숫자만 입력해 주세요.")
                self.load_product_table()
                return
            self.model.update_product_info(p_id, new_price_jpy=int(new_val))

        elif col == 7:  # 엔화 할인액
            if not new_val.isdigit():
                QMessageBox.warning(self, "경고", "엔화 할인 금액은 숫자만 입력해 주세요.")
                self.load_product_table()
                return
            self.model.update_product_info(p_id, new_disc_ja=int(new_val))

        self.load_product_table()

    def _on_add_category(self):
        cat_name = self.ui.le_new_category.text().strip()
        if not cat_name:
            QMessageBox.warning(self, "경고", "추가할 카테고리명을 입력해주세요.")
            return

        if self.model.add_category(cat_name):
            QMessageBox.information(self, "완료", f"'{cat_name}' 카테고리가 추가되었습니다.")
            self.ui.le_new_category.clear()
            self.refresh_all_data()
        else:
            QMessageBox.warning(self, "오류", "카테고리 추가에 실패했습니다.")

    # admin_menu_dialog_view.py 중 _on_add_product 수정 부분
    def _on_add_product(self):
        cat_id = self.ui.cb_category.currentData()
        name_ko = self.ui.txt_name_ko.text().strip()
        price_ko = self.ui.sb_proce_ko.value()
        disc_student = self.ui.sb_disc_student.value()
        disc_academy = self.ui.sb_disc_academy.value()
        price_ja = self.ui.sb_price_ja.value()
        disc_ja = self.ui.sb_disc_ja.value()

        if not cat_id or not name_ko:
            QMessageBox.warning(self, "경고", "카테고리와 한국어 상품명은 필수 입력 항목입니다.")
            return

        # 모델 매개변수 규격에 맞춰 정확하게 전달 (discount_jpy 추가)
        if self.model.add_product(
            category_id=cat_id, 
            prod_name=name_ko, 
            price=price_ko, 
            price_jpy=price_ja, 
            discount_student=disc_student, 
            discount_academy=disc_academy, 
            discount_jpy=disc_ja
        ):
            QMessageBox.information(self, "완료", "신규 상품이 등록되었습니다.")
            self.ui.txt_name_ko.clear()
            self.ui.sb_disc_student.setValue(0)
            self.ui.sb_disc_academy.setValue(0)
            self.ui.sb_disc_ja.setValue(0)
            self.refresh_all_data()
        else:
            QMessageBox.warning(self, "오류", "상품 등록 실패")

    def _on_delete_category(self):
        cat_id = self.ui.cb_delete_category.currentData()
        cat_name = self.ui.cb_delete_category.currentText()

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

    def _on_edit_category(self):
        cat_id = self.ui.cb_delete_category.currentData()
        current_name = self.ui.cb_delete_category.currentText()

        if not cat_id:
            QMessageBox.warning(self, "경고", "수정할 카테고리를 선택해주세요.")
            return

        new_name, ok1 = QInputDialog.getText(
            self, "카테고리명 수정", "새 카테고리명(한국어)을 입력하세요:", QLineEdit.EchoMode.Normal, current_name
        )
        if not ok1 or not new_name.strip():
            return

        target_cat = next((c for c in self.model.categories if str(c.get("title")) == str(cat_id)), {})
        current_name_ja = target_cat.get("name_ja", new_name)

        #ew_name_ja, ok2 = QInputDialog.getText(
        #    self, "카테고리명 수정 (일본어)", "새 카테고리명(일본어)을 입력하세요:", QLineEdit.EchoMode.Normal, current_name_ja
        #)
        #if not ok2:
        #    new_name_ja = current_name_ja

        #if self.model.update_category(cat_id, new_name, new_name_ja):
        if self.model.update_category(cat_id, new_name):
            QMessageBox.information(self, "완료", f"카테고리명이 '{new_name}'(으)로 변경되었습니다.")
            self.refresh_all_data()
            idx = self.ui.cb_delete_category.findData(cat_id)
            if idx != -1:
                self.ui.cb_delete_category.setCurrentIndex(idx)
        else:
            QMessageBox.warning(self, "오류", "카테고리명 변경에 실패했습니다.")

    def _on_move_category_up(self):
        cat_id = self.ui.cb_delete_category.currentData()
        if not cat_id:
            return
        if self.model.move_category_up(cat_id):
            self.refresh_all_data()
            idx = self.ui.cb_delete_category.findData(cat_id)
            if idx != -1:
                self.ui.cb_delete_category.setCurrentIndex(idx)

    def _on_move_category_down(self):
        cat_id = self.ui.cb_delete_category.currentData()
        if not cat_id:
            return
        if self.model.move_category_down(cat_id):
            self.refresh_all_data()
            idx = self.ui.cb_delete_category.findData(cat_id)
            if idx != -1:
                self.ui.cb_delete_category.setCurrentIndex(idx)

    def _get_selected_product_id(self):
        selected_rows = self.ui.tbw_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "경고", "상품을 선택해주세요.")
            return None

        row = selected_rows[0].row()
        item = self.ui.tbw_table.item(row, 0)
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

    def _on_table_item_double_clicked(self, item: QTableWidgetItem):
        if item.column() != 0:
            return

        product_id = item.text().strip()
        if not product_id:
            return

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

        abs_image_path = target_product.get("image_abs_path", "")
        if not abs_image_path:
            rel_image_path = target_product.get("image", "")
            abs_image_path = ImageManager.get_absolute_image_path(get_project_root(), rel_image_path)

        if os.path.exists(abs_image_path):
            try:
                parent_dir = os.path.dirname(os.path.abspath(abs_image_path))
                url = QUrl.fromLocalFile(parent_dir)
                QDesktopServices.openUrl(url)
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일을 열 수 없습니다:\n{e}")
        else:
            QMessageBox.warning(
                self, 
                "파일 없음", 
                f"등록된 파일을 찾을 수 없습니다.\n경로: {abs_image_path}\n이미지를 새로 생성합니다."
            )
            ImageManager.ensure_default_sample_image(abs_image_path, target_product.get("name", ""))