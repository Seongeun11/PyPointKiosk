#src\my_package\controller\order_menu_controller.py
class OrderMenuController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # View 이벤트 바인딩
        self.view.category_clicked_signal.connect(self.handle_category_click)
        self.view.product_clicked_signal.connect(self.handle_product_click)
        self.view.pay_clicked_signal.connect(self.handle_pay_click)
        
        # 초기 화면 업데이트
        self.update_view()

    def update_view(self):
        categories = self.model.get_categories()
        current_idx = self.model.current_category_idx
        products = self.model.get_current_products()

        self.view.render_categories(categories, current_idx)
        self.view.render_products(products)

    def handle_category_click(self, category_idx: int):
        self.model.set_category(category_idx)
        self.update_view()

    def handle_product_click(self, product_data: dict):
        print(f"[Controller] 선택된 상품: {product_data['name']} / 경로: {product_data.get('image_abs_path')}")

    def handle_pay_click(self):
        print("[Controller] 결제 진행")