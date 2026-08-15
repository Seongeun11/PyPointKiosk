# my_package/utils/path_utils.py
import sys
import os

def get_project_root() -> str:
    """
    프로젝트의 최상위 루트 경로(resources 폴더가 존재하는 위치)를 반환합니다.
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller 실행 환경 (sys._MEIPASS 또는 exe 위치)
        return getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    
    # 일반 파이썬 실행 환경 (path_utils.py 위치 기준 2단계 상위 폴더 = 프로젝트 루트)
    # my_package/utils/path_utils.py -> my_package/utils -> my_package -> 프로젝트 루트
    current_file = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    return project_root