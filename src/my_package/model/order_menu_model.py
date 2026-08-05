#src\my_package\model\order_menu_model.py
import json
import os
from typing import Optional

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

    def save_data(self):
        """변경된 카테고리/상품 데이터를 JSON 파일에 영구 저장"""
        save_categories = []
        for cat in self.categories:
            cat_copy = {
                "id": cat.get("id"),
                "name": cat.get("name"),
                "products": []
            }
            for prod in cat.get("products", []):
                p_copy = {
                    "id": prod.get("id"),
                    "name": prod.get("name"),
                    "price": prod.get("price"),
                    "image": prod.get("image", ""),
                    "is_sold_out": prod.get("is_sold_out", False)
                }
                cat_copy["products"].append(p_copy)
            save_categories.append(cat_copy)

        out_data = {"categories": save_categories}
        try:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(out_data, f, ensure_ascii=False, indent=2)
            # 재로드하여 절대경로 재계산
            self.load_data()
        except Exception as e:
            print(f"[Model Error] JSON 데이터를 저장하는 데 실패했습니다: {e}")
    def add_category(self, cat_name: str) -> bool:
        """신규 카테고리 추가"""
        if not cat_name:
            return False
            
        existing_ids = []
        for c in self.categories:
            try:
                existing_ids.append(int(c.get("id")))
            except (ValueError, TypeError):
                pass
        new_id = str(max(existing_ids) + 1) if existing_ids else "cat_1"

        new_category = {
            "id": new_id,
            "name": cat_name,
            "products": []
        }
        self.categories.append(new_category)
        self.save_data()
        return True

    def remove_category(self, category_id: str) -> tuple[bool, str]:
        """카테고리 삭제 (상품 존재 여증 검증 및 안전 인덱스 조정)"""
        target_cat = None
        for cat in self.categories:
            if str(cat["id"]) == str(category_id):
                target_cat = cat
                break
                
        if not target_cat:
            return False, "존재하지 않는 카테고리입니다."

        if len(target_cat.get("products", [])) > 0:
            return False, "카테고리 안에 상품이 존재하여 삭제할 수 없습니다.\n상품을 먼저 삭제하거나 다른 카테고리로 이동해주세요."

        self.categories.remove(target_cat)
        self.save_data()

        # [핵심 보완] 카테고리 삭제 후 현재 선택 인덱스가 범위를 벗어나지 않도록 안심 조정
        self._validate_current_category_idx()

        return True, "카테고리가 삭제되었습니다."
    def _validate_current_category_idx(self):
        """현재 카테고리 인덱스 유효성 검증 및 자동 보정"""
        if not self.categories:
            self.current_category_idx = 0
        elif self.current_category_idx >= len(self.categories):
            self.current_category_idx = max(0, len(self.categories) - 1)
            
    def add_product(self, category_id: str, prod_name: str, price: int, image_path: str = ""):
        """신규 상품 추가"""
        for cat in self.categories:
            if cat["id"] == category_id:
                # 새 ID 생성 (가장 큰 ID + 1)
                existing_ids = [p["id"] for c in self.categories for p in c.get("products", []) if isinstance(p.get("id"), int)]
                new_id = max(existing_ids) + 1 if existing_ids else 1
                
                new_prod = {
                    "id": new_id,
                    "name": prod_name,
                    "price": price,
                    "image": image_path,
                    "is_sold_out": False
                }
                cat["products"].append(new_prod)
                self.save_data()
                return True
        return False
    
 

    # ==========================================
    # [핵심 수정] 상품 정보 수정 (기본값 설정 = None)
    # ==========================================
    def update_product_info(self, product_id: str, new_cat_name: Optional[str] = None, new_name: Optional[str] = None, new_price: Optional[int] = None) -> bool:
        """
        TypeError 방지를 위해 모든 파라미터에 선택적 기본값(= None) 설정
        """
        target_prod = None
        current_cat = None

        # 1. 수정할 상품 찾기
        for cat in self.categories:
            for p in cat.get("products", []):
                if str(p["id"]) == str(product_id):
                    target_prod = p
                    current_cat = cat
                    break
            if target_prod:
                break

        if not target_prod:
            return False

        # 2. 상품명 변경
        if new_name is not None:
            target_prod["name"] = new_name

        # 3. 가격 변경
        if new_price is not None:
            target_prod["price"] = new_price

        # 4. 카테고리 변경 (이동)
        if new_cat_name is not None and current_cat is not None and new_cat_name != current_cat.get("name"):
            dest_cat = next((c for c in self.categories if c["name"] == new_cat_name), None)
            if dest_cat:
                current_cat["products"].remove(target_prod)
                dest_cat["products"].append(target_prod)
            else:
                return False

        self.save_data()
        return True

    
    def remove_product(self, product_id):
        """상품 제거"""
        for cat in self.categories:
            products = cat.get("products", [])
            for p in products:
                if str(p["id"]) == str(product_id):
                    products.remove(p)
                    self.save_data()
                    return True
        return False

    def toggle_sold_out(self, product_id):
        """판매/품절 상태 전환"""
        for cat in self.categories:
            for p in cat.get("products", []):
                if str(p["id"]) == str(product_id):
                    p["is_sold_out"] = not p.get("is_sold_out", False)
                    self.save_data()
                    return True
        return False

    def get_categories(self) -> list:
        return self.categories

    def set_category(self, idx: int):
        if 0 <= idx < len(self.categories):
            self.current_category_idx = idx

    def get_current_products(self) -> list:
        """[수정] 에러 방지를 위해 인덱스 범위를 안전하게 재검증 후 상품 목록 반환"""
        # 1. 카테고리가 완전히 비어있는 경우
        if not self.categories:
            self.current_category_idx = 0
            return []

        # 2. 인덱스가 범위를 벗어난 경우 자동 보정
        self._validate_current_category_idx()

        # 3. 안전하게 상품 리스트 반환
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