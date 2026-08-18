#my_package\model\payment_menu_model.py
from datetime import datetime

class PaymentMenuModel:
    """결제 금액 및 할인 로직 관리 Model"""
    def __init__(self, purchase_amount: int = 0):
        self.purchase_amount = purchase_amount  # 총 구매 금액
        self.discount_amount = 0                # 할인 금액
        self.selected_discount_type = None      # 'student', 'academy', 'coupon' or None
        self.cart_items = []                   # 장바구니 상세 정보 저장용 리스트
        self.currency = "KRW"                   # 기본 통화
        self.unit = "원"                        # 기본 단위
        # [신규] 받은 금액 상태 추가 (현금/쿠폰 구분)
        self.cash_received = 0
        self.coupon_received = 0
        
    def set_payment_data(self, cart_items: list, amount: int, currency: str = "KRW"):
        """구매 금액 설정 및 통화 상태 동기화"""
        self.cart_items = cart_items
        self.purchase_amount = amount
        self.discount_amount = 0
        self.selected_discount_type = None
        self.cash_received = 0
        self.coupon_received = 0
        
        if cart_items and "currency" in cart_items[0]:
            self.currency = cart_items[0]["currency"]
        else:
            self.currency = currency

        self.unit = "¥" if self.currency == "JPY" else "원"

    def set_custom_discount(self, discount_type: str, discount_amount: int):
        """다이얼로그에서 설정된 금액 반영"""
        if discount_amount <= 0:
            self.clear_discount()
            return

        self.discount_amount = min(discount_amount, self.purchase_amount)
        self.selected_discount_type = discount_type

    def togle_discount(self, discount_type: str):
        if self.selected_discount_type == discount_type:
                    # 이미 선택된 할인을 한 번 더 누르면 토글(해제) 처리
                    self.clear_discount()
                    return
        
    def apply_fixed_discount(self, discount_type: str):
        """
        [핵심 요구사항]
        장바구니 상품별 지정된 고정 할인 금액(수련생/아카데미)의 총합을 실시간 계산해 적용
        할인액이 0원이어도 클릭 시 할인 타입 선택/해제(토글)가 동작하도록 처리
        """
        self.togle_discount(discount_type)

        total_discount = 0
        for item in self.cart_items:
            qty = item.get("quantity", 1)
            if discount_type == "student":
                disc_per_unit = item.get("discount_student", 0)
            elif discount_type == "academy":
                disc_per_unit = item.get("discount_academy", 0)
            elif discount_type == "coupon":
                            disc_per_unit = item.get("discount_coupon", 0)
            else:
                disc_per_unit = 0

            # 엔화 결제 모드 시 할인액 없음
            if self.currency == "JPY":
                disc_per_unit = 0

            total_discount += (disc_per_unit * qty)

        # 할인 금액이 구매 총액을 초과하지 않도록 캡핑
        self.discount_amount = min(total_discount, self.purchase_amount)
        # 할인액이 0원이라도 버튼 선택 상태를 유지하기 위해 할인 타입 저장
        self.selected_discount_type = discount_type

    def is_payment_valid(self) -> bool:
        """총 받은 금액(현금+쿠폰)이 최종 결제 금액 이상인지 검증"""
        return self.get_total_received() >= self.get_final_payment_amount()

    def get_shortage_amount(self) -> int:
        """부족한 금액 계산"""
        final_pay = self.get_final_payment_amount()
        total_rec = self.get_total_received()
        return max(0, final_pay - total_rec)
    
    def set_received_amounts(self, cash: int, coupon: int):
        """현금 및 쿠폰 받은 금액 설정 (한도 제한 제거)"""
        self.cash_received = max(0, cash)
        self.coupon_received = max(0, coupon)

    def get_total_received(self) -> int:
        """총 받은 금액 (현금 + 쿠폰)"""
        return self.cash_received + self.coupon_received

    def get_change_amount(self) -> int:
        """거스름돈 계산 (총 받은 금액 - 최종 결제 금액)"""
        total_rec = self.get_total_received()
        final_pay = self.get_final_payment_amount()
        return max(0, total_rec - final_pay)

    def clear_discount(self):
        """할인 상태 전체 초기화"""
        self.discount_amount = 0
        self.selected_discount_type = None
        self.cash_received = 0
        self.coupon_received = 0

    def get_final_payment_amount(self) -> int:
        """최종 결제 금액 반환"""
        final_price = self.purchase_amount - self.discount_amount
        return max(0, final_price)

    def generate_receipt_text(self, pay_type: str) -> str:
        is_jpy = (self.currency == "JPY")
        
        pay_type_names = {
            "cash": "現金決済" if is_jpy else "현금 결제",
            "bank": "銀行振込" if is_jpy else "계좌 이체",
            "point": "アカデミーポイント" if is_jpy else "아카데미 포인트"
        }
        discount_names = {
            "student": "修練生割引" if is_jpy else "수련생 할인",
            "academy": "アカデミー割引" if is_jpy else "아카데미 할인",
            "coupon": "クーポン割引" if is_jpy else "쿠폰 할인",
            None: "なし" if is_jpy else "없음"
        }

        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = [
            "============================================",
            "          [ アカデミー 注文レシート ]         " if is_jpy else "            [ 아카데미 주문 영수증 ]           ",
            "============================================",
            f" 日時: {now_str}" if is_jpy else f" 일시: {now_str}",
            f" 通貨: {self.currency}" if is_jpy else f" 통화: {self.currency}",
            f" 決済手段: {pay_type_names.get(pay_type, pay_type)}" if is_jpy else f" 결제 수단: {pay_type_names.get(pay_type, pay_type)}",
            "--------------------------------------------",
            f" {'商品名':<16} {'数量':<6} {'単価':<8} {'金額':<8}" if is_jpy else f" {'상품명':<16} {'수량':<6} {'단가':<8} {'금액':<8}",
            "--------------------------------------------"
        ]

        for item in self.cart_items:
            name = item.get('name', '상품명 없음' if not is_jpy else '商品名なし')
            qty = item.get('quantity', 0)
            price = item.get('price', 0)
            total = item.get('total_price', qty * price)
            lines.append(f" {name:<16} {qty:<6} {price:<8,} {total:<8,}")

        order_lbl = " 注文金額:" if is_jpy else " 주문 금액:"
        disc_type_lbl = " 割引種類:" if is_jpy else " 할인 종류:"
        disc_amt_lbl = " 割引金額:" if is_jpy else " 할인 금액:"
        total_lbl = " 最終決済金額:" if is_jpy else " 최종 결제 금액:"

        none_str = "なし" if is_jpy else "없음"
        disc_name_str = discount_names.get(self.selected_discount_type, none_str)

        lines.extend([
            "--------------------------------------------",
            f"{order_lbl:<20} {self.purchase_amount:>10,} {self.unit}",
            f"{disc_type_lbl:<20} {disc_name_str:>10}",
            f"{disc_amt_lbl:<20} -{self.discount_amount:>10,} {self.unit}",
            "--------------------------------------------",
            f"{total_lbl:<20} {self.get_final_payment_amount():>10,} {self.unit}",
            "============================================"
        ])

        return "\n".join(lines)

    def on_go_back(self, message: str):
        print(message)