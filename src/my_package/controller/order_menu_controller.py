#src\my_package\controller\order_menu_controller.py
class OrderMenuController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # View 이벤트 바인딩
        self.view.category_clicked_signal.connect(self.handle_category_click)
        self.view.product_clicked_signal.connect(self.handle_product_click)
        self.view.pay_clicked_signal.connect(self.handle_pay_click)
        # [추가] 전체 삭제 바인딩
        self.view.clear_cart_clicked_signal.connect(self.handle_clear_cart)
        # [신규 추가] 수량 변경 및 단일 항목 삭제 핸들러 바인딩
        self.view.change_qty_signal.connect(self.handle_change_qty)
        self.view.remove_item_signal.connect(self.handle_remove_item)

        # 초기 화면 업데이트
        self.update_view()

    def update_view(self):
        categories = self.model.get_categories()
        current_idx = self.model.current_category_idx
        products = self.model.get_current_products()

        self.view.render_categories(categories, current_idx)
        self.view.render_products(products)
        self._refresh_cart_and_count()

    #def update_cart_display(self):
    #    cart_items = self.model.get_cart_items()
    #    total_price = self.model.get_total_price()
    #    self.view.update_cart_view(cart_items, total_price)

    def handle_category_click(self, category_idx: int):
        self.model.set_category(category_idx)
        self.update_view()

    def handle_product_click(self, product_data: dict):
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
    
    def handle_pay_click(self):
        total_price = self.model.get_total_price()
        if total_price == 0:
            print("[Controller] 장바구니가 비어 있습니다.")
            return
        print(f"[Controller] 결제 진행 - 총 금액: {total_price:,}원")

    def _refresh_cart_and_count(self):
        """Model 데이터를 읽어 View(장바구니 리스트 + 상품 개수)를 동기화"""
        cart_items = self.model.get_cart_items()
        total_price = self.model.get_total_price()
        
        # [수정] Model에서 직접 전체 누적 수량을 가져옴 (Key 불일치 오류 방지)
        total_count = self.model.get_total_count()

        # View 업데이트 요청
        self.view.update_cart_view(cart_items, total_price)
        self.view.update_product_count_view(total_count)