#src\my_package\controller\main_controller.py
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox

# Login Controller
from controller.login_controller import LoginController

# MainMenu MVC Components
from view.main_menu_view import MainMenuView
from model.main_menu_model import MainMenuModel
from controller.main_menu_controller import MainMenuController

# OrderMenu MVC Components
from view.order_menu_view import OrderMenuView
from model.order_menu_model import OrderMenuModel
from controller.order_menu_controller import OrderMenuController

# PaymentMenu MVC Components
from view.payment_menu_view import PaymentMenuView
from model.payment_menu_model import PaymentMenuModel
from controller.payment_menu_controller import PaymentMenuController

from view.receipt_menu_view import ReceiptMenuView
from controller.receipt_menu_controller import ReceiptMenuController

from utils.auth_manager import SupabaseGlobalContext


class MainController(QMainWindow):
    """
    애플리케이션 전체 화면 전환(Navigation) 및 
    각 MVC 모듈의 생명주기를 총괄하는 최상위 Root Controller
    """
    def __init__(self):
        super().__init__()
        self._init_window()
        self._init_views()

    def _init_window(self):
        """초기 창 설정 (로그인 화면 스펙)"""
        self.setWindowTitle("아카데미 관리자전용 포스기 - 로그인")

    def _init_views(self):
        """화면 전환용 StackedWidget 설정 및 로그인 컨트롤러 연동"""
        self.stack = QStackedWidget(self)
        self.setCentralWidget(self.stack)

        # 1. LoginController 생성 및 성공 콜백 연결
        self.login_controller = LoginController(
            stacked_widget=self.stack,
            on_success=self.on_login_succeeded
        )

    def on_login_succeeded(self):
        """로그인 성공 시 실행되는 메인 화면 전환 로직"""
        # 1. 인증 세션 검증
        supabase_client = SupabaseGlobalContext.get_client()
        if supabase_client is None:
            QMessageBox.critical(self, "오류", "인증 세션을 찾을 수 없습니다.")
            return

        # 2. 창 크기 잠금 해제 및 확장
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)
        #self.resize(1280, 720)

        # 3. 메인 메뉴 화면(MainMenu)으로 이동
        self.switch_to_main_menu()

    def switch_to_main_menu(self):
        """메인 메뉴 화면으로 전환 (Lazy Loading 적용)"""
        if not hasattr(self, 'main_menu_view'):
            self.main_menu_model = MainMenuModel()
            self.main_menu_view = MainMenuView(parent=self)
            self.main_menu_controller = MainMenuController(
                model=self.main_menu_model,
                view=self.main_menu_view
            )
            
            # [시그널 연결] '시작하기' 클릭 시 주문 메뉴로 전환
            self.main_menu_controller.start_order_requested_signal.connect(
                self.switch_to_order_menu
            )
            
            self.stack.addWidget(self.main_menu_view)

        # UI 업데이트 및 화면 전환
        self.setWindowTitle("아카데미 관리자전용 포스기 - 메인메뉴")
        self.stack.setCurrentWidget(self.main_menu_view)

    def switch_to_order_menu(self):
        if not hasattr(self, 'order_menu_view'):
            self.order_menu_model = OrderMenuModel("resources/products.json")
            self.order_menu_view = OrderMenuView(parent=self)
            self.order_menu_controller = OrderMenuController(
                model=self.order_menu_model,
                view=self.order_menu_view
            )
            
            # [핵심] pay_requested_signal (cart_items, total_price)을 switch_to_payment_menu로 전달
            self.order_menu_controller.pay_requested_signal.connect(
                self.switch_to_payment_menu
            )
            
            self.stack.addWidget(self.order_menu_view)

        self.setWindowTitle("아카데미 관리자전용 포스기 - 주문하기")
        self.stack.setCurrentWidget(self.order_menu_view)


    # [수정] 파라미터에 cart_items: list 추가!
    def switch_to_payment_menu(self, cart_items: list, total_price: int):
        """OrderMenuView에서 결제 요청 시 cart_items와 total_price를 받아 처리"""
        if total_price <= 0 or not cart_items:
            QMessageBox.warning(self, "알림", "장바구니에 담긴 상품이 없습니다.")
            return

        if not hasattr(self, 'payment_menu_view'):
            self.payment_menu_model = PaymentMenuModel()
            self.payment_menu_view = PaymentMenuView(parent=self)
            
            self.payment_menu_controller = PaymentMenuController(
                model=self.payment_menu_model,
                view=self.payment_menu_view
            )
            
            # [수정] 영수증 텍스트(receipt_text)를 파라미터로 받는 콜백 연결
            self.payment_menu_controller.payment_completed_signal.connect(
                self.on_payment_finished
            )
            
            self.stack.addWidget(self.payment_menu_view)

        # [핵심] 장바구니 목록과 총 금액을 함께 전달
        self.payment_menu_controller.init_payment_data(cart_items, total_price)

        self.setWindowTitle("아카데미 관리자전용 포스기 - 결제하기")
        self.stack.setCurrentWidget(self.payment_menu_view)
    
    def on_payment_finished(self, receipt_text: str):
        """결제 완료 후 장바구니 비우기 및 메인 메뉴(또는 주문 메뉴) 복귀"""
        #QMessageBox.information(self, "결제 완료", "결제가 성공적으로 완료되었습니다!")
        self.switch_to_receipt_menu(receipt_text)
                
        # 장바구니 초기화
        #if hasattr(self, 'order_menu_model'):
        #    self.order_menu_model.clear_cart()
        #    self.order_menu_controller.update_view()
        #    """결제 완료 시 영수증 화면(ReceiptMenuView)으로 전환"""
            
        # 메인 메뉴 화면으로 복귀
        #self.switch_to_main_menu()

    def switch_to_receipt_menu(self, receipt_text: str):
        """영수증 화면 생성 및 전환 (Lazy Loading)"""
        if not hasattr(self, 'receipt_menu_view'):
            # ReceiptModel이 별도로 필요 없다면 None으로 주입
            self.receipt_menu_view = ReceiptMenuView(parent=self)
            self.receipt_menu_controller = ReceiptMenuController(
                model=None,
                view=self.receipt_menu_view
            )
            
            # 영수증 확인 완료 시 처리 연결
            self.receipt_menu_controller.complete_requested_signal.connect(
                self.on_receipt_confirmed
            )
            
            self.stack.addWidget(self.receipt_menu_view)

        # 뷰에 영수증 텍스트 전달
        self.receipt_menu_controller.set_receipt_text(receipt_text)

        self.setWindowTitle("아카데미 관리자전용 포스기 - 결제 완료")
        self.stack.setCurrentWidget(self.receipt_menu_view)

    def on_receipt_confirmed(self):
        """영수증 확인 후 장바구니 비우기 및 메인 메뉴 복귀"""
        # 장바구니 초기화
        if hasattr(self, 'order_menu_model'):
            self.order_menu_model.clear_cart()
            self.order_menu_controller.update_view()
        
        # 메인 메뉴 화면으로 이동
        self.switch_to_main_menu()