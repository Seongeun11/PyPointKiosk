#src\my_package\controller\payment_menu_controller.py
from PySide6.QtCore import QObject, Signal
from datetime import datetime
from model.receipt_repository_model import ReceiptRepositoryModel

class PaymentMenuController(QObject):
    payment_completed_signal = Signal(str) # 결제 완료 시 상위 컨트롤러 알림

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.receipt_repo = ReceiptRepositoryModel() # [추가] 영수증 저장소 모델

        # View 시그널 연결
        self.view.discount_requested.connect(self.handle_discount)
        self.view.pay_type_requested.connect(self.handle_payment)

    def init_payment_data(self, cart_items: list, total_price: int):
        """화면 진입 시 장바구니/금액 데이터 초기화 및 UI 리프레시"""
        self.model.set_payment_data(cart_items, total_price)
        self.refresh_view()

    def handle_discount(self, discount_type: str):
        """할인 버튼 클릭 이벤트 처리 (토글 적용)"""
        self.model.toggle_discount(discount_type)
        self.refresh_view()

    def handle_payment(self, pay_type: str):

        """결제 실행 -> JSON 영수증 저장 -> 영수증 텍스트 생성 후 전환"""
        cart_list = getattr(self.model, 'cart_items', [])
        purchase_amt = self.model.purchase_amount
        discount_type = self.model.selected_discount_type
        discount_amt = self.model.discount_amount
        final_amt = self.model.get_final_payment_amount()

        # [핵심] JSON 배열(1~999)에 영수증 데이터 기록
        self.receipt_repo.add_receipt(
            pay_type=pay_type,
            cart_items=cart_list,
            purchase_amount=purchase_amt,
            discount_type=discount_type,
            discount_amount=discount_amt,
            final_amount=final_amt
        )

        receipt_text = self.generate_receipt_text(pay_type)
        self.payment_completed_signal.emit(receipt_text)

    def generate_receipt_text(self, pay_type: str) -> str:
        """영수증 포맷 텍스트 생성 로직"""
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
        
        lines = []
        lines.append("============================================")
        lines.append("            [ 아카데미 주문 영수증 ]           ")
        lines.append("============================================")
        lines.append(f" 일시: {now_str}")
        lines.append(f" 결제 수단: {pay_type_names.get(pay_type, pay_type)}")
        lines.append("--------------------------------------------")
        lines.append(f" {'상품명':<16} {'수량':<6} {'단가':<8} {'금액':<8}")
        lines.append("--------------------------------------------")

        cart_list = getattr(self.model, 'cart_items', [])
        if isinstance(cart_list, list):
            for item in cart_list:
                name = item.get('name', '상품명 없음')
                qty = item.get('quantity', 0)
                price = item.get('price', 0)
                total = item.get('total_price', qty * price)
                lines.append(f" {name:<16} {qty:<6} {price:<8,} {total:<8,}")

        lines.append("--------------------------------------------")
        lines.append(f" 주문 금액 (Purchase):        {self.model.purchase_amount:>10,} 원")
        lines.append(f" 할인 종류 (Discount Type):   {discount_names.get(self.model.selected_discount_type):>10}")
        lines.append(f" 할인 금액 (Discount Amt):   -{self.model.discount_amount:>10,} 원")
        lines.append("--------------------------------------------")
        lines.append(f" 최종 결제 금액 (TOTAL):       {self.model.get_final_payment_amount():>10,} 원")
        lines.append("============================================\n")

        return "\n".join(lines)

    def refresh_view(self):
        """Model의 최신 상태를 View에 반영"""
        purchase_amt = self.model.purchase_amount
        discount_amt = self.model.discount_amount if hasattr(self, 'discount_amount') else self.model.discount_amount
        final_pay_amt = self.model.get_final_payment_amount()
        
        self.view.update_amounts(purchase_amt, discount_amt, final_pay_amt)