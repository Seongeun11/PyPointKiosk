from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PySide6.QtCore import Signal, Qt

class LoginView(QWidget):
    # 로그인 시도 이벤트를 외부(Controller/Service)로 전송하는 Signal
    login_requested = Signal(str, str)
    non_server_requested = Signal()  # 서버 연결 없이 진행 요청 Signal

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 180)
        self._init_ui()

    def _init_ui(self):
        # 전체 레이아웃 (부모 창 크기에 맞춰 유연하게 확장되도록 설정)
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # ID 입력
        self.id_label = QLabel("아이디", self)
        self.id_entry = QLineEdit(self)
        
        # 비밀번호 입력
        self.pw_label = QLabel("비밀번호", self)
        self.pw_entry = QLineEdit(self)
        self.pw_entry.setEchoMode(QLineEdit.EchoMode.Password)

        # 로그인 버튼
        self.login_btn = QPushButton("로그인", self)
        
        # 상태 표시 라벨
        self.status_label = QLabel("로그인 필요\n엔터 또는 로그인 버튼을 눌러주세요.", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 레이아웃 배치
        # 레이아웃 배치 (위젯들을 레이아웃에 순서대로 추가)
        main_layout.addStretch(1)  # 상단 여백 (중앙 정렬 효과)
        main_layout.addWidget(self.id_label)
        main_layout.addWidget(self.id_entry)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.pw_label)
        main_layout.addWidget(self.pw_entry)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.login_btn)
        main_layout.addSpacing(10)
        main_layout.addWidget(self.status_label)
        main_layout.addStretch(1)  # 하단 여백 (중앙 정렬 효과)

        # 이벤트 바인딩
        self.id_entry.returnPressed.connect(self._on_submit)
        self.pw_entry.returnPressed.connect(self._on_submit)
        self.login_btn.clicked.connect(self._on_submit)

    def _on_submit(self):
        user_id = self.id_entry.text().strip()
        user_pw = self.pw_entry.text().strip()
        # UI 동작을 처리하지 않고 백엔드로 이벤트 이관
        self.login_requested.emit(user_id, user_pw)

    def show_loading(self, message: str):
        """로딩 상태 UI 반영 (메인 스레드 안전)"""
        self.login_btn.setEnabled(False)
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color: blue;")

    def show_ready(self, message: str, color: str = "red"):
        """일반/오류 상태 UI 반영 (메인 스레드 안전)"""
        self.login_btn.setEnabled(True)
        self.status_label.setText(message)
        self.status_label.setStyleSheet(f"color: {color};")