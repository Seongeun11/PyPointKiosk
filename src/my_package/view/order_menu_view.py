#src\my_package\view\order_menu_view.py
from PySide6.QtWidgets import (
    QWidget, QSizePolicy, QPushButton, QToolButton, QLayout, QSpacerItem,
    QScrollArea, QHBoxLayout, QGridLayout, QListWidgetItem
)
from PySide6.QtGui import QIcon, QResizeEvent, QShowEvent, QMouseEvent
from PySide6.QtCore import QSize, Qt, Signal, QTimer

# 자동 생성된 UI 클래스 import
from ui.ui_order_menu import Ui_Form 
from custom_widget.cart_item_widget import CartItemWidget #장바구니 관리 클래스
from utils.image_manager import ImageManager #이미지 관리 유틸리티 클래스

# 타이틀 버튼의 더블클릭을 감지하기 위한 Custom PushButton
class TitleButton(QPushButton):
    double_clicked = Signal()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit()
        super().mouseDoubleClickEvent(event)

class OrderMenuView(QWidget):
    category_clicked_signal = Signal(int)
    product_clicked_signal = Signal(dict)
    pay_clicked_signal = Signal()
    title_double_clicked_signal = Signal()  # [추가] 타이틀 더블클릭 시그널
    clear_cart_clicked_signal = Signal()  # [추가] 장바구니 전체 삭제 시그널
    # [수량 조절 및 삭제 시그널 추가]
    change_qty_signal = Signal(str, int)  # (product_id, delta)
    remove_item_signal = Signal(str)      # (product_id)

    orderview_on_go_back_signal = Signal(str) # 뒤로가기

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

       
        #self.ui.lst_my_order_details.setModel(self.cart_list_model)
        
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        # 4열 고정 규격
        self.GRID_COLS = 4
        self.GRID_ROWS = 3
        # 1페이지당 기본 아이템 개수 (열 x 행)
        self.GRID_PAGE_SIZE = self.GRID_COLS * self.GRID_ROWS
        
        # 행 수에 따른 버튼 적정 높이 계산 (예: 2행=300px, 3행=200px 등)
        # 키오스크 해상도나 레이아웃에 맞춰 적절한 기본 높이 로직을 적용합니다.
        self.BUTTON_HEIGHT = 280
        self.PRODUCT_BTN_HEIGHT = max(self.BUTTON_HEIGHT, int(600 / self.GRID_ROWS))

        #CATEGORY 관련 상수
        self.CAT_COUNT = 6  # 2행 카테고리 버튼 수 기준
        self.CAT_ROWS = 2
        self.CAT_COLS = 4
        self.VISIBLE_CAT_COUNT = self.CAT_ROWS * self.CAT_COLS  # 한 화면 최대 8개

        

        # 메인 Vertical Layout 반응형 레이아웃 Stretch 비율 설정
        self.ui.verticalLayout.setStretch(0, 1)
        self.ui.verticalLayout.setStretch(1, 2)
        self.ui.verticalLayout.setStretch(2, 12)
        self.ui.verticalLayout.setStretch(3, 5)

        # 하단 결제 버튼의 Designer 고정 최소 높이 제한 해제 (반응형 확장용)
        if hasattr(self.ui, "btn_payment"):
            self.ui.btn_payment.setMinimumSize(QSize(0, 0))
            self.ui.btn_payment.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

        self._setup_scroll_areas()
        self._connect_static_signals()

    def _setup_scroll_areas(self):
        """Designer 레이아웃 내 스크롤 영역 및 동적 버튼 구축"""
        # 1. 카테고리 스크롤 영역
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

        # 2. 메뉴 4열 세로 스크롤 영역
        self.menu_scroll = QScrollArea(self)
        self.menu_scroll.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.menu_scroll.setWidgetResizable(True)
        self.menu_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        # [수정] 스크롤바 유무에 따른 너비/높이 변동을 막기 위해 항상 켜둠
        self.menu_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        
        self.menu_scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.menu_container = QWidget()
        self.menu_grid_layout = QGridLayout(self.menu_container)
        self.menu_grid_layout.setSpacing(10)
        self.menu_scroll.setWidget(self.menu_container)

        self.ui.gridLayout.addWidget(self.menu_scroll)

    def _clear_layout(self, layout: QLayout | None):
        """레이아웃 내부 위젯 및 스페이서 삭제"""
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
        """수정된 UI 객체명 기반 시그널 바인딩"""
        if hasattr(self.ui, "btn_payment"):
            self.ui.btn_payment.clicked.connect(
                lambda: self.pay_clicked_signal.emit()
            )
        if hasattr(self.ui, "btn_all_delete"):
            self.ui.btn_all_delete.clicked.connect(
                lambda: self.clear_cart_clicked_signal.emit()
            )
        if hasattr(self.ui, "btn_title"):
            # 기존 btn_title의 mouseDoubleClickEvent 재정의
            self.ui.btn_title.mouseDoubleClickEvent = self._on_title_double_clicked
            #self.ui.btn_title.clicked.connect(lambda: self.title_double_clicked_signal.emit())

        if hasattr(self.ui, "btn_back"):
            
           self.ui.btn_back.clicked.connect(self.handle_go_back_clicked)
            

    def _on_title_double_clicked(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.title_double_clicked_signal.emit()

    def _get_placeholder_icon(self) -> QIcon:
        """ImageManager 위임"""
        return ImageManager.create_placeholder_icon(120, 120, "No Image")

    def _get_category_step(self) -> int:
        if self.category_layout.count() > 0:
            first_item = self.category_layout.itemAt(0)
            widget = first_item.widget() if first_item else None
            if widget is not None:
                return widget.width() + self.category_layout.spacing()
        return 120

    def _scroll_category_left(self):
        bar = self.category_scroll.horizontalScrollBar()
        bar.setValue(bar.value() - self._get_category_step())

    def _scroll_category_right(self):
        bar = self.category_scroll.horizontalScrollBar()
        bar.setValue(bar.value() + self._get_category_step())

    def _update_category_nav_buttons(self):
        bar = self.category_scroll.horizontalScrollBar()
        self.btn_cat_prev.setEnabled(bar.value() > bar.minimum())
        self.btn_cat_next.setEnabled(bar.value() < bar.maximum())

    # ---------------------------------------------------------
    # [수정] _update_ui_scaling : 더미 버튼은 스케일링 계산에서 제외
    # ---------------------------------------------------------
    def _update_ui_scaling(self):
        w, h = self.width(), self.height()
        if w <= 100 or h <= 100:
            return

        base_scale = min(w / 640.0, h / 720.0)
        title_font_size = max(14, min(int(18 * base_scale), 32))
        cat_font_size = max(10, min(int(13 * base_scale), 20))
        prod_font_size = max(11, min(int(14 * base_scale), 24))
        pay_font_size = max(16, min(int(22 * base_scale), 40))

        # 1. 타이틀 라벨 (lbl_title)
        if hasattr(self.ui, "lbl_title"):
            font = self.ui.btn_title.font()
            font.setPointSize(title_font_size)
            self.ui.btn_title.setFont(font)

        # 2. 카테고리 버튼
        for i in range(self.category_layout.count()):
            item = self.category_layout.itemAt(i)
            widget = item.widget() if item else None
            if widget:
                font = widget.font()
                font.setPointSize(cat_font_size)
                widget.setFont(font)

        # 3. 메뉴 상품 버튼 (더미 버튼 제외 조건 추가)
        for i in range(self.menu_grid_layout.count()):
            layout_item = self.menu_grid_layout.itemAt(i)
            widget = layout_item.widget() if layout_item else None
            
            # [핵심] 실제 활성화된 QToolButton만 스케일링을 수행하여 UI 왜곡 방지
            if isinstance(widget, QToolButton) and widget.isEnabled():
                btn_w, btn_h = widget.width(), widget.height()

                if btn_w > 20 and btn_h > 20:
                    icon_dim = max(50, min(int(min(btn_w, btn_h) * 0.52), 300))
                    widget.setIconSize(QSize(icon_dim, icon_dim))

                font = widget.font()
                font.setPointSize(prod_font_size)
                widget.setFont(font)
        # [추가] 상품 개수 표시 LineEdit (le_product) 스케일링 적용
        if hasattr(self.ui, "le_product"):
            font = self.ui.le_select_products.font()
            font.setPointSize(prod_font_size)
            self.ui.le_select_products.setFont(font)
            self.ui.le_select_products.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
        # 4. 결제 버튼 (btn_payment)
        if hasattr(self.ui, "btn_payment"):
            font = self.ui.btn_payment.font()
            font.setPointSize(pay_font_size)
            self.ui.btn_payment.setFont(font)
            
    # ---------------------------------------------------------
    # [동적 변경 함수] 실행 중에도 행 수를 변경할 수 있는 Setter 추가
    # ---------------------------------------------------------
    def set_grid_rows(self, rows: int):
        """메뉴 그리드의 행 수를 동적으로 변경"""
        if rows > 0:
            self.GRID_ROWS = rows
            self.GRID_PAGE_SIZE = self.GRID_COLS * self.GRID_ROWS
            self.PRODUCT_BTN_HEIGHT = max(150, int(600 / self.GRID_ROWS))
            
    def render_categories(self, categories: list, current_idx: int):
        self._clear_layout(self.category_layout)
        cat_count = len(categories)

        if cat_count <= self.CAT_COUNT:
            current_rows = 1
            btn_height = 45
            self.ui.verticalLayout.setStretch(1, 1)
        else:
            current_rows = self.CAT_ROWS
            btn_height = 38
            self.ui.verticalLayout.setStretch(1, 2)

        has_more_than_visible = cat_count > self.VISIBLE_CAT_COUNT
        self.btn_cat_prev.setVisible(has_more_than_visible)
        self.btn_cat_next.setVisible(has_more_than_visible)

        for idx, category in enumerate(categories):
            btn = QPushButton(category["name"], self)
            btn.setFixedHeight(btn_height)

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
                lambda checked=False, c_idx=idx: self.category_clicked_signal.emit(c_idx)
            )

            row = idx % current_rows
            col = idx // current_rows
            self.category_layout.addWidget(btn, row, col)

        QTimer.singleShot(0, self._update_ui_scaling)

    # ---------------------------------------------------------
    # [수정] render_products : 빈 슬롯을 투명 QToolButton으로 채워 완벽한 그리드 유지를 보장
    # ---------------------------------------------------------
    def render_products(self, products: list):
        self._clear_layout(self.menu_grid_layout)

        # 1. 열(Column) 비율을 1:1:1:1로 동일하게 유지
        for col in range(self.GRID_COLS):
            self.menu_grid_layout.setColumnStretch(col, 1)

        total_items = len(products)
        # 아이템 수가 부족해도 최소 1페이지 분량(GRID_PAGE_SIZE)을 보장
        display_items = max(total_items, self.GRID_PAGE_SIZE)

        # 2. 행(Row) 개수 계산 및 Stretch 초기화
        total_rows = (display_items + self.GRID_COLS - 1) // self.GRID_COLS
        for r in range(total_rows):
            self.menu_grid_layout.setRowStretch(r, 0) # 세로로 불필요하게 늘어나는 것 방지

        # 3. 실제 상품 및 더미 위젯 배치
        for idx in range(display_items):
            row = idx // self.GRID_COLS
            col = idx % self.GRID_COLS

            if idx < total_items:
                btn = self._create_product_button(products[idx], self.PRODUCT_BTN_HEIGHT)
                self.menu_grid_layout.addWidget(btn, row, col)
            else:
                # 완벽히 동일한 최소/최대 크기를 갖는 투명 더미 버튼 배치
                dummy_btn = self._create_dummy_button(self.PRODUCT_BTN_HEIGHT)
                self.menu_grid_layout.addWidget(dummy_btn, row, col)

        # 4. 하단 남는 공간을 밀어내서 상단 정렬을 유휴시키는 Vertical Spacer 추가
        v_spacer = QSpacerItem(1, 1, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        self.menu_grid_layout.addItem(v_spacer, total_rows, 0, 1, self.GRID_COLS)

        self.menu_scroll.verticalScrollBar().setValue(0)
        QTimer.singleShot(0, self._update_ui_scaling)


    # ---------------------------------------------------------
    # [신규 추가] 투명 더미 버튼 생성 함수 (그리드 레이아웃 틀 고정용)
    # ---------------------------------------------------------
    def _create_dummy_button(self, height: int) -> QToolButton:
        dummy = QToolButton()
        # Expanding / Fixed 조합 및 높이 고정
        dummy.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        dummy.setFixedHeight(height)
        dummy.setEnabled(False)  # 클릭 이벤트 차단
        
        # 완전 투명 및 테두리 제거 (공간만 정확히 점유)
        dummy.setStyleSheet("""
            QToolButton {
                border: none;
                background-color: transparent;
            }
        """)
        return dummy
    
    def _create_product_button(self, product_data: dict, height: int) -> QToolButton:
        btn = QToolButton()
        btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        btn.setFixedHeight(height)
        btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        is_sold_out = product_data.get("is_sold_out", False)

        name = str(product_data.get('display_name', product_data.get('name', '')))
        if len(name) > 6 and ' ' not in name:
            mid = len(name) // 2
            formatted_name = name[:mid] + '\n' + name[mid:]
        else:
            formatted_name = name

        formatted_price = product_data.get("price_str", f"{product_data.get('computed_price', product_data.get('price', 0)):,}원")
        
        if is_sold_out:
            btn.setText(f"[품절]\n{formatted_name}")
        else:
            btn.setText(f"{formatted_name}\n{formatted_price}")

        # ImageManager를 이용한 아이콘 설정
        img_path = product_data.get("image_abs_path", "")
        btn.setIcon(ImageManager.get_product_icon(img_path))

        btn.setEnabled(not is_sold_out)

        btn.setStyleSheet("""
            QToolButton {
                border: 1px solid #CCCCCC;
                border-radius: 8px;
                font-weight: bold;
                color: #333333;
                background-color: #FFFFFF;
                padding: 4px;
            }
            QToolButton:hover {
                border: 2px solid #FF5500;
                background-color: #FFF5F0;
            }
            QToolButton:pressed {
                background-color: #E0E0E0;
            }
            QToolButton:disabled {
                border: 1px solid #AAAAAA;
                background-color: #EFEFEF;
                color: #888888;
            }
        """)

        btn.clicked.connect(
            lambda checked=False, p=product_data: self.product_clicked_signal.emit(p)
        )
        return btn

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        QTimer.singleShot(0, self._update_ui_scaling)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        QTimer.singleShot(0, self._update_ui_scaling)
    # ---------------------------------------------------------
    # [신규] MVC 바인딩용 : 전체 상품 수량 UI 업데이트
    # ---------------------------------------------------------
    def update_product_count_view(self, total_count: int):
        """장바구니/선택된 전체 상품 개수를 le_select_products에 반영"""
        if hasattr(self.ui, "le_select_products"):
            self.ui.le_select_products.setText(f"{total_count}개")
            # 필요 시 읽기 전용으로 보장
            self.ui.le_select_products.setReadOnly(True)

    # --- QListWidget 기반 장바구니 렌더링 ---
    # OrderMenuView 내 장바구니 렌더링 업데이트 함수 수정
    def update_cart_view(self, cart_items: list, total_price: int, currency: str = "KRW"):
        self.ui.lst_my_order_details.clear()
        # [방어 로직] 호출 시 currency 파라미터가 누락되었더라도 cart_items 내 첫번째 아이템에서 currency 자동 추출
        target_currency = currency
        if cart_items and isinstance(cart_items[0], dict):
            item_curr = cart_items[0].get("currency")
            if item_curr:
                target_currency = item_curr

        for item in cart_items:
            item_widget = CartItemWidget(item)
            item_widget.qty_changed_signal.connect(
                lambda p_id, delta: self.change_qty_signal.emit(p_id, delta)
            )
            item_widget.remove_requested_signal.connect(
                lambda p_id: self.remove_item_signal.emit(p_id)
            )

            list_item = QListWidgetItem(self.ui.lst_my_order_details)
            list_item.setSizeHint(item_widget.sizeHint())
            self.ui.lst_my_order_details.addItem(list_item)
            self.ui.lst_my_order_details.setItemWidget(list_item, item_widget)

        if cart_items:
            self.ui.lst_my_order_details.scrollToBottom()

        # [수정] 통화 단위 및 기호(¥ / 원) 판별 반영
        if str(target_currency).upper() == "JPY":
            price_text = f"총 ¥{total_price:,}"
        else:
            price_text = f"총 {total_price:,}원"

        self.ui.le_total_price.setText(price_text)

    #뒤로가기 시그널 이벤트 연결
    def handle_go_back_clicked(self):
        self.orderview_on_go_back_signal.emit("goback")
        pass