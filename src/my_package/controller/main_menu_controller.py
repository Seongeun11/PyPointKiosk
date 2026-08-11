#src\my_package\controller\main_menu_controller.py
from PySide6.QtCore import QObject, Signal

class MainMenuController(QObject):
    """
    메인 메뉴 화면(MainMenuView) 전용 Controller
    """
    # Model로 시그널 전송
    start_order_requested_signal = Signal()
    on_ko_set_language_signal = Signal()
    on_jp_set_language_signal = Signal()
    on_en_set_language_signal = Signal()
    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        # View의 이벤트 시그널 바인딩
        self.view.start_requested.connect(self.handle_start_requested)


    def handle_start_requested(self, message: str):
        """'시작하기' 버튼 클릭 이벤트 처리"""
        # 1. Model 비즈니스 로직 실행
        self.model.on_print_message()
        
        # 2. View 업데이트 (필요한 경우)
        #self.view.title_label.setText("주문 화면으로 이동합니다...")
        
        # 3. Root Controller(MainController)에 주문 화면 전환 요청
        self.start_order_requested_signal.emit()

    def on_english_button_clicked(self, message: str):
            """ 영어 버튼 클릭 이벤트 처리"""
            # 1. Model 비즈니스 로직 실행
            self.model.on_print_message()
            
            self.on_en_set_language_signal.emit()

    def on_japan_button_clicked(self, message: str):
        """ 일본어 버튼 클릭 이벤트 처리"""
        # 1. Model 비즈니스 로직 실행
        self.model.on_print_message()
        
        self.on_jp_set_language_signal.emit()

    def on_ko_button_clicked(self, message: str):
        """ 한국어 버튼 클릭 이벤트 처리"""
        # 1. Model 비즈니스 로직 실행
        self.model.on_print_message()
        
        self.on_ko_set_language_signal.emit()