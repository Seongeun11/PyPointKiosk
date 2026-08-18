# my_package\utils\base_scaled_manager.py

from PySide6.QtWidgets import QWidget, QDialog
from PySide6.QtGui import QResizeEvent, QFont
from PySide6.QtCore import QTimer

class BaseScaledWidget(QWidget):
    BASE_WIDTH = 720.0
    BASE_HEIGHT = 720.0
    BASE_FONT_SIZE = 24  # 기본 폰트 크기를 클래스 변수로 분리
    MIN_FONT_SIZE = 24
    MAX_FONT_SIZE = 40

    def __init__(self, parent=None):
        super().__init__(parent)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        QTimer.singleShot(0, self._apply_dynamic_font_scale)

    def _apply_dynamic_font_scale(self):
        w, h = self.width(), self.height()
        if w <= 100 or h <= 100:
            return

        scale = min(w / self.BASE_WIDTH, h / self.BASE_HEIGHT)
        # 클래스 변수를 참조하도록 수정
        base_pt = max(self.MIN_FONT_SIZE, min(int(self.BASE_FONT_SIZE * scale), self.MAX_FONT_SIZE))

        current_font = self.font()
        current_font.setPointSize(base_pt)
        self.setFont(current_font)


class BaseScaledDialog(QDialog):
    """모든 QDialog 기반 View의 동적 문자 크기 일괄 조절을 위한 공통 Base Class"""
    
    BASE_WIDTH = 820.0
    BASE_HEIGHT = 820.0
    BASE_FONT_SIZE = 12  # 기본 폰트 크기를 클래스 변수로 분리
    MIN_FONT_SIZE = 12
    MAX_FONT_SIZE = 30
    def __init__(self, parent=None):
        super().__init__(parent)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        QTimer.singleShot(0, self._apply_dynamic_font_scale)

    def _apply_dynamic_font_scale(self):
            
            w, h = self.width(), self.height()
            if w <= 100 or h <= 100:
                return
    
            scale = min(w / self.BASE_WIDTH, h / self.BASE_HEIGHT)
            # 클래스 변수를 참조하도록 수정
            base_pt = max(self.MIN_FONT_SIZE, min(int(self.BASE_FONT_SIZE * scale), self.MAX_FONT_SIZE))
    
            current_font = self.font()
            current_font.setPointSize(base_pt)
            self.setFont(current_font)

