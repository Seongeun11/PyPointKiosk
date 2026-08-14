#src\my_package\utils\image_manager.py
import os
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor
from PySide6.QtCore import Qt

class ImageManager:
    """이미지 경로 처리, 플레이스홀더 생성 및 QIcon 변환을 전담하는 클래스"""

    @staticmethod
    def get_absolute_image_path(base_dir: str, rel_image_path: str) -> str:
        """상대 이미지 경로를 절대 경로로 안전하게 변환"""
        if not rel_image_path:
            return ""
        if os.path.isabs(rel_image_path):
            return rel_image_path
        return os.path.join(base_dir, rel_image_path)

    @staticmethod
    def create_placeholder_icon(width: int = 120, height: int = 120, text: str = "No Image") -> QIcon:
        """이미지가 없거나 유효하지 않을 때 사용할 플레이스홀더 아이콘 생성"""
        pixmap = QPixmap(width, height)
        pixmap.fill(QColor("#E0E0E0"))
        painter = QPainter(pixmap)
        painter.setPen(QColor("#888888"))
        painter.drawText(
            pixmap.rect(), Qt.AlignmentFlag.AlignCenter, text
        )
        painter.end()
        return QIcon(pixmap)

    @classmethod
    def get_product_icon(cls, abs_image_path: str, width: int = 120, height: int = 120) -> QIcon:
        """파일 존재 여부를 확인하고 아이콘(또는 플레이스홀더) 반환"""
        if abs_image_path and os.path.exists(abs_image_path):
            return QIcon(abs_image_path)
        return cls.create_placeholder_icon(width, height)