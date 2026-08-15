import os
import json
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List

from my_package.utils.path_utils import get_project_root


class ReceiptRepositoryModel:
    """
    영수증 일자별 JSON 데이터 저장 및 조회 전담 Model
    """
    CLOSING_OFFSET_HOURS = 2

    def __init__(self, base_receipts_dir: str = "resources/receipts", products_path: str = "resources/products.json"):
        self.project_root = get_project_root()
        
        if os.path.isabs(base_receipts_dir):
            self.receipts_dir = base_receipts_dir
        else:
            self.receipts_dir = os.path.join(self.project_root, base_receipts_dir)

        if os.path.isabs(products_path):
            self.products_path = products_path
        else:
            self.products_path = os.path.join(self.project_root, products_path)

        os.makedirs(self.receipts_dir, exist_ok=True)

    def get_business_date_str(self, dt: Optional[datetime] = None) -> str:
        if dt is None:
            dt = datetime.now()
        business_dt = dt - timedelta(hours=self.CLOSING_OFFSET_HOURS)
        return business_dt.strftime("%Y-%m-%d")

    def _get_daily_file_path(self, date_str: Optional[str] = None) -> str:
        if not date_str:
            date_str = self.get_business_date_str()
        filename = f"receipts_{date_str}.json"
        return os.path.join(self.receipts_dir, filename)

    def _load_receipts_by_path(self, file_path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(file_path):
            return []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Model Error] 영수증 파일 읽기 실패 ({file_path}): {e}")
            return []

    def add_receipt(self, pay_type: str, cart_items: list, purchase_amount: int, 
                    discount_type: str, discount_amount: int, final_amount: int,
                    currency: str = "KRW") -> dict:
        now = datetime.now()
        business_date_str = self.get_business_date_str(now)
        daily_file_path = self._get_daily_file_path(business_date_str)

        receipts = self._load_receipts_by_path(daily_file_path)
        next_id = (len(receipts) % 999) + 1

        receipt_data = {
            "id": next_id,
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "pay_type": pay_type,                     
            "discount_type": discount_type,           
            "currency": currency,
            "purchase_amount": purchase_amount,
            "discount_amount": discount_amount,       
            "final_amount": final_amount,             
            "items": cart_items                       
        }

        receipts.append(receipt_data)

        try:
            with open(daily_file_path, "w", encoding="utf-8") as f:
                json.dump(receipts, f, ensure_ascii=False, indent=2)
                print(f"[Model] 영수증 저장 완료 (통화: {currency}, 영업일: {business_date_str}): {daily_file_path}")
        except Exception as e:
            print(f"[Model Error] 영수증 저장 실패: {e}")

        return receipt_data

    def get_receipts_by_date(self, date_str: Optional[str] = None) -> list:
        file_path = self._get_daily_file_path(date_str)
        return self._load_receipts_by_path(file_path)