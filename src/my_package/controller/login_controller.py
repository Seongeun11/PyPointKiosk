from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox
from view.login_view import LoginView
from model.login_model import LoginModel

class LoginController(QObject):
    def __init__(self, stacked_widget, on_success=None, parent=None):
        super().__init__(parent)
        # stacked_widget: QStackedWidget 인스턴스 (Tkinter의 root/pack 대체)
        self.stacked_widget = stacked_widget
        self.on_success = on_success if on_success else self._default_success_action
        
        self.login_model = LoginModel()
        self.login_view = None
        self.current_worker = None

        self.show_login_frame()

    def show_login_frame(self):
        """LoginView 생성 및 QStackedWidget에 배치"""
        self.login_view = LoginView()
        
        # UI에서 로그인 시도 Signal이 올 때 Controller 함수 호출
        self.login_view.login_requested.connect(self.handle_login_request)
  
        # QStackedWidget에 뷰 추가 및 활성화
        self.stacked_widget.addWidget(self.login_view)
        self.stacked_widget.setCurrentWidget(self.login_view)

    def handle_login_request(self, admin_id: str, pw: str):
        """UI에서 로그인 요청이 들어왔을 때 실행"""
        # UI 상태를 로딩 상태로 변경
        assert self.login_view is not None
        self.login_view.show_loading("웹 서버에 로그인을 시도합니다...")

        # 비동기 스레드 생성 및 바인딩
        self.current_worker = self.login_model.create_login_worker(admin_id, pw)
        self.current_worker.finished.connect(self._on_login_finished)
        self.current_worker.start()

    def _on_login_finished(self, is_success: bool, message: str, color: str):
        """Worker Thread 완료 Signal 수신 (Main 스레드에서 전용 실행)"""
        if is_success:
            assert self.login_view is not None
            self.login_view.show_ready(message, color)
            # 성공 콜백 실행
            if self.on_success:
                self.on_success()
        else:
            assert self.login_view is not None
            self.login_view.show_ready(message, color)

    def _default_success_action(self):
        """콜백이 없을 경우 실행되는 기본 액션"""
        QMessageBox.warning(
            self.login_view, 
            "오류", 
            "메인화면이 생성되지 않았습니다.\n확인을 누르면 프로그램이 종료됩니다."
        )
        if self.login_view and self.login_view.window():
            self.login_view.window().close()