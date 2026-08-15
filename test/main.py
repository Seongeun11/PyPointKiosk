#src\my_package\main.py
import sys
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