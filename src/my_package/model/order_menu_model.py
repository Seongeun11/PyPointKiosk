#src\my_package\model\order_menu_model.py
import json
import os

class OrderMenuModel:
    """메뉴 데이터 및 이미지 경로, 키오스크 상태 관리 Model"""
    def __init__(self, json_path):
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.json_path = os.path.join(self.base_dir, json_path)
        
        self.categories = []
        self.current_category_idx = 0
        
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
        """선택된 카테고리의 전체 상품 반환 (뷰에서 4열 그리드 스크롤 처리)"""
        if not self.categories:
            return []
        return self.categories[self.current_category_idx].get("products", [])