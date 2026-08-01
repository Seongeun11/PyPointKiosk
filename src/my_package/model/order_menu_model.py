#src\my_package\model\order_menu_model.py
import json
import os

class OrderMenuModel:
    """메뉴 데이터 및 장바구니 비즈니스 로직 관리 Model"""
    def __init__(self, json_path):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.json_path = os.path.join(self.base_dir, json_path)
        
        self.categories = []
        self.current_category_idx = 0
        # 장바구니 데이터 구조: { product_id: { "info": dict, "quantity": int } }
        self.cart: dict[str, dict] = {}
        self.load_data()

    def load_data(self):
        if not os.path.exists(self.json_path):
            print(f"[Model Error] JSON 파일이 없습니다: {self.json_path}")
            return
            
        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.categories = data.get("categories", [])
                
            for cat in self.categories:
                for prod in cat.get("products", []):
                    img_rel_path = prod.get("image", "")
                    if img_rel_path:
                        prod["image_abs_path"] = os.path.join(self.base_dir, img_rel_path)
                    else:
                        prod["image_abs_path"] = ""
        except Exception as e:
            print(f"[Model Error] JSON 데이터를 읽는 데 실패했습니다: {e}")

    def get_categories(self) -> list:
        return self.categories

    def set_category(self, idx: int):
        if 0 <= idx < len(self.categories):
            self.current_category_idx = idx

    def get_current_products(self) -> list:
        if not self.categories:
            return []
        return self.categories[self.current_category_idx].get("products", [])

    # --- 장바구니 비즈니스 로직 ---
    def add_to_cart(self, product_data: dict):
        # 고유 ID가 없으면 상품명을 Key로 사용
        p_id = str(product_data.get("id", product_data.get("name")))
        
        if p_id in self.cart:
            self.cart[p_id]["quantity"] += 1
        else:
            self.cart[p_id] = {
                "info": product_data,
                "quantity": 1
            }
    def change_quantity(self, product_id: str, delta: int):
        """수량 변경 및 0 이하 시 자동 삭제"""
        if product_id in self.cart:
            self.cart[product_id]["quantity"] += delta
            if self.cart[product_id]["quantity"] <= 0:
                self.remove_from_cart(product_id)

    def remove_from_cart(self, product_id: str):
        """단일 상품 삭제"""
        if product_id in self.cart:
            del self.cart[product_id]

    def clear_cart(self):
        """장바구니 전체 초기화"""
        self.cart.clear()

    def get_cart_items(self) -> list:
        """View 표시용 리스트 규격 변환"""
        items = []
        for p_id, data in self.cart.items():
            items.append({
                "id": p_id,
                "name": data["info"]["name"],
                "price": data["info"]["price"],
                "quantity": data["quantity"],
                "total_price": data["info"]["price"] * data["quantity"]
            })
        return items
    
    def get_total_count(self) -> int:
        """장바구니 전체 수량 합계 계산"""
        return sum(data["quantity"] for data in self.cart.values())
    
    def get_total_price(self) -> int:
        return sum(item["total_price"] for item in self.get_cart_items())