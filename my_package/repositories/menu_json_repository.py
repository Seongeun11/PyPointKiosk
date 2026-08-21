#my_package\repositories\menu_json_repository.py
import json
import os
from my_package.utils.path_utils import get_project_root

class MenuJsonRepository:
    """JSON 파일 Persistence I/O 관리 담당 계층"""

    def __init__(self, _base_dir: str, _json_path: str):
        # 프로젝트 전체 최상위 루트 경로 획득
        self.project_root = get_project_root()
        self.base_dir = _base_dir if _base_dir else self.project_root

        # 1. 전달받은 경로 조합
        if os.path.isabs(_json_path):
            candidate_path = _json_path
        else:
            candidate_path = os.path.abspath(os.path.join(self.base_dir, _json_path))

        # 2. 만약 해당 경로에 파일이 존재하지 않는다면, 최상위 project_root 기준으로 탐색
        if not os.path.exists(candidate_path):
            # 'my_package/resources/...' 처럼 붙은 경우를 대비해 순수 파일명/상대 경로 보정
            clean_rel_path = _json_path.replace("my_package/", "").replace("my_package\\", "")
            root_candidate = os.path.abspath(os.path.join(self.project_root, clean_rel_path))
            
            if os.path.exists(root_candidate):
                self.json_path = root_candidate
            else:
                self.json_path = candidate_path
        else:
            self.json_path = candidate_path
            
    def load(self) -> list:
        """JSON 데이터 읽기 및 할인 필드 기본값 보정"""
        if not os.path.exists(self.json_path):
            print(f"[Repository Error] JSON 파일이 존재하지 않습니다: {self.json_path}")
            os.makedirs(os.path.dirname(self.json_path), exist_ok=True)
            print(f"[Repository Info] JSON 파일 경로 생성: {os.path.dirname(self.json_path)}")
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
                    # 이미지 경로 탐색 보정 (프로젝트 루트 기준)
                    if img_rel_path:
                        if os.path.isabs(img_rel_path):
                            prod["image_abs_path"] = img_rel_path
                        else:
                            # 1순위: project_root 기준 탐색
                            img_abs = os.path.normpath(os.path.join(self.project_root, img_rel_path))
                            if not os.path.exists(img_abs):
                                # 2순위: base_dir 기준 탐색
                                img_abs = os.path.normpath(os.path.join(self.base_dir, img_rel_path))
                            prod["image_abs_path"] = img_abs
                    else:
                        prod["image_abs_path"] = ""

                    if "name_ja" not in prod or not prod["name_ja"]:
                        prod["name_ja"] = prod.get("name", "")
                    if "price_jpy" not in prod or prod["price_jpy"] is None:
                        prod["price_jpy"] = int(prod.get("price", 0) // 10)
                        
                    # [신규] 할인 금액 기본값 보정
                    if "discount_student" not in prod:
                        prod["discount_student"] = 0
                    if "discount_academy" not in prod:
                        prod["discount_academy"] = 0

            return categories
        except Exception as e:
            print(f"[Repository Error] JSON 로드 실패: {e}")
            return []

    def save(self, categories: list) -> bool:
        """메모리의 카테고리/상품 데이터를 JSON으로 저장 (할인 금액 추가)"""
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
                    "discount_student": prod.get("discount_student", 0), # [신규] 수련생 고정 할인
                    "discount_academy": prod.get("discount_academy", 0), # [신규] 아카데미 고정 할인
                    "discount_jpy": prod.get("discount_jpy", 0), # [신규] 엔화 고정 할인
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