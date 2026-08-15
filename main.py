#src\main.py
import os
import sys

# 1. 현재 파일(main.py) 위치 기준
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. my_package 폴더 경로 지정 (구조에 맞춰 설정)
# 만약 my_package가 루트 아래 바로 있다면:
#MY_PACKAGE_DIR = os.path.join(BASE_DIR, "my_package")
# 만약 src/my_package 구조라면 아래 주석 해제하여 사용:
# MY_PACKAGE_DIR = os.path.join(BASE_DIR, "src", "my_package")

# sys.path에 루트 디렉토리와 my_package 디렉토리 모두 추가
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
#if MY_PACKAGE_DIR not in sys.path and os.path.exists(MY_PACKAGE_DIR):
#    sys.path.insert(0, MY_PACKAGE_DIR)

from PySide6.QtWidgets import QApplication, QMessageBox
from my_package.controller.main_controller import MainController

def mainapp():
    # 1. PySide6 애플리케이션 인스턴스 생성 (프로세스당 1개 필수)
    app = QApplication(sys.argv)
    
    try:
        # 2. 메인 애플리케이션 컨트롤러(QMainWindow) 생성 및 구동
        # 메인 컨트롤러 내부에서 로그인 화면 -> 메인 화면 Flow를 총괄합니다.
        main_controller = MainController()
        main_controller.show()

        # 3. Qt 이벤트 루프 실행 (Tkinter의 mainloop() 역할)
        sys.exit(app.exec())

    except Exception as e:
        # 시스템 초기화 치명적 에러 발생 시 Qt 메시지 박스로 출력
        error_msg = f"[치명적 구동 에러] 시스템 초기화 실패:\n{e}"
        print(error_msg)
        
        # app 인스턴스가 존재할 경우에만 GUI 메시지박스 노출
        if QApplication.instance():
            QMessageBox.critical(None, "에러", error_msg)
        sys.exit(1)

if __name__ == "__main__":
    mainapp()