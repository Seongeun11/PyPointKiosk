#src\my_package\model\payment_menu_model.py
from datetime import datetime
class PaymentMenuModel:
    """결제 금액 및 할인 로직 관리 Model"""
    def __init__(self, purchase_amount: int = 0):
        self.purchase_amount = purchase_amount  # 총 구매 금액
        self.discount_amount = 0                # 할인 금액
        self.selected_discount_type = None      # 'student', 'academy', None
        self.cart_items = []                   # 장바구니 상세 정보 저장용 리스트
        self.currency = "KRW"                   # 기본 통화 [추가]
        self.unit = "원"                        # 기본 단위 [추가]
        
    def set_payment_data(self, cart_items: list, amount: int, currency: str = "KRW"):
        """구매 금액 설정 및 통화 상태 동기화"""
        self.cart_items = cart_items
        self.purchase_amount = amount
        self.discount_amount = 0
        self.selected_discount_type = None
        
        # [수정] cart_items 기반 통화 정보 및 단위 설정
        if cart_items and "currency" in cart_items[0]:
            self.currency = cart_items[0]["currency"]
        else:
            self.currency = currency

        self.unit = "¥" if self.currency == "JPY" else "원"

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
        pay_type_names = {
            "cash": "現金決済" if self.currency == "JPY" else "현금 결제",
            "bank": "銀行振込" if self.currency == "JPY" else "계좌 이체",
            "point": "アカデミーポイント" if self.currency == "JPY" else "아카데미 포인트"
        }
        discount_names = {
            "student": "修練生割引 (10%)" if self.currency == "JPY" else "수련생 할인 (10%)",
            "academy": "アカデミー割引 (15%)" if self.currency == "JPY" else "아카데미 할인 (15%)",
            None: "なし" if self.currency == "JPY" else "없음"
        }

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = [
            "============================================",
            "          [ アカデミー 注文レシート ]         " if self.currency == "JPY" else "            [ 아카데미 주문 영수증 ]           ",
            "============================================",
            f" 日時: {now_str}" if self.currency == "JPY" else f" 일시: {now_str}",
            f" 通貨: {self.currency}" if self.currency == "JPY" else f" 통화: {self.currency}",
            f" 決済手段: {pay_type_names.get(pay_type, pay_type)}" if self.currency == "JPY" else f" 결제 수단: {pay_type_names.get(pay_type, pay_type)}",
            "--------------------------------------------",
            f" {'商品名':<16} {'数量':<6} {'単価':<8} {'金額':<8}" if self.currency == "JPY" else f" {'상품명':<16} {'수량':<6} {'단가':<8} {'금액':<8}",
            "--------------------------------------------"
        ]

        for item in self.cart_items:
            name = item.get('name', '상품명 없음')
            qty = item.get('quantity', 0)
            price = item.get('price', 0)
            total = item.get('total_price', qty * price)
            lines.append(f" {name:<16} {qty:<6} {price:<8,} {total:<8,}")

        # [수정] 하드코딩된 '원' 제거 및 self.unit 적용
        order_lbl = " 注文金額:" if self.currency == "JPY" else " 주문 금액 (Purchase):"
        disc_type_lbl = " 割引種類:" if self.currency == "JPY" else " 할인 종류 (Discount Type):"
        disc_amt_lbl = " 割引金額:" if self.currency == "JPY" else " 할인 금액 (Discount Amt):"
        total_lbl = " 最終決済金額:" if self.currency == "JPY" else " 최종 결제 금액 (TOTAL):"

        lines.extend([
            "--------------------------------------------",
            f"{order_lbl:<20} {self.purchase_amount:>10,} {self.unit}",
            f"{disc_type_lbl:<20} {discount_names.get(self.selected_discount_type):>10}",
            f"{disc_amt_lbl:<20} -{self.discount_amount:>10,} {self.unit}",
            "--------------------------------------------",
            f"{total_lbl:<20} {self.get_final_payment_amount():>10,} {self.unit}",
            "============================================"
        ])

        return "\n".join(lines)

    def on_go_back(self,message:str):

        print(message)