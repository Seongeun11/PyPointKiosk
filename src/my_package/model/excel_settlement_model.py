#src\my_package\model\excel_settlement_model.py
from typing import List, Dict, Any

class SettlementModel:
    """일일 정산 데이터 집계 및 저장 관리 Model"""
    def __init__(self):
        # 완료된 주문 건 저장소 (DB 연동 시 DB Query로 대체)
        self.completed_orders: List[Dict[str, Any]] = []
        self.point_history: List[Dict[str, Any]] = []

    def record_order(self, cart_items: List[Dict[str, Any]], discount_type: str, pay_type: str, user_info: Dict[str, Any]):
        """결제 완료 시 주문 내역 기록"""
        for item in cart_items:
            self.completed_orders.append({
                "name": item.get("name"),
                "quantity": item.get("quantity", 1),
                "discount_type": discount_type,
                "pay_type": pay_type
            })

        if pay_type == "point" and user_info:
            self.point_history.append({
                "name": user_info.get("name", ""),
                "generation": user_info.get("generation", ""),
                "point": user_info.get("used_point", 0),
                "memo": ", ".join([str(i.get("name")) for i in cart_items if i.get("name") is not None])
            })

    def get_daily_sales_summary(self) -> List[Dict[str, Any]]:
        return self.completed_orders

    def get_point_history(self) -> List[Dict[str, Any]]:
        return self.point_history