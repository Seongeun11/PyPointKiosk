#my_package\controller\payment_menu_controller.py
import os
from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QDialog
from datetime import datetime
from my_package.repositories.receipt_json_repository import ReceiptRepositoryModel
from my_package.view.discount_dialog_view import DiscountDialog
from my_package.view.amount_received_dialog_view import AmountReceivedDialog
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
            "cash_rec": "받은 현금",      # [추가] 누락되었던 키 추가
            "coupon_rec": "받은 쿠폰",    # [추가] 누락되었던 키 추가
            "change_amt": "거스름 금액",
            "pay_types": {
                "cash": "현금 결제",
                "bank": "계좌 이체",
                "point": "아카데미 포인트"
            },
            "discounts": {
                "student": "수련생 할인",
                "academy": "아카데미 할인",
                "coupon": "쿠폰 할인",
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
            "cash_rec": "お預かり(現金)",    # [추가] 누락되었던 키 추가
            "coupon_rec": "お預かり(クーポン)", # [추가] 누락되었던 키 추가
            "change_amt" : "お釣り金額",
            "pay_types": {
                "cash": "現金決済",
                "bank": "銀行振込",
                "point": "アカデミーポイント"
            },
            "discounts": {
                "student": "修練生割引",
                "academy": "アカデミー割引",
                "coupon": "クーポン割引",
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
        self.view.open_discount_dialog_signal.connect(self.handle_open_discount_dialog)
        self.view.clear_discount_signal.connect(self.handle_clear_discount)
        self.view.pay_type_requested_signal.connect(self.handle_payment)
        self.view.view_go_back_requested_signal.connect(self.handle_go_back)
        # [신규] 받은금액 버튼 시그널 연결
        if hasattr(self.view, "open_amount_received_dialog_signal"):
            self.view.open_amount_received_dialog_signal.connect(self.handle_open_amount_received_dialog)

    def init_payment_data(self, cart_items: list, total_price: int, lang_mode: str = "ko_krw"):
        """화면 진입 시 장바구니/금액/언어-통화 모드 데이터 초기화 및 UI 리프레시"""
        self.lang_mode = lang_mode.lower() if lang_mode else "ko_krw"
        currency = "JPY" if "jpy" in self.lang_mode else "KRW"
        
        self.model.set_payment_data(cart_items, total_price, currency=currency)
        self.refresh_view()

    def handle_open_discount_dialog(self, discount_type: str):
        """
        수련생/아카데미 버튼 클릭 시 상품별 지정 고정 금액 반영
        쿠폰 버튼 클릭 시 퍼센트 할인 다이얼로그 오픈
        """
        if discount_type == "coupon":
            # [수정] 쿠폰 클릭 시 퍼센트 할인 다이얼로그 오픈 로직으로 바인딩
            self.handle_open_coupon_dialog(discount_type)
        else:
            # 고정 할인 적용 (토글 가능)
            self.model.apply_fixed_discount(discount_type)
            self.refresh_view()
    
    def handle_open_coupon_dialog(self, discount_type: str):
        """
        쿠폰 퍼센트 할인 다이얼로그 호출 및 반영
        """
        is_ja = self._is_japanese()
        title = "クーポン割引設定 (%)" if is_ja else "쿠폰 퍼센트 할인 설정"

        dialog = DiscountDialog(
            title=title,
            discount_type=discount_type,
            purchase_amount=self.model.purchase_amount,
            current_discount=self.model.discount_amount,
            currency=self.model.currency,
            parent=self.view
        )

        result = dialog.exec()
        accepted_code = getattr(QDialog.DialogCode, "Accepted", 1)

        if result == accepted_code:
            applied_amount = dialog.get_discount_amount()
            self.model.set_custom_discount(discount_type, applied_amount)
            self.refresh_view()

    def handle_open_amount_received_dialog(self):
        """[신규/개편] 받은 금액 및 쿠폰 입력 다이얼로그 호출"""
        is_ja = self._is_japanese() 
        title = "預かり金・クーポン設定" if is_ja else "받은 금액 및 쿠폰 입력"

        dialog = AmountReceivedDialog(
            title=title,
            final_amount=self.model.get_final_payment_amount(),
            current_cash=self.model.cash_received,
            current_coupon=self.model.coupon_received,
            currency=self.model.currency,
            lang_mode=self.lang_mode, # [수정] lang_mode 전달
            parent=self.view
        )

        result = dialog.exec()
        accepted_code = getattr(QDialog.DialogCode, "Accepted", 1) 

        if result == accepted_code:
            cash, coupon = dialog.get_payment_values()
            self.model.set_received_amounts(cash, coupon)
            self.refresh_view()

    def handle_clear_discount(self):
        """전체 할인 취소"""
        self.model.clear_discount()
        self.refresh_view()

    def _is_japanese(self) -> bool:
        """ja_jpy 모드일 때만 True 반환"""
        return self.lang_mode == "ja_jpy"

    def _is_jpy(self) -> bool:
        """ko_jpy 또는 ja_jpy 모드일 때 True 반환"""
        if hasattr(self.model, 'currency') and self.model.currency == "JPY":
            return True
        return "jpy" in self.lang_mode

    def _get_currency_info(self) -> tuple[str, str]:
        """현재 모드에 따른 currency(코드) 및 unit(기호) 반환"""
        if self._is_jpy():
            return "JPY", "¥"
        return "KRW", "원"

    def handle_payment(self, pay_type: str):
        """
        View의 확인 다이얼로그에서 '예'를 클릭했을 때만 호출됨.
        비즈니스 로직(저장, 영수증 발행) 실행 후 완료 알림.
        """
        # 1. [신규] 받은 금액 부족 여부 검증
        if not self.model.is_payment_valid():
            shortage = self.model.get_shortage_amount()
            currency, unit = self._get_currency_info()
            
            is_ja = self._is_japanese()
            title = "金額不足" if is_ja else "금액 부족 경고"
            
            if is_ja:
                msg = f"お預かり金額が不足しています。\n不足金額: {shortage:,}{unit}"
            else:
                msg = f"받은 금액이 최종 결제 금액보다 부족합니다.\n부족한 금액: {shortage:,}{unit}\n\n금액을 확인 후 다시 시도해주세요."

            from PySide6.QtWidgets import QMessageBox
            QMessageBox.warning(self.view, title, msg)
            return  # 결제 진행 중단
        
        cart_list = getattr(self.model, 'cart_items', [])
        purchase_amt = self.model.purchase_amount
        discount_type = self.model.selected_discount_type
        discount_amt = self.model.discount_amount
        final_amt = self.model.get_final_payment_amount()

        cash_rec = self.model.cash_received
        coupon_rec = self.model.coupon_received
        change_amt = self.model.get_change_amount()

        currency, _ = self._get_currency_info()
        # 1. 영수증 뷰 텍스트 먼저 생성
        receipt_text = self.generate_receipt_text(pay_type)

        # 1. 영수증 JSON 레포지토리 저장 
        self.receipt_repo.add_receipt(
            pay_type=pay_type,
            cart_items=cart_list,
            purchase_amount=purchase_amt,
            discount_type=discount_type,
            discount_amount=discount_amt,
            final_amount=final_amt,
            currency=currency,
            cash_received=cash_rec,
            coupon_received=coupon_rec,
            change_amount=change_amt,
            receipt_text=receipt_text,  # [신규 전달]
        )

        # 2. 결제 완료 팝업 알림 (선택사항)
        #if self._is_japanese():
        #    QMessageBox.information(self.view, "完了", "決済が正常に完了しました。")
        #else:
        #    QMessageBox.information(self.view, "완료", "결제가 성공적으로 완료되었습니다.")

        # 3. 영수증 텍스트 생성 및 완료 시그널 발행
        receipt_text = self.generate_receipt_text(pay_type)
        self.payment_completed_signal.emit(receipt_text)

    def handle_go_back(self):
        """이전 화면 요청 처리"""
        self.go_back_requested_signal.emit("goback")

    def generate_receipt_text(self, pay_type: str) -> str:
        """영수증 포맷 텍스트 생성 로직"""
        lang_key = "ja" if self._is_japanese() else "ko"
        labels = self.LABELS[lang_key]
        currency, unit = self._get_currency_info()

        pay_type_str = labels["pay_types"].get(pay_type, pay_type)
        discount_type_str = labels["discounts"].get(self.model.selected_discount_type, labels["discounts"][None])
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        lines = [
            "===============================",
            labels["title"],
            "===============================",
            f" {labels['date']}: {now_str}",
            f" {labels['currency']}: {currency}",
            f" {labels['pay_type']}: {pay_type_str}",
            "--------------------------------------------",
            labels["header"],
            "--------------------------------------------"
        ]

        cart_list = getattr(self.model, 'cart_items', [])
        if isinstance(cart_list, list):
            for item in cart_list:
                name = item.get('name', 'N/A')
                qty = item.get('quantity', 0)
                price = item.get('price', 0)
                total = item.get('total_price', qty * price)
                lines.append(f" {name:<16} {qty:<6} {price:<8,} {total:<8,}")

        lines.extend([
            "--------------------------------------------",
            f" {labels['purchase_amt']}:        {self.model.purchase_amount:>10,} {unit}",
            f" {labels['discount_type']}:     {discount_type_str:>10}",
            f" {labels['discount_amt']}:     -{self.model.discount_amount:>10,} {unit}",
            "--------------------------------------------",
            f" {labels['final_amt']}:       {self.model.get_final_payment_amount():>10,} {unit}",
            f" {labels['cash_rec']}:              {self.model.cash_received:>10,} {unit}",
            f" {labels['coupon_rec']}:            {self.model.coupon_received:>10,} {unit}",
            f" {labels['change_amt']}:            {self.model.get_change_amount():>10,} {unit}",
            "===============================\n"
        ])

        return "\n".join(lines)

    def refresh_view(self):
        """현금(lb_amount_received_num)과 쿠폰(lb_received_coupon_num) 데이터를 개별 바인딩"""
        purchase_amt = self.model.purchase_amount
        discount_amt = self.model.discount_amount
        final_pay_amt = self.model.get_final_payment_amount()
        discount_type = self.model.selected_discount_type

        cash_rec = self.model.cash_received
        coupon_rec = self.model.coupon_received
        change_amt = self.model.get_change_amount()
        
        lang_key = "ja" if self._is_japanese() else "ko"
        labels = self.LABELS[lang_key]
        _, unit = self._get_currency_info()

        # 할인 브랜드명 프리픽스 정의
        prefix = f"[{labels['discounts'].get(discount_type, '')}] " if discount_type else ""

        # View 단위 갱신 호출
        self.view.update_payment_summary(
            purchase_amt=purchase_amt,
            discount_amt=discount_amt,
            final_pay_amt=final_pay_amt,
            cash_rec=cash_rec,
            coupon_rec=coupon_rec,
            change_amt=change_amt,
            prefix=prefix,
            unit=unit
        )

        self.view.update_discount_button_states(discount_type)
        is_jpy = self._is_jpy()
        is_ja = self._is_japanese()
        
        # [수정] View에 lang_mode 전달
        self.view.set_lang_mode(self.lang_mode)
        self.view.set_bank_transfer_state(is_jpy=is_jpy, is_ja=is_ja)