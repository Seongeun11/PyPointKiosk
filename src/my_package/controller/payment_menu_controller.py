# src/my_package/controller/payment_menu_controller.py

import os
from PySide6.QtCore import QObject, Signal
from datetime import datetime
from repositories.excel_receipt_repository import ReceiptRepositoryModel

class PaymentMenuController(QObject):
    payment_completed_signal = Signal(str)
    go_back_requested_signal = Signal(str)

    # 다국어 영수증 텍스트 리소스 맵
    LABELS = {
        "ko": {
            "title": "            [ 아카데미 주문 영수증 ]           ",
            "date": "일시",
            "currency": "통화",
            "pay_type": "결제 수단",
            "header": f" {'상품명':<16} {'수량':<6} {'단가':<8} {'금액':<8}",
            "purchase_amt": "주문 금액",
            "discount_type": "할인 종류",
            "discount_amt": "할인 금액",
            "final_amt": "최종 결제 금액",
            "pay_types": {
                "cash": "현금 결제",
                "bank": "계좌 이체",
                "point": "아카데미 포인트"
            },
            "discounts": {
                "student": "수련생 할인 (10%)",
                "academy": "아카데미 할인 (15%)",
                None: "없음"
            }
        },
        "ja": {
            "title": "          [ アカデミー 注文レシート ]         ",
            "date": "日時",
            "currency": "通貨",
            "pay_type": "決済手段",
            "header": f" {'商品名':<16} {'数量':<6} {'単価':<8} {'金額':<8}",
            "purchase_amt": "注文金額",
            "discount_type": "割引種類",
            "discount_amt": "割引金額",
            "final_amt": "最終決済金額",
            "pay_types": {
                "cash": "現金決済",
                "bank": "銀行振込",
                "point": "アカデミーポイント"
            },
            "discounts": {
                "student": "修練生割引 (10%)",
                "academy": "アカデミー割引 (15%)",
                None: "なし"
            }
        }
    }

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view
        self.receipt_repo = ReceiptRepositoryModel()
        self.lang_mode = "ko_krw"

        # View 시그널 연결
        self.view.discount_requested_signal.connect(self.handle_discount)
        self.view.pay_type_requested_signal.connect(self.handle_payment)
        self.view.view_go_back_requested_signal.connect(self.handle_go_back)

    def init_payment_data(self, cart_items: list, total_price: int, lang_mode: str = "ko_krw"):
        """화면 진입 시 장바구니/금액/언어-통화 모드 데이터 초기화 및 UI 리프레시"""
        self.lang_mode = lang_mode.lower() if lang_mode else "ko_krw"
        self.model.set_payment_data(cart_items, total_price)
        self.refresh_view()

    def handle_discount(self, discount_type: str):
        """할인 선택/해제 처리"""
        self.model.toggle_discount(discount_type)
        self.refresh_view()

    def _is_japanese(self) -> bool:
        return "ja" in self.lang_mode

    def _is_jpy(self) -> bool:
        # [수정] Model에 전달된 currency 또는 lang_mode 키워드로 통화 판별
        if hasattr(self.model, 'currency') and self.model.currency == "JPY":
            return True
        return "jpy" in self.lang_mode

    def _get_currency_info(self) -> tuple[str, str]:
        """현재 모드에 따른 currency(코드) 및 unit(기호) 반환"""
        if self._is_jpy():
            return "JPY", "¥"
        return "KRW", "원"

    def handle_payment(self, pay_type: str):
        """결제 실행 -> Repository 영수증 저장 -> 영수증 텍스트 생성 후 시그널 발행"""
        cart_list = getattr(self.model, 'cart_items', [])
        purchase_amt = self.model.purchase_amount
        discount_type = self.model.selected_discount_type
        discount_amt = self.model.discount_amount
        final_amt = self.model.get_final_payment_amount()

        currency, _ = self._get_currency_info()

        # 데이터베이스/엑셀 저장을 위한 영수증 기록
        self.receipt_repo.add_receipt(
            pay_type=pay_type,
            cart_items=cart_list,
            purchase_amount=purchase_amt,
            discount_type=discount_type,
            discount_amount=discount_amt,
            final_amount=final_amt,
            currency=currency
        )

        receipt_text = self.generate_receipt_text(pay_type)
        self.payment_completed_signal.emit(receipt_text)

    def handle_go_back(self):
        """이전 화면 요청 처리"""
        self.go_back_requested_signal.emit("goback")

    def generate_receipt_text(self, pay_type: str) -> str:
        """영수증 포맷 텍스트 생성 로직 (엔화/원화 및 다국어 완벽 적용)"""
        lang_key = "ja" if self._is_japanese() else "ko"
        labels = self.LABELS[lang_key]
        currency, unit = self._get_currency_info()

        pay_type_str = labels["pay_types"].get(pay_type, pay_type)
        discount_type_str = labels["discounts"].get(self.model.selected_discount_type, labels["discounts"][None])
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = []
        lines.append("============================================")
        lines.append(labels["title"])
        lines.append("============================================")
        lines.append(f" {labels['date']}: {now_str}")
        lines.append(f" {labels['currency']}: {currency}")
        lines.append(f" {labels['pay_type']}: {pay_type_str}")
        lines.append("--------------------------------------------")
        lines.append(labels["header"])
        lines.append("--------------------------------------------")

        cart_list = getattr(self.model, 'cart_items', [])
        if isinstance(cart_list, list):
            for item in cart_list:
                name = item.get('name', 'N/A')
                qty = item.get('quantity', 0)
                price = item.get('price', 0)
                total = item.get('total_price', qty * price)
                lines.append(f" {name:<16} {qty:<6} {price:<8,} {total:<8,}")

        lines.append("--------------------------------------------")
        lines.append(f" {labels['purchase_amt']}:        {self.model.purchase_amount:>10,} {unit}")
        lines.append(f" {labels['discount_type']}:   {discount_type_str:>10}")
        lines.append(f" {labels['discount_amt']}:   -{self.model.discount_amount:>10,} {unit}")
        lines.append("--------------------------------------------")
        lines.append(f" {labels['final_amt']}:       {self.model.get_final_payment_amount():>10,} {unit}")
        lines.append("============================================\n")

        return "\n".join(lines)

    def refresh_view(self):
        """Model의 최신 상태를 View UI 라인에디터에 반영 (통화 단위 포함)"""
        purchase_amt = self.model.purchase_amount
        discount_amt = self.model.discount_amount
        final_pay_amt = self.model.get_final_payment_amount()

        _, unit = self._get_currency_info()

        # UI 요소에 엔화(¥)/원화(원) 표기 동적 업데이트
        # [수정] 단위 포맷 공백 조절 및 정확한 unit 반영
        unit_str = f" {unit}" if unit == "원" else f"{unit}"
        if unit == "¥":
            self.view.ui.le_purchase_amount_num.setText(f"¥{purchase_amt:,}")
            self.view.ui.le_discount_amount_num.setText(f"-¥{discount_amt:,}")
            self.view.ui.le_payment_amount_num.setText(f"¥{final_pay_amt:,}")
        else:
            self.view.ui.le_purchase_amount_num.setText(f"{purchase_amt:,}원")
            self.view.ui.le_discount_amount_num.setText(f"-{discount_amt:,}원")
            self.view.ui.le_payment_amount_num.setText(f"{final_pay_amt:,}원")