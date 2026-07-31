#src\my_package\controller\main_controller.py
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from controller.login_controller import LoginController

from view.main_view import MainView
from view.order_menu_view import OrderMenuView
from model.main_model import MainModel
from utils.auth_manager import SupabaseGlobalContext

class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_model = MainModel()
        self._init_window()
        self._init_views()

    def _init_window(self):
        """초기 창 설정 (로그인 화면 스펙)"""
        self.setWindowTitle("아카데미 결제 키오스크 - 로그인")
        #self.resize(400, 300)
        #self.setFixedSize(400, 300) # 로그인 시에는 크기 고정

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
        """[기존 succeeded 콜백 대체] 로그인 성공 시 실행되는 메인 화면 전환 로직"""
        # 1. 인증 세션 검증
        supabase_client = SupabaseGlobalContext.get_client()
        if supabase_client is None:
            QMessageBox.critical(self, "오류", "인증 세션을 찾을 수 없습니다.")
            return

        # 2. 창 크기 잠금 해제 및 확장 (Tkinter의 root.resizable / geometry 대체)
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215) # QWidget 최대 크기 해제
        self.resize(1280, 720)
        self.setWindowTitle("아카데미 결제 키오스크 - 메인메뉴")

        # 3. MainView 생성 및 화면 스택 전환
        self.main_view = MainView(parent=self)

        # [화면 전환 이벤트 연결] 
        # 버튼 클릭 시 Model 메시지 출력 + OrderMenuView로 전환 처리
        self.main_view.start_requested.connect(self.main_model.on_print_message)
        self.main_view.start_requested.connect(self.switch_to_order_menu)


        # 2. [주요 연결 포인트] View Signal -> Service Method 연결
        self.main_view.start_requested.connect(self.main_model.on_print_message)
        
        # (옵션) Controller 내부 UI 반응 로직도 별도 slot 연결 가능
        self.main_view.start_requested.connect(self.handle_ui_update)
        self.stack.addWidget(self.main_view)
        self.stack.setCurrentWidget(self.main_view)

    def handle_ui_update(self, message: str):
        """UI 타이틀 텍스트 변경이 필요한 경우 처리"""
        if hasattr(self, 'main_view'):
            self.main_view.title_label.setText(message)

    def switch_to_order_menu(self, message: str):
        """MainView에서 '시작하기' 클릭 시 주문 메뉴 화면으로 전환"""
        if not hasattr(self, 'order_menu_view'):
            self.order_menu_view = OrderMenuView(parent=self)
            self.stack.addWidget(self.order_menu_view)
        
        self.setWindowTitle("아카데미 결제 키오스크 - 주문하기")
        self.stack.setCurrentWidget(self.order_menu_view)