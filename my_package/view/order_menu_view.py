#my_package\view\order_menu_view.py
from PySide6.QtWidgets import (
    QWidget, QSizePolicy, QPushButton, QToolButton, QLayout, QSpacerItem,
    QScrollArea, QHBoxLayout, QGridLayout, QListWidgetItem
)
from PySide6.QtGui import QIcon, QResizeEvent, QShowEvent, QMouseEvent,QFontMetrics,QPalette,QColor
from PySide6.QtCore import QSize, Qt, Signal, QTimer

# 자동 생성된 UI 클래스 import
from my_package.ui.ui_order_menu import Ui_Form 
from my_package.custom_widget.cart_item_widget import CartItemWidget #장바구니 관리 클래스
from my_package.utils.image_manager import ImageManager #이미지 관리 유틸리티 클래스
from my_package.utils.base_scaled_manager import BaseScaledWidget
# 타이틀 버튼의 더블클릭을 감지하기 위한 Custom PushButton
class TitleButton(QPushButton):
    double_clicked = Signal()

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit()
        super().mouseDoubleClickEvent(event)

class OrderMenuView(BaseScaledWidget):
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

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.setMinimumSize(720, 880)
        # 4열 고정 규격
        self.GRID_COLS = 4
        self.GRID_ROWS = 4
        # 1페이지당 기본 아이템 개수 (열 x 행)
        self.GRID_PAGE_SIZE = self.GRID_COLS * self.GRID_ROWS
        
        # 행 수에 따른 버튼 적정 높이 계산 (예: 2행=300px, 3행=200px 등)
        # 키오스크 해상도나 레이아웃에 맞춰 적절한 기본 높이 로직을 적용합니다.
        self.BUTTON_HEIGHT = 200
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

        # 기본 화면 비율 계산 (BaseScaledWidget 기준과 통일)
        base_scale = min(w / self.width(), h / self.height())
        
        # 폰트 크기 단계별 산출 (최소pt ~ 최대pt)
        title_font_size = max(20, min(int(30 * base_scale), 32))
        cat_font_size   = max(28, min(int(30 * base_scale), 32))
        prod_font_size  = max(11, min(int(14 * base_scale), 24))
        sub_font_size   = max(11, min(int(13 * base_scale), 22)) # [추가] 하단 정보용
        pay_font_size   = max(16, min(int(22 * base_scale), 40))

        # 1. 타이틀 버튼 (btn_title) 및 뒤로가기 버튼 (btn_back)
        if hasattr(self.ui, "btn_title"):
            font = self.ui.btn_title.font()
            font.setPointSize(title_font_size)
            self.ui.btn_title.setFont(font)

        #if hasattr(self.ui, "btn_back"):
        #    font = self.ui.btn_back.font()
        #    font.setPointSize(sub_font_size)
        #    self.ui.btn_back.setFont(font)

        # 2. 카테고리 버튼들
        for i in range(self.category_layout.count()):
            item = self.category_layout.itemAt(i)
            widget = item.widget() if item else None
            if widget:
                font = widget.font()
                font.setPointSize(cat_font_size)
                widget.setFont(font)

        # 3. 메뉴 상품 버튼들
        for i in range(self.menu_grid_layout.count()):
            layout_item = self.menu_grid_layout.itemAt(i)
            widget = layout_item.widget() if layout_item else None
            
            if isinstance(widget, QToolButton) and widget.isEnabled():
                btn_w, btn_h = widget.width(), widget.height()

                if btn_w > 20 and btn_h > 20:
                    icon_dim = max(50, min(int(min(btn_w, btn_h) * 0.52), 300))
                    widget.setIconSize(QSize(icon_dim, icon_dim))

                font = widget.font()
                font.setPointSize(prod_font_size)
                widget.setFont(font)

        # 4. [해결/추가] 하단 주문 정보 LineEdit 및 버튼 일괄 스케일링
        #info_widgets = [
        #    getattr(self.ui, "lb_select_products", None), # 선택 개수
        #    getattr(self.ui, "lb_total_price", None),      # 총 금액
        #    getattr(self.ui, "lb_time_counter", None),     # 남은 시간 라벨
        #    getattr(self.ui, "lb_time_num", None),         # 남은 시간 숫자
        #    getattr(self.ui, "btn_all_delete", None)       # 전체 삭제 버튼
        #]

        #for widget in info_widgets:
        #    if widget:
        #        font = widget.font()
                # 총 금액과 전체삭제 버튼은 약간 강조
        #        if widget in (self.ui.lb_total_price, self.ui.btn_all_delete):
        #            font.setPointSize(int(sub_font_size * 1.15))
        #        else:
        #            font.setPointSize(sub_font_size)
        #        widget.setFont(font)

        # 5. [해결/추가] 장바구니 리스트(QListWidget) 폰트 스케일링
        #if hasattr(self.ui, "lst_my_order_details"):
        #    font = self.ui.lst_my_order_details.font()
        #    font.setPointSize(sub_font_size)
        #    self.ui.lst_my_order_details.setFont(font)

        # 6. 결제 버튼 (btn_payment)
        if hasattr(self.ui, "btn_payment"):
        # font-weight 및 font-size를 CSS에서 제외하여 폰트 상속 유지
        # CSS 대신 QPalette를 통해 색상 적용 (폰트 스케일링 유지를 위함)
            palette_green = self.ui.btn_payment.palette()
            palette_green.setColor(QPalette.ColorRole.Button, QColor("#019811"))
            self.ui.btn_payment.setPalette(palette_green)
                    
        #    font = self.ui.btn_payment.font()
        #    font.setPointSize(pay_font_size)
        #    self.ui.btn_payment.setFont(font)
            
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
                    font-size: 18px;
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
    # [교정된] render_products : 항상 GRID_PAGE_SIZE(16개) 이상 
    # 및 4열 규격(4의 배수)을 보장하여 동일한 높이/크기 유지
    # ---------------------------------------------------------
    def render_products(self, products: list):
        self._clear_layout(self.menu_grid_layout)

        # 1. 열(Column) 비율을 1:1:1:1로 동일하게 유지
        for col in range(self.GRID_COLS):
            self.menu_grid_layout.setColumnStretch(col, 1)

        total_items = len(products)
        
        # [원인 해결 핵심] 아이템 수가 10개('잔' 카테고리)여도 최소 16개(4행x4열) 보장
        # 16개 초과 시에는 4의 배수로 반올림하여 항상 채워진 행 규격 유지
        if total_items <= self.GRID_PAGE_SIZE:
            display_items = self.GRID_PAGE_SIZE
        else:
            display_items = ((total_items + self.GRID_COLS - 1) // self.GRID_COLS) * self.GRID_COLS

        # 2. 행(Row) 개수 계산
        total_rows = display_items // self.GRID_COLS
        for r in range(total_rows):
            self.menu_grid_layout.setRowStretch(r, 0)

        # 3. 실제 상품 및 더미 위젯 배치
        for idx in range(display_items):
            row = idx // self.GRID_COLS
            col = idx % self.GRID_COLS

            if idx < total_items:
                btn = self._create_product_button(products[idx], self.PRODUCT_BTN_HEIGHT)
                self.menu_grid_layout.addWidget(btn, row, col)
            else:
                # 동일 규격의 투명 더미 버튼으로 빈 공간 채움
                dummy_btn = self._create_dummy_button(self.PRODUCT_BTN_HEIGHT)
                self.menu_grid_layout.addWidget(dummy_btn, row, col)

        # 4. 하단 여백 밀어내기 스페이서 추가 (정확히 total_rows 위치에 배치)[cite: 1]
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

        # 1. 원본 상품명 추출
        raw_name = str(product_data.get('display_name', product_data.get('name', '')))
        
        # 2. 버튼 내 텍스트 표시 가능 가용 너비 계산 (버튼 마진 및 패딩 고려: 약 20px 차감)
        # GRID_COLS(4열) 스크롤 영역 내부 너비를 기준으로 동적 계산하거나, 안전치 적용
        font = btn.font()
        metrics = QFontMetrics(font)
        
        # 4열 기준 대략적인 1개 버튼 가용 너비 (예: 120~150px 기준 safety max limits)
        # grid layout 안에서 버튼이 고정폭을 유지하도록 max_text_width 설정
        max_text_width = 70  

        # 3. QFontMetrics 기반 동적 자동 줄바꿈(Word Wrap) 처리 함수
        def wrap_text_by_pixel(text: str, max_width: int, metrics: QFontMetrics) -> str:
            lines = []
            current_line = ""
            
            for char in text:
                # 공백이나 기존 줄바꿈이 있을 경우
                if char == '\n':
                    lines.append(current_line)
                    current_line = ""
                    continue
                    
                test_line = current_line + char
                # 픽셀 너비 측정 후 초과 시 줄바꿈 처리
                if metrics.horizontalAdvance(test_line) > max_width and current_line:
                    lines.append(current_line)
                    current_line = char
                else:
                    current_line = test_line
                    
            if current_line:
                lines.append(current_line)
                
            return "\n".join(lines)

        formatted_name = wrap_text_by_pixel(raw_name, max_text_width, metrics)
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
        """장바구니/선택된 전체 상품 개수를 lb_select_products에 반영"""
        if hasattr(self.ui, "lb_select_products"):
            self.ui.lb_select_products.setText(f"{total_count}개")
            # 필요 시 읽기 전용으로 보장
            #self.ui.lb_select_products.setReadOnly(True)

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

        self.ui.lb_total_price.setText(price_text)

    #뒤로가기 시그널 이벤트 연결
    def handle_go_back_clicked(self):
        self.orderview_on_go_back_signal.emit("goback")
        pass