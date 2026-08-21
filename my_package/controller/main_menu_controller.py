#my_package\controller\main_menu_controller.py
from PySide6.QtCore import QObject, Signal

from my_package.view.order_cancel_dialog_view import OrderCancelDialog
from my_package.repositories.receipt_json_repository import ReceiptRepositoryModel
class MainMenuController(QObject):
    """
    메인 메뉴 화면(MainMenuView) 전용 Controller
    """
    # Model로 시그널 전송
    start_order_requested_signal = Signal()
    # 언어 변경 요청 시 언어 코딩값(str)을 상위 Controller로 전달
    language_changed_signal = Signal(str)

    def __init__(self, model, view):
        super().__init__()
        self.model = model
        self.view = view

        self.receipt_repository = ReceiptRepositoryModel()
        
        # View 이벤트 시그널 바인딩
        self.view.start_requested.connect(self.handle_start_requested)
        self.view.language_signal.connect(self.handle_language_change)
        self.view.cancel_my_order_signal.connect(self.handle_open_cancel_order_dialog)

    def handle_start_requested(self, message: str):
        """'시작하기' 버튼 클릭 이벤트 처리"""
        # 1. Model 비즈니스 로직 실행
        self.model.on_print_message()
        
        # 2. View 업데이트 (필요한 경우)
        #self.view.title_label.setText("주문 화면으로 이동합니다...")
        
        # 3. Root Controller(MainController)에 주문 화면 전환 요청
        self.start_order_requested_signal.emit()

    def handle_language_change(self, lang: str):
        """언어 선택 버튼 클릭 이벤트 통합 처리"""
        #self.model.on_print_message()
        
        #self.p=self.model.set_text(lang)
        #print(self.p)
        self.view.update_btn_text(self.model.set_text(lang))
        print(f"[MainMenuController] 언어 변경 요청: {lang}")
        self.language_changed_signal.emit(lang)
 
    def handle_open_cancel_order_dialog(self, msg: str):
        """주문 취소 다이얼로그 호출"""
        dialog = OrderCancelDialog(self.receipt_repository, parent=self.view)
        dialog.exec()