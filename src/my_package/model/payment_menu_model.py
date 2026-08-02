#src\my_package\model\payment_menu_model.py
from datetime import datetime
class PaymentMenuModel:
    """결제 금액 및 할인 로직 관리 Model"""
    def __init__(self, purchase_amount: int = 0):
        self.purchase_amount = purchase_amount  # 총 구매 금액
        self.discount_amount = 0                # 할인 금액
        self.selected_discount_type = None      # 'student', 'academy', None
        self.cart_items = []               # 장바구니 상세 정보 저장용 리스트
        
    def set_payment_data(self, cart_items: list, amount: int):
        """구매 금액 설정 및 상태 초기화"""
        self.cart_items = cart_items
        self.purchase_amount = amount
        self.discount_amount = 0
        self.selected_discount_type = None

    def toggle_discount(self, discount_type: str):
        """
        할인 적용/취소(토글) 비즈니스 로직
        - 이미 선택된 할인을 다시 누르면 할인 취소
        - 다른 할인을 누르면 해당 할인으로 변경
        """
        # 1. 이미 선택되어 있는 할인을 다시 누른 경우 -> 할인 취소 (Toggle Off)
        if self.selected_discount_type == discount_type:
            self.discount_amount = 0
            self.selected_discount_type = None
            return

        # 2. 새로운 할인 적용 (Toggle On / Switch)
        if discount_type == "student":
            # 예: 수련생 10% 할인
            self.discount_amount = int(self.purchase_amount * 0.10)
            self.selected_discount_type = "student"
            
        elif discount_type == "academy":
            # 예: 아카데미 15% 할인
            self.discount_amount = int(self.purchase_amount * 0.15)
            self.selected_discount_type = "academy"
            
        else:
            self.discount_amount = 0
            self.selected_discount_type = None

    def get_final_payment_amount(self) -> int:
        """최종 결제 금액 반환"""
        final_price = self.purchase_amount - self.discount_amount
        return max(0, final_price)

    def generate_receipt_text(self, pay_type: str) -> str:
        """영수증에 출력할 텍스트 문자열 생성 (비즈니스 로직)"""
        pay_type_names = {
            "cash": "현금 결제",
            "bank": "계좌 이체",
            "point": "아카데미 포인트"
        }
        discount_names = {
            "student": "수련생 할인 (10%)",
            "academy": "아카데미 할인 (15%)",
            None: "없음"
        }

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = [
            "============================================",
            "            [ 아카데미 키오스크 영수증 ]           ",
            "============================================",
            f" 일시: {now_str}",
            f" 결제 수단: {pay_type_names.get(pay_type, pay_type)}",
            "--------------------------------------------",
            f" {'상품명':<16} {'수량':<6} {'단가':<8} {'금액':<8}",
            "--------------------------------------------"
        ]

        for item in self.cart_items:
            name = item.get('name', '상품명 없음')
            qty = item.get('quantity', 0)
            price = item.get('price', 0)
            total = item.get('total_price', qty * price)
            lines.append(f" {name:<16} {qty:<6} {price:<8,} {total:<8,}")

        lines.extend([
            "--------------------------------------------",
            f" 주문 금액 (Purchase):        {self.purchase_amount:>10,} 원",
            f" 할인 종류 (Discount Type):   {discount_names.get(self.selected_discount_type):>10}",
            f" 할인 금액 (Discount Amt):   -{self.discount_amount:>10,} 원",
            "--------------------------------------------",
            f" 최종 결제 금액 (TOTAL):       {self.get_final_payment_amount():>10,} 원",
            "============================================"
        ])

        return "\n".join(lines)