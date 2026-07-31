import os
from PySide6.QtWidgets import (
    QWidget, QSizePolicy, QPushButton, QToolButton, QLayout, QSpacerItem,
    QScrollArea, QHBoxLayout, QGridLayout
)
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QResizeEvent, QShowEvent, QFont
from PySide6.QtCore import QSize, Qt, Signal, QTimer

from ui.ui_order_menu import Ui_Form


class OrderMenuView(QWidget):
    category_clicked_signal = Signal(int)
    product_clicked_signal = Signal(dict)
    pay_clicked_signal = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # 4열 고정 규격
        self.GRID_COLS = 4
        
        # 2줄 카테고리용 설정 (2행 x 4열 = 한 화면에 최대 8개)
        self.CAT_ROWS = 2
        self.CAT_COLS = 4
        self.VISIBLE_CAT_COUNT = self.CAT_ROWS * self.CAT_COLS  # 8개

        # 메인 Vertical Layout 반응형 레이아웃 Stretch 비율 설정
        # (타이틀 : 카테고리 : 메뉴판 : 장바구니/결제 = 1 : 2 : 12 : 5)
        self.ui.verticalLayout.setStretch(0, 1)
        self.ui.verticalLayout.setStretch(1, 2)
        self.ui.verticalLayout.setStretch(2, 12)
        self.ui.verticalLayout.setStretch(3, 5)

        # 하단 결제 버튼의 Designer 고정 최소 높이 제한 해제
        if hasattr(self.ui, "pushButton"):
            self.ui.pushButton.setMinimumSize(QSize(0, 0))
            self.ui.pushButton.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

        self._setup_scroll_areas()
        self._connect_static_signals()

    def _setup_scroll_areas(self):
        """Designer 레이아웃을 대체하여 스크롤 영역 및 이동 버튼 구축"""
        # ------------------------------------------------------------------
        # 1. 카테고리 영역 (2줄 QGridLayout + 좌/우 스크롤)
        # ------------------------------------------------------------------
        self.category_wrapper_layout = QHBoxLayout()
        self.category_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        self.category_wrapper_layout.setSpacing(4)

        self.btn_cat_prev = QPushButton("<")
        self.btn_cat_prev.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.btn_cat_prev.setFixedWidth(36)
        self.btn_cat_prev.clicked.connect(self._scroll_category_left)

        self.btn_cat_next = QPushButton(">")
        self.btn_cat_next.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        self.btn_cat_next.setFixedWidth(36)
        self.btn_cat_next.clicked.connect(self._scroll_category_right)

        self.category_scroll = QScrollArea(self)
        self.category_scroll.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.category_scroll.setWidgetResizable(True)
        self.category_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.category_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.category_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.category_container = QWidget()
        
        # 2줄 배치용 QGridLayout
        self.category_layout = QGridLayout(self.category_container)
        self.category_layout.setContentsMargins(0, 0, 0, 0)
        self.category_layout.setHorizontalSpacing(8)
        self.category_layout.setVerticalSpacing(6)
        
        self.category_scroll.setWidget(self.category_container)
        self.category_scroll.horizontalScrollBar().valueChanged.connect(self._update_category_nav_buttons)

        self.category_wrapper_layout.addWidget(self.btn_cat_prev)
        self.category_wrapper_layout.addWidget(self.category_scroll, 1)
        self.category_wrapper_layout.addWidget(self.btn_cat_next)

        self.ui.horizontalLayout.addLayout(self.category_wrapper_layout)

        # ------------------------------------------------------------------
        # 2. 메뉴 4열 세로 스크롤 영역
        # ------------------------------------------------------------------
        self.menu_scroll = QScrollArea(self)
        self.menu_scroll.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.menu_scroll.setWidgetResizable(True)
        self.menu_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.menu_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.menu_container = QWidget()
        self.menu_grid_layout = QGridLayout(self.menu_container)
        self.menu_grid_layout.setSpacing(10)
        self.menu_scroll.setWidget(self.menu_container)

        self.ui.gridLayout.addWidget(self.menu_scroll)

    def _clear_layout(self, layout: QLayout | None):
        """레이아웃 내의 모든 위젯 및 스페이서 삭제"""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                if item is not None:
                    widget = item.widget()
                    child_layout = item.layout()

                    if widget is not None:
                        widget.deleteLater()
                    elif child_layout is not None:
                        self._clear_layout(child_layout)

    def _connect_static_signals(self):
        if hasattr(self.ui, "pushButton"):
            self.ui.pushButton.clicked.connect(
                lambda: self.pay_clicked_signal.emit()
            )

    def _get_placeholder_icon(self) -> QIcon:
        pixmap = QPixmap(120, 120)
        pixmap.fill(QColor("#E0E0E0"))
        painter = QPainter(pixmap)
        painter.setPen(QColor("#888888"))
        painter.drawText(
            pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "No Image"
        )
        painter.end()
        return QIcon(pixmap)

    # ------------------------------------------------------------------
    # Category Scroll Logic (버튼 제어)
    # ------------------------------------------------------------------
    def _get_category_step(self) -> int:
        """한 열(Column) 스크롤 거리 계산"""
        if self.category_layout.count() > 0:
            first_item = self.category_layout.itemAt(0)
            if first_item:
                first_widget = first_item.widget()
                if first_widget:
                    return first_widget.width() + self.category_layout.horizontalSpacing()
        return 120

    def _scroll_category_left(self):
        """< 버튼 클릭 시 왼쪽으로 1열 이동"""
        bar = self.category_scroll.horizontalScrollBar()
        bar.setValue(bar.value() - self._get_category_step())

    def _scroll_category_right(self):
        """> 버튼 클릭 시 오른쪽으로 1열 이동"""
        bar = self.category_scroll.horizontalScrollBar()
        bar.setValue(bar.value() + self._get_category_step())

    def _update_category_nav_buttons(self):
        """스크롤 위치에 따른 이동 버튼 활성화/비활성화"""
        bar = self.category_scroll.horizontalScrollBar()
        self.btn_cat_prev.setEnabled(bar.value() > bar.minimum())
        self.btn_cat_next.setEnabled(bar.value() < bar.maximum())

    def _update_ui_scaling(self):
        """창 크기에 비례하여 아이콘, 상품 버튼 높이 및 UI 요소별 폰트 크기 자동 계산"""
        w = self.width()
        h = self.height()

        if w <= 100 or h <= 100:
            return

        # 기준 해상도 비례 폰트 계산 (최소/최대 범위 제한)
        base_scale = min(w / 640.0, h / 720.0)
        title_font_size = max(14, min(int(18 * base_scale), 32))
        cat_font_size = max(10, min(int(13 * base_scale), 20))
        prod_font_size = max(11, min(int(14 * base_scale), 24))
        pay_font_size = max(16, min(int(22 * base_scale), 40))

        # 1. 상단 타이틀 라벨 폰트 반영
        if hasattr(self.ui, "label"):
            font = self.ui.label.font()
            font.setPointSize(title_font_size)
            self.ui.label.setFont(font)

        # 2. 카테고리 버튼 폰트 반영
        for i in range(self.category_layout.count()):
            item = self.category_layout.itemAt(i)
            if item is None:
                continue
            btn = item.widget()
            if btn is None:
                continue
            font = btn.font()
            font.setPointSize(cat_font_size)
            btn.setFont(font)

        # 3. 메뉴 상품 버튼 (높이, 아이콘 및 폰트 반영)
        viewport_height = self.menu_scroll.viewport().height()
        button_height = max(180, int((viewport_height - 20) / 2)) if viewport_height > 100 else 200

        for i in range(self.menu_grid_layout.count()):
            layout_item = self.menu_grid_layout.itemAt(i)
            if layout_item is not None:
                widget = layout_item.widget()
                if isinstance(widget, QToolButton):
                    widget.setFixedHeight(button_height)
                    btn_w = widget.width()
                    btn_h = widget.height()

                    if btn_w > 20 and btn_h > 20:
                        icon_dim = max(50, min(int(min(btn_w, btn_h) * 0.52), 300))
                        widget.setIconSize(QSize(icon_dim, icon_dim))

                    font = widget.font()
                    font.setPointSize(prod_font_size)
                    widget.setFont(font)

        # 4. 결제 버튼 폰트 반영
        if hasattr(self.ui, "pushButton"):
            font = self.ui.pushButton.font()
            font.setPointSize(pay_font_size)
            self.ui.pushButton.setFont(font)

        # 내비게이션 버튼 활성화 상태 최신화
        self._update_category_nav_buttons()

    # ------------------------------------------------------------------
    # Render Methods
    # ------------------------------------------------------------------
    def render_categories(self, categories: list, current_idx: int):
        self._clear_layout(self.category_layout)

        cat_count = len(categories)

        has_more_than_visible = cat_count > self.VISIBLE_CAT_COUNT
        self.btn_cat_prev.setVisible(has_more_than_visible)
        self.btn_cat_next.setVisible(has_more_than_visible)

        for idx, category in enumerate(categories):
            btn = QPushButton(category["name"], self)
            btn.setFixedHeight(38)

            if not has_more_than_visible:
                btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            else:
                btn.setMinimumWidth(120)

            is_selected = idx == current_idx
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {"#FF5500" if is_selected else "#E0E0E0"};
                    color: {"#FFFFFF" if is_selected else "#000000"};
                    font-size: 13px;
                    font-weight: bold;
                    border-radius: 6px;
                }}
            """)

            btn.clicked.connect(
                lambda checked=False, c_idx=idx: self.category_clicked_signal.emit(
                    c_idx
                )
            )

            row = idx % self.CAT_ROWS
            col = idx // self.CAT_ROWS
            self.category_layout.addWidget(btn, row, col)

        QTimer.singleShot(0, self._update_ui_scaling)

    def render_products(self, products: list):
        self._clear_layout(self.menu_grid_layout)

        for col in range(self.GRID_COLS):
            self.menu_grid_layout.setColumnStretch(col, 1)

        viewport_height = self.menu_scroll.viewport().height()
        button_height = max(180, int((viewport_height - 20) / 2)) if viewport_height > 100 else 200

        total_items = len(products)
        display_items = max(total_items, 8)

        for idx in range(display_items):
            row = idx // self.GRID_COLS
            col = idx % self.GRID_COLS

            if idx < total_items:
                btn = self._create_product_button(products[idx], button_height)
                self.menu_grid_layout.addWidget(btn, row, col)
            else:
                dummy_spacer = QSpacerItem(
                    1, button_height, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
                )
                self.menu_grid_layout.addItem(dummy_spacer, row, col)

        self.menu_scroll.verticalScrollBar().setValue(0)
        QTimer.singleShot(0, self._update_ui_scaling)

    def _create_product_button(self, product_data: dict, height: int) -> QToolButton:
        btn = QToolButton()
        btn.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        btn.setFixedHeight(height)
        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        formatted_price = f"{product_data['price']:,}원"
        btn.setText(f"{product_data['name']}\n{formatted_price}")

        img_path = product_data.get("image_abs_path", "")
        if img_path and os.path.exists(img_path):
            btn.setIcon(QIcon(img_path))
        else:
            btn.setIcon(self._get_placeholder_icon())

        btn.setStyleSheet("""
            QToolButton {
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                font-weight: bold;
                color: #333333;
                background-color: #FFFFFF;
                padding: 6px;
            }
            QToolButton:hover {
                border: 2px solid #FF5500;
                background-color: #FFF5F0;
            }
            QToolButton:pressed {
                background-color: #E0E0E0;
            }
        """)

        btn.clicked.connect(
            lambda checked=False, p=product_data: self.product_clicked_signal.emit(
                p
            )
        )
        return btn

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        QTimer.singleShot(0, self._update_ui_scaling)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        # 레이아웃 리사이징 완료 후 다음 이벤트 루프 시점에 즉각 UI 비율 반영
        QTimer.singleShot(0, self._update_ui_scaling)