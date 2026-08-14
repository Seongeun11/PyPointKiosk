# src\my_package\model\order_menu_model.py

import os
import shutil
from typing import Optional
from repositories.menu_json_repository import MenuJsonRepository
from utils.image_manager import ImageManager

class OrderMenuModel:
    """메뉴 데이터, 다국어(한국어/일본어) 및 장바구니 비즈니스 로직 관리 Model"""

    def __init__(self, json_path: str):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        
        # 절대 경로와 상대 경로 결합 안전 보장
        if not os.path.isabs(json_path):
            self.json_path = os.path.join(self.base_dir, json_path)
        else:
            self.json_path = json_path

        # 절대 경로(self.json_path)를 Repository에 전달
        self.repository = MenuJsonRepository(self.base_dir, self.json_path)

        self.categories: list = []
        self.current_category_idx: int = 0
        
        # 언어 및 통화 상태 분리
        self.raw_mode: str = "ko_krw" # [추가] 원본 모드 문자열 저장
        self.current_lang: str = "ko"       # 'ko' 또는 'ja'
        self.current_currency: str = "KRW"  # 'KRW' 또는 'JPY'

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

    # --- 언어 및 통화 모드 설정 ---
    def set_language_mode(self, mode: str):
        """'ko_krw', 'ko_jpy', 'ja_jpy' 규격 처리"""
        self.raw_mode = mode.lower() if mode else "ko_krw" # [수정] 원본 모드 저장
        if self.raw_mode == "ja_jpy":
            self.current_lang = "ja"
            self.current_currency = "JPY"
        elif self.raw_mode == "ko_jpy":
            self.current_lang = "ko"
            self.current_currency = "JPY"
        else:  # ko_krw 또는 기본값
            self.current_lang = "ko"
            self.current_currency = "KRW"

    def get_mode(self) -> str:
        """[신규] 설정된 원본 모드 반환"""
        return self.raw_mode
    
    def get_language(self) -> str:
        return self.current_lang

    def get_currency_code(self) -> str:
        return self.current_currency

    def get_currency_unit(self) -> str:
        return "¥" if self.current_currency == "JPY" else "원"

    # --- 카테고리 관리 ---
    def add_category(self, cat_name: str, cat_name_ja: str = "") -> bool:
        """신규 카테고리 추가 (한국어/일본어 지원)"""
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
        """카테고리 삭제 (상품 존재 여부 검증 및 안전 인덱스 조정)"""
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
        """신규 상품 추가 (한국어/일본어 및 원화/엔화 포함)(ID 기반 이미지 경로 자동 지정)"""
        for cat in self.categories:
            if str(cat.get("title")) == str(category_id) or str(cat.get("id")) == str(category_id):
                existing_ids = [p["id"] for c in self.categories for p in c.get("products", []) if isinstance(p.get("id"), int)]
                new_id = max(existing_ids) + 1 if existing_ids else 1

               # 2. 경로 설정 (JSON용 상대경로 / 실제 파일작업용 절대경로)
                rel_image_path = f"resources/images/{new_id}.png"
                abs_image_path = os.path.join(self.base_dir, rel_image_path)

                # 3. 이미지 파일 처리 로직
                if image_path and os.path.exists(image_path):
                    # 외부에서 지정한 이미지가 있으면 ID 규칙에 맞게 복사
                    os.makedirs(os.path.dirname(abs_image_path), exist_ok=True)
                    shutil.copy(image_path, abs_image_path)
                else:
                    # 지정된 이미지가 없으면 default.png 복사 또는 예시 이미지 생성
                    ImageManager.ensure_default_sample_image(abs_image_path, prod_name)

                new_prod = {
                    "id": new_id,
                    "name": prod_name,
                    "name_ja": prod_name_ja if prod_name_ja else prod_name,
                    "price": price,
                    "price_jpy": price_jpy if price_jpy is not None else int(price // 10),
                    "image": rel_image_path,  # JSON에는 항상 규격화된 상대 경로 저장
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

    # --- 뷰(View) 전용 조회 메서드 ---
    def get_categories(self) -> list:
        """현재 선택된 언어에 맞춘 카테고리 목록 반환"""
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

    def get_current_products(self) -> list:
        """현재 선택된 카테고리의 상품 정보 및 다국어/다중통화 계산된 정보 반환"""
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

            # ImageManager를 이용한 절대 경로 계산
            rel_image = p.get("image", "")
            abs_image_path = ImageManager.get_absolute_image_path(self.base_dir, rel_image)

            p_display = dict(p)
            p_display["display_name"] = name
            p_display["computed_price"] = price
            p_display["price_str"] = price_str
            p_display["image_abs_path"] = abs_image_path
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
        p_id_str = str(product_id)
        if p_id_str in self.cart:
            self.cart[p_id_str]["quantity"] += delta
            if self.cart[p_id_str]["quantity"] <= 0:
                self.remove_from_cart(p_id_str)

    def remove_from_cart(self, product_id: str):
        """단일 상품 삭제"""
        p_id_str = str(product_id)
        if p_id_str in self.cart:
            del self.cart[p_id_str]

    def clear_cart(self):
        """장바구니 전체 초기화"""
        self.cart.clear()

    def get_cart_items(self) -> list:
        """현재 언어 및 통화 상태가 실시간 계산되어 반영된 장바구니 리스트 반환"""
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
                total_price = price * qty
                price_str = f"¥{total_price:,}"
            else:
                price = info.get("price", 0)
                unit = "원"
                total_price = price * qty
                price_str = f"{total_price:,}원"

            items.append({
                "id": p_id,
                "name": name,
                "price": price,
                "quantity": qty,
                "total_price": total_price,
                "currency": self.current_currency,
                "unit": unit,
                "price_str": price_str
            })
        return items

    def get_total_count(self) -> int:
        """장바구니 전체 수량 합계 계산"""
        return sum(data["quantity"] for data in self.cart.values())

    def get_total_price(self) -> int:
        """현재 선택된 언어/통화 기준의 장바구니 총 금액 합계"""
        return sum(item["total_price"] for item in self.get_cart_items())

    def on_view_go_back(self, message: str):
        print(message)