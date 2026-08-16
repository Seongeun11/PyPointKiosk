# my_package/utils/path_utils.py
import sys
import os

def get_project_root() -> str:
    """
    개발 환경에서는 프로젝트 최상위 루트를,
    PyInstaller 빌드(EXE) 환경에서는 실행 파일(.exe)이 위치한 외부 폴더 경로를 반환합니다.
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller로 빌드된 EXE 실행 환경: executable 파일이 위치한 디렉터리
        return os.path.dirname(os.path.abspath(sys.executable))
    
    # 일반 파이썬 개발 실행 환경
    current_file = os.path.abspath(__file__)
    # my_package/utils/path_utils.py -> my_package/utils -> my_package -> 루트
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
    return project_root