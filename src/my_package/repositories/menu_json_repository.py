#src\my_package\repositories\menu_json_repository.py
import json
import os

class MenuJsonRepository:
    """JSON 파일 Persistence I/O 관리 담당 계층"""

    def __init__(self, base_dir: str, json_path: str):
        self.base_dir = base_dir
        # [수정] 넘겨받은 경로가 상대 경로일 경우를 대비해 한번 더 안전하게 절대 경로화
        self.json_path = os.path.abspath(json_path) if not os.path.isabs(json_path) else json_path

    def load(self) -> list:
        """JSON 데이터 읽기 및 절대 경로/다국어 기본값 보정"""
        if not os.path.exists(self.json_path):
            print(f"[Repository Error] JSON 파일이 존재하지 않습니다: {self.json_path}")
            return []

        try:
            with open(self.json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                categories = data.get("categories", [])

            for cat in categories:
                if "name_ja" not in cat or not cat["name_ja"]:
                    cat["name_ja"] = cat.get("name", "")

                for prod in cat.get("products", []):
                    img_rel_path = prod.get("image", "")
                    prod["image_abs_path"] = (
                        os.path.join(self.base_dir, img_rel_path) if img_rel_path else ""
                    )

                    if "name_ja" not in prod or not prod["name_ja"]:
                        prod["name_ja"] = prod.get("name", "")
                    if "price_jpy" not in prod or prod["price_jpy"] is None:
                        prod["price_jpy"] = int(prod.get("price", 0) // 10)

            return categories
        except Exception as e:
            print(f"[Repository Error] JSON 로드 실패: {e}")
            return []

    def save(self, categories: list) -> bool:
        """메모리의 카테고리/상품 데이터를 JSON으로 직렬화 및 저장"""
        save_categories = []
        for cat in categories:
            cat_copy = {
                "title": cat.get("title"),
                "name": cat.get("name"),
                "name_ja": cat.get("name_ja", cat.get("name")),
                "products": []
            }
            for prod in cat.get("products", []):
                p_copy = {
                    "id": prod.get("id"),
                    "name": prod.get("name"),
                    "name_ja": prod.get("name_ja", prod.get("name")),
                    "price": prod.get("price", 0),
                    "price_jpy": prod.get("price_jpy", int(prod.get("price", 0) // 10)),
                    "image": prod.get("image", ""),
                    "is_sold_out": prod.get("is_sold_out", False)
                }
                cat_copy["products"].append(p_copy)
            save_categories.append(cat_copy)

        try:
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump({"categories": save_categories}, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[Repository Error] JSON 저장 실패: {e}")
            return False