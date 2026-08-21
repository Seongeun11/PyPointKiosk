import os
import shutil
from typing import Optional
from my_package.repositories.menu_json_repository import MenuJsonRepository
from my_package.utils.image_manager import ImageManager
from my_package.utils.path_utils import get_project_root

class OrderMenuModel:
    """메뉴 데이터, 다국어(한국어/일본어) 및 장바구니 비즈니스 로직 관리 Model"""

    def __init__(self, json_path: str):
        self.base_dir = get_project_root()
        if not os.path.isabs(json_path):
            self.json_path = os.path.join(self.base_dir, json_path)
        else:
            self.json_path = json_path

        self.repository = MenuJsonRepository(self.base_dir, self.json_path)
        self.categories: list = []
        self.current_category_idx: int = 0
        
        self.raw_mode: str = "ko_krw"
        self.current_lang: str = "ko"
        self.current_currency: str = "KRW"

        self.cart: dict[str, dict] = {}
        self.load_data()

    def load_data(self):
        self.categories = self.repository.load()

    def save_data(self):
        if self.repository.save(self.categories):
            self.load_data()

    def set_language_mode(self, mode: str):
        self.raw_mode = mode.lower() if mode else "ko_krw"
        if self.raw_mode == "ja_jpy":
            self.current_lang = "ja"
            self.current_currency = "JPY"
        elif self.raw_mode == "ko_jpy":
            self.current_lang = "ko"
            self.current_currency = "JPY"
        else:
            self.current_lang = "ko"
            self.current_currency = "KRW"

    def get_mode(self) -> str:
        return self.raw_mode
    
    def get_language(self) -> str:
        return self.current_lang

    def get_currency_code(self) -> str:
        return self.current_currency

    def get_currency_unit(self) -> str:
        return "¥" if self.current_currency == "JPY" else "원"

    def add_category(self, cat_name: str, cat_name_ja: str = "") -> bool:
        if not cat_name:
            return False

        existing_ids = []
        for c in self.categories:
            try:
                existing_ids.append(int(c.get("title", c.get("id", 0))))
            except (ValueError, TypeError):
                pass
        new_id = str(max(existing_ids) + 1) if existing_ids else "1"

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
        target_cat = None
        for cat in self.categories:
            if str(cat.get("title")) == str(category_id) or str(cat.get("id")) == str(category_id):
                target_cat = cat
                break

        if not target_cat:
            return False, "존재하지 않는 카테고리입니다."

        if len(target_cat.get("products", [])) > 0:
            return False, "카테고리 안에 상품이 존재하여 삭제할 수 없습니다.\n상품을 먼저 삭제하거나 다른 카테고리로 이동해주세요."

        self.categories.remove(target_cat)
        self.save_data()
        self._validate_current_category_idx()
        return True, "카테고리가 삭제되었습니다."

    def move_category_up(self, category_id: str) -> bool:
        idx = next((i for i, c in enumerate(self.categories) if str(c.get("title", c.get("id"))) == str(category_id)), -1)
        if idx > 0:
            self.categories[idx], self.categories[idx - 1] = self.categories[idx - 1], self.categories[idx]
            self.save_data()
            return True
        return False

    def move_category_down(self, category_id: str) -> bool:
        idx = next((i for i, c in enumerate(self.categories) if str(c.get("title", c.get("id"))) == str(category_id)), -1)
        if idx != -1 and idx < len(self.categories) - 1:
            self.categories[idx], self.categories[idx + 1] = self.categories[idx + 1], self.categories[idx]
            self.save_data()
            return True
        return False

    def _validate_current_category_idx(self):
        if not self.categories:
            self.current_category_idx = 0
        elif self.current_category_idx >= len(self.categories):
            self.current_category_idx = max(0, len(self.categories) - 1)

    # --- 상품 관리 (discount_jpy 인자 반영) ---
    def add_product(self, category_id: str, prod_name: str, price: int,
                    price_jpy: Optional[int] = None, image_path: str = "", 
                    discount_student: int = 0, discount_academy: int = 0, 
                    discount_jpy: int = 0, prod_name_ja: str = "") -> bool:
        """신규 상품 추가 (수련생/아카데미/엔화 고정 할인액 포함)"""
        for cat in self.categories:
            if str(cat.get("title")) == str(category_id) or str(cat.get("id")) == str(category_id):
                existing_ids = [p["id"] for c in self.categories for p in c.get("products", []) if isinstance(p.get("id"), int)]
                new_id = max(existing_ids) + 1 if existing_ids else 1

                rel_image_path = f"resources/images/{new_id}.png"
                abs_image_path = os.path.join(self.base_dir, rel_image_path)

                if image_path and os.path.exists(image_path):
                    os.makedirs(os.path.dirname(abs_image_path), exist_ok=True)
                    shutil.copy(image_path, abs_image_path)
                else:
                    ImageManager.ensure_default_sample_image(abs_image_path, prod_name)

                new_prod = {
                    "id": new_id,
                    "name": prod_name,
                    "name_ja": prod_name_ja if prod_name_ja else prod_name,
                    "price": price,
                    "price_jpy": price_jpy if price_jpy is not None else int(price // 10),
                    "discount_student": discount_student,
                    "discount_academy": discount_academy,
                    "discount_jpy": discount_jpy,
                    "image": rel_image_path,
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
                            new_price_jpy: Optional[int] = None,
                            new_disc_student: Optional[int] = None,
                            new_disc_academy: Optional[int] = None,
                            new_disc_ja: Optional[int] = None) -> bool:
        """상품 정보 수정 (엔화 할인 금액 수정 포함)"""
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

        if new_name is not None: target_prod["name"] = new_name
        if new_name_ja is not None: target_prod["name_ja"] = new_name_ja
        if new_price is not None: target_prod["price"] = new_price
        if new_price_jpy is not None: target_prod["price_jpy"] = new_price_jpy
        if new_disc_student is not None: target_prod["discount_student"] = new_disc_student
        if new_disc_academy is not None: target_prod["discount_academy"] = new_disc_academy
        if new_disc_ja is not None: target_prod["discount_jpy"] = new_disc_ja

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
        for cat in self.categories:
            products = cat.get("products", [])
            for p in products:
                if str(p["id"]) == str(product_id):
                    products.remove(p)
                    self.save_data()
                    return True
        return False

    def toggle_sold_out(self, product_id: str) -> bool:
        for cat in self.categories:
            for p in cat.get("products", []):
                if str(p["id"]) == str(product_id):
                    p["is_sold_out"] = not p.get("is_sold_out", False)
                    self.save_data()
                    return True
        return False

    def get_categories(self) -> list:
        result = []
        for cat in self.categories:
            display_name = cat.get("name_ja") if self.current_lang == "ja" and cat.get("name_ja") else cat.get("name")
            result.append({
                "title": cat.get("title", cat.get("id")),
                "name": display_name,
                "raw_name": cat.get("name"),
                "raw_name_ja": cat.get("name_ja", "")
            })
        return result

    def set_category(self, idx: int):
        if 0 <= idx < len(self.categories):
            self.current_category_idx = idx
            
    def update_category(self, category_id: str, new_name: str, new_name_ja: str = "") -> bool:
        if not new_name.strip():
            return False

        for cat in self.categories:
            if str(cat.get("title")) == str(category_id) or str(cat.get("id")) == str(category_id):
                cat["name"] = new_name.strip()
                if new_name_ja.strip():
                    cat["name_ja"] = new_name_ja.strip()
                elif "name_ja" not in cat or not cat["name_ja"]:
                    cat["name_ja"] = new_name.strip()

                self.save_data()
                return True
        return False
    
    def get_current_products(self) -> list:
        if not self.categories:
            self.current_category_idx = 0
            return []

        self._validate_current_category_idx()
        raw_products = self.categories[self.current_category_idx].get("products", [])

        display_products = []
        is_ja_lang = (self.current_lang == "ja")
        is_jpy_curr = (self.current_currency == "JPY")

        for p in raw_products:
            name = p.get("name_ja") if is_ja_lang and p.get("name_ja") else p.get("name")

            if is_jpy_curr:
                price = p.get("price_jpy") if p.get("price_jpy") is not None else int(p.get("price", 0) // 10)
                price_str = f"¥{price:,}"
            else:
                price = p.get("price", 0)
                price_str = f"{price:,}원"

            rel_image = p.get("image", "")
            abs_image_path = ImageManager.get_absolute_image_path(self.base_dir, rel_image)

            p_display = dict(p)
            p_display["display_name"] = name
            p_display["computed_price"] = price
            p_display["price_str"] = price_str
            p_display["image_abs_path"] = abs_image_path
            display_products.append(p_display)

        return display_products
    
    def add_to_cart(self, product_data: dict):
        p_id = str(product_data.get("id", product_data.get("name")))
        if p_id in self.cart:
            self.cart[p_id]["quantity"] += 1
        else:
            self.cart[p_id] = {
                "info": product_data,
                "quantity": 1
            }

    def change_quantity(self, product_id: str, delta: int):
        p_id_str = str(product_id)
        if p_id_str in self.cart:
            self.cart[p_id_str]["quantity"] += delta
            if self.cart[p_id_str]["quantity"] <= 0:
                self.remove_from_cart(p_id_str)

    def remove_from_cart(self, product_id: str):
        p_id_str = str(product_id)
        if p_id_str in self.cart:
            del self.cart[p_id_str]

    def clear_cart(self):
        self.cart.clear()

    def get_cart_items(self) -> list:
        items = []
        is_ja_lang = (self.current_lang == "ja")
        is_jpy_curr = (self.current_currency == "JPY")

        for p_id, data in self.cart.items():
            info = data["info"]
            qty = data["quantity"]

            name = info.get("name_ja") if is_ja_lang and info.get("name_ja") else info.get("name")
            
            if is_jpy_curr:
                price = info.get("price_jpy") if info.get("price_jpy") is not None else int(info.get("price", 0) // 10)
                unit = "¥"
            else:
                price = info.get("price", 0)
                unit = "원"

            total_price = price * qty
            price_str = f"{unit}{total_price:,}" if unit == "¥" else f"{total_price:,}원"

            items.append({
                "id": p_id,
                "name": name,
                "price": price,
                "quantity": qty,
                "total_price": total_price,
                "discount_student": info.get("discount_student", 0),
                "discount_academy": info.get("discount_academy", 0),
                "discount_jpy": info.get("discount_jpy", 0),
                "currency": self.current_currency,
                "unit": unit,
                "price_str": price_str
            })
            #print("json저장완료")
        return items

    def get_total_count(self) -> int:
        return sum(data["quantity"] for data in self.cart.values())

    def get_total_price(self) -> int:
        return sum(item["total_price"] for item in self.get_cart_items())

    def on_view_go_back(self, message: str):
        print(message)