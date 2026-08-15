#my_package\model\login_model.py
from PySide6.QtCore import QThread, Signal
from my_package.utils.auth_manager import SupabaseAuthManager, SupabaseGlobalContext

class LoginWorker(QThread):
    """
    백그라운드 스레드에서 Supabase 실제 인증을 수행하는 Worker Thread
    Qt Event Loop가 메인 스레드로 안전하게 Signal을 전달합니다.
    """
    # (is_success, status_message, text_color)
    finished = Signal(bool, str, str)

    def __init__(self, admin_id: str, pw: str, parent=None):
        super().__init__(parent)
        self.admin_id = admin_id.strip() if admin_id else ""
        self.pw = pw.strip() if pw else ""
        self.auth_manager = SupabaseAuthManager()

    def run(self):
        # 1. 입력값 기본 유효성 검사
        if not self.admin_id or not self.pw:
            self.finished.emit(False, "ID와 비밀번호를 모두 입력해주세요.", "red")
            return

        # 2. Supabase 로그인 시도
        try:
            self.auth_manager.login_and_get_client(self.admin_id, self.pw)
            client = SupabaseGlobalContext.get_client()

            if client is not None:
                self.finished.emit(True, "웹 서버 로그인을 성공했습니다.", "green")
            else:
                self.finished.emit(False, "로그인 실패: 세션 정보가 존재하지 않습니다.", "red")

        except Exception as e:
            error_msg = str(e)
            if "Invalid login credentials" in error_msg:
                ui_msg = "로그인 실패: ID 또는 비밀번호가 올바르지 않습니다."
            else:
                ui_msg = "오류 발생: 서버에 연결할 수 없습니다.\n인터넷 연결을 확인해주세요."
            
            self.finished.emit(False, ui_msg, "red")


class LoginModel:
    """
    Worker Thread 생성을 전담하는 서비스 클래스
    """
    def create_login_worker(self, admin_id: str, pw: str) -> LoginWorker:
        return LoginWorker(admin_id, pw)