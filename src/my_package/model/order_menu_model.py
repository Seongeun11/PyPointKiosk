#src\my_package\model\order_menu_model.py
import os
from typing import Optional
from repositories.menu_json_repository import MenuJsonRepository

class OrderMenuModel:
    """메뉴 데이터, 다국어(한국어/일본어) 및 장바구니 비즈니스 로직 관리 Model"""
    
    def __init__(self, json_path: str):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
         # 절대 경로와 상대 경로 결합 안전 보장
        if not os.path.isabs(json_path):
            self.json_path = os.path.join(self.base_dir, json_path)
        else:
            self.json_path = json_path

        #절대 경로(self.json_path)를 Repository에 전달
        self.repository = MenuJsonRepository(self.base_dir, self.json_path)

       


        self.categories: list = []
        self.current_category_idx: int = 0
        self.current_lang:str = "ko"  # 기본 언어: 'ko' (한국어/KRW), 'ja' (일본어/JPY)

        # 장바구니 데이터 구조: { product_id: { "info": dict, "quantity": int } }
        self.cart: dict[str, dict] = {}
        self.load_data()

    # --- 데이터 동기화 ---
    def load_data(self):
        """Repository를 통한 데이터 로드"""
        self.categories = self.repository.load()

    def save_data(self):
        """Repository를 통한 데이터 저장 및 최신화"""
        if self.repository.save(self.categories):
            self.load_data()


    # --- 언어 설정 및 조회 ---
    def set_language(self, lang: str):
        """언어 설정 변경 ('ko' 또는 'ja')"""
        if lang in ["ko", "ja"]:
            self.current_lang = lang

    def get_language(self) -> str:
        return self.current_lang

    
    # --- 카테고리 관리 ---
    def add_category(self, cat_name: str, cat_name_ja: str = "") -> bool:
        """신규 카테고리 추가 (한국어/일본어 지원)"""
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
            "title": new_id,
            "name": cat_name,
            "name_ja": cat_name_ja if cat_name_ja else cat_name,
            "products": []
        }
        self.categories.append(new_category)
        self.save_data()
        return True

    def remove_category(self, category_id: str) -> tuple[bool, str]:
        """카테고리 삭제 (상품 존재 여부 검증 및 안전 인덱스 조정)"""
        target_cat = None
        for cat in self.categories:
            if str(cat["title"]) == str(category_id):
                target_cat = cat
                break
                
        if not target_cat:
            return False, "존재하지 않는 카테고리입니다."

        if len(target_cat.get("products", [])) > 0:
            return False, "카테고리 안에 상품이 존재하여 삭제할 수 없습니다.\n상품을 먼저 삭제하거나 다른 카테고리로 이동해주세요."

        self.categories.remove(target_cat)
        self.save_data()

        # 카테고리 삭제 후 선택 인덱스 안심 조정
        self._validate_current_category_idx()

        return True, "카테고리가 삭제되었습니다."

    def _validate_current_category_idx(self):
        """현재 카테고리 인덱스 유효성 검증 및 자동 보정"""
        if not self.categories:
            self.current_category_idx = 0
        elif self.current_category_idx >= len(self.categories):
            self.current_category_idx = max(0, len(self.categories) - 1)

    # --- 상품 관리 ---
    def add_product(self, category_id: str, prod_name: str, price: int, 
                    prod_name_ja: str = "", price_jpy: Optional[int] = None, image_path: str = "") -> bool:
        """신규 상품 추가 (한국어/일본어 및 원화/엔화 포함)"""
        for cat in self.categories:
            # [수정] 타입 안전성을 보장하기 위해 str()로 비교
            if str(cat["title"]) == str(category_id):
                existing_ids = [p["id"] for c in self.categories for p in c.get("products", []) if isinstance(p.get("id"), int)]
                new_id = max(existing_ids) + 1 if existing_ids else 1
                
                new_prod = {
                    "id": new_id,
                    "name": prod_name,
                    "name_ja": prod_name_ja if prod_name_ja else prod_name,
                    "price": price,
                    "price_jpy": price_jpy if price_jpy is not None else int(price // 10),
                    "image": image_path,
                    "is_sold_out": False
                }
                cat["products"].append(new_prod)
                self.save_data()
                return True
        return False

    def update_product_info(self, product_id: str, 
                            new_cat_name: Optional[str] = None, 
                            new_name: Optional[str] = None, 
                            new_name_ja: Optional[str] = None,
                            new_price: Optional[int] = None,
                            new_price_jpy: Optional[int] = None) -> bool:
        """상품 정보 수정 (다국어 정보 포함)"""
        target_prod = None
        current_cat = None

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

        if new_name is not None:
            target_prod["name"] = new_name
        if new_name_ja is not None:
            target_prod["name_ja"] = new_name_ja
        if new_price is not None:
            target_prod["price"] = new_price
        if new_price_jpy is not None:
            target_prod["price_jpy"] = new_price_jpy

        # 카테고리 이동 처리
        if new_cat_name is not None and current_cat is not None and new_cat_name != current_cat.get("name"):
            dest_cat = next((c for c in self.categories if c["name"] == new_cat_name), None)
            if dest_cat:
                current_cat["products"].remove(target_prod)
                dest_cat["products"].append(target_prod)
            else:
                return False

        self.save_data()
        return True

    def remove_product(self, product_id: str) -> bool:
        """상품 제거"""
        for cat in self.categories:
            products = cat.get("products", [])
            for p in products:
                if str(p["id"]) == str(product_id):
                    products.remove(p)
                    self.save_data()
                    return True
        return False

    def toggle_sold_out(self, product_id: str) -> bool:
        """판매/품절 상태 전환"""
        for cat in self.categories:
            for p in cat.get("products", []):
                if str(p["id"]) == str(product_id):
                    p["is_sold_out"] = not p.get("is_sold_out", False)
                    self.save_data()
                    return True
        return False

    def get_categories(self) -> list:
        """현재 선택된 언어에 맞춘 카테고리 목록 반환"""
        result = []
        for cat in self.categories:
            display_name = cat.get("name_ja") if self.current_lang == "ja" and cat.get("name_ja") else cat.get("name")
            result.append({
                "title": cat.get("title"),
                "name": display_name,
                "raw_name": cat.get("name"),
                "raw_name_ja": cat.get("name_ja", "")
            })
        return result

    def set_category(self, idx: int):
        if 0 <= idx < len(self.categories):
            self.current_category_idx = idx

    def get_current_products(self) -> list:
        """현재 언어 모드에 적합하게 변환된 상품 목록 반환"""
        if not self.categories:
            self.current_category_idx = 0
            return []

        self._validate_current_category_idx()
        raw_products = self.categories[self.current_category_idx].get("products", [])
        
        display_products = []
        for p in raw_products:
            is_ja = (self.current_lang == "ja")
            name = p.get("name_ja") if is_ja and p.get("name_ja") else p.get("name")
            price = p.get("price_jpy", int(p.get("price", 0) // 10)) if is_ja else p.get("price", 0)
            
            p_display = dict(p)  # 원본 딕셔너리 복사 (name_ja, price_jpy 등 원본 필드 유지)
            p_display["display_name"] = name
            p_display["display_price"] = price
            p_display["price_str"] = f"¥{price:,}" if is_ja else f"{price:,}원"
            display_products.append(p_display)

        return display_products

    # --- 장바구니 비즈니스 로직 ---
    def add_to_cart(self, product_data: dict):
        """장바구니 담기 (고유 ID 기반)"""
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
        """현재 언어(원화/엔화) 설정에 맞춰 동적으로 계산된 장바구니 리스트 반환"""
        items = []
        is_ja = (self.current_lang == "ja")

        for p_id, data in self.cart.items():
            info = data["info"]
            qty = data["quantity"]

            name = info.get("name_ja") if is_ja and info.get("name_ja") else info.get("name")
            price = info.get("price_jpy", int(info.get("price", 0) // 10)) if is_ja else info.get("price", 0)
            
            items.append({
                "id": p_id,
                "name": name,
                "price": price,
                "quantity": qty,
                "total_price": price * qty,
                "price_str": f"¥{price * qty:,}" if is_ja else f"{price * qty:,}원"
            })
        return items

    def get_total_count(self) -> int:
        """장바구니 전체 수량 합계 계산"""
        return sum(data["quantity"] for data in self.cart.values())

    def get_total_price(self) -> int:
        """현재 선택된 언어/통화 기준의 장바구니 총 금액 합계"""
        return sum(item["total_price"] for item in self.get_cart_items())