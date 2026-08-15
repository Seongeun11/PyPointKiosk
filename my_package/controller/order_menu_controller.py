#my_package\controller\order_menu_controller.py
from PySide6.QtCore import QObject, Signal

from my_package.view.admin_menu_dialog_view import AdminMenuDialogView  # QObject, Signal 추가

class OrderMenuController(QObject):         # QObject 상속 추가
    # [수정] 결제 요청 시그널에 currency(str) 매개변수 추가 (cart_items, total_price, currency)
    pay_requested_signal = Signal(list, int, str)
    go_back_requested_signal = Signal()
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        
      
        
        # View 이벤트 바인딩
        self.view.category_clicked_signal.connect(self.handle_category_click)
        self.view.product_clicked_signal.connect(self.handle_product_click)
        self.view.pay_clicked_signal.connect(self.handle_pay_click)
        # [추가] 전체 삭제 바인딩
        self.view.clear_cart_clicked_signal.connect(self.handle_clear_cart)
        self.view.title_double_clicked_signal.connect(self.handle_title_double_click)  # [추가] 타이틀 클릭 이벤트 바인딩
        # [신규 추가] 수량 변경 및 단일 항목 삭제 핸들러 바인딩
        self.view.change_qty_signal.connect(self.handle_change_qty)
        self.view.remove_item_signal.connect(self.handle_remove_item)
        #뒤로가기 핸들러
        self.view.orderview_on_go_back_signal.connect(self.handle_go_back)
        # 초기 화면 업데이트
        self.update_view()

    def set_language(self, mode: str):
        """[수정] 모드 코드를 모델에 반영하고 뷰 동기화"""
        self.model.set_language_mode(mode)
        self.update_view()

    def update_view(self):
        categories = self.model.get_categories()
        current_idx = self.model.current_category_idx
        products = self.model.get_current_products()

        self.view.render_categories(categories, current_idx)
        self.view.render_products(products)
        self._refresh_cart_and_count()

    def _refresh_cart_and_count(self):
        cart_items = self.model.get_cart_items()
        total_price = self.model.get_total_price()
        total_count = self.model.get_total_count()
        current_currency = self.model.get_currency_code()

        # [수정] 통화 코드를 명시적으로 전달
        self.view.update_cart_view(cart_items, total_price, currency=current_currency)
        self.view.update_product_count_view(total_count)

    def handle_title_double_click(self):
            print("[Controller] 타이틀 클릭 - 메인 메뉴로 돌아가기 요청")
            dialog = AdminMenuDialogView(self.model, parent=self.view)
            # 관리자 창이 닫히면 키오스크 메인 화면 업데이트
            dialog.exec()
            self.update_view()

    def handle_category_click(self, category_idx: int):
        self.model.set_category(category_idx)
        self.update_view()

    def handle_product_click(self, product_data: dict):
        # [품절 상품 차단 방어 로직]
        if product_data.get("is_sold_out", False):
            print(f"[Controller] '{product_data.get('name')}' 상품은 품절 상태이므로 선택할 수 없습니다.")
            return

        self.model.add_to_cart(product_data)
        self._refresh_cart_and_count()
        
    def handle_change_qty(self, product_id: str, delta: int):
        """수량 변경 (+1, -1) 처리"""
        self.model.change_quantity(product_id, delta)
        self._refresh_cart_and_count()

    def handle_remove_item(self, product_id: str):
        """장바구니 개별 항목 삭제 처리"""
        self.model.remove_from_cart(product_id)
        self._refresh_cart_and_count()
    def handle_clear_cart(self):
        """장바구니 비우기 핸들러"""
        self.model.clear_cart()
        self._refresh_cart_and_count()
    
    # src/my_package/controller/order_menu_controller.py

    def handle_pay_click(self):
        total_price = self.model.get_total_price()
        if total_price == 0:
            print("[Controller] 장바구니가 비어 있습니다.")
            return

        cart_items = self.model.get_cart_items()
        raw_mode = self.model.get_mode() # [수정] 단순 lang이 아닌 원본 mode("ko_jpy" 등) 추출
        currency_code = self.model.get_currency_code()

        print(f"[Controller] 결제 진행 - 통화: {currency_code}, 모드: {raw_mode}, 총 금액: {total_price:,}")

        # [수정] raw_mode를 결제 시그널로 전달
        self.pay_requested_signal.emit(cart_items, total_price, raw_mode)
        
    def handle_go_back(self):
        self.model.on_view_go_back("order_view_goback")
        self.model.clear_cart()
        self._refresh_cart_and_count()
        
        # Root Controller로 화면 전환 요청 전달
        self.go_back_requested_signal.emit()