#src\my_package\utils\image_manager.py
import os
import shutil
from typing import Optional
from PySide6.QtGui import QPixmap, QPainter, QColor, QFont
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon                                                                                                                                         
class ImageManager:
    """이미지 경로 처리, 플레이스홀더 생성 및 QIcon 변환 전담 클래스"""

    @staticmethod                                                                                            
    def get_absolute_image_path(base_dir: str, rel_image_path: str) -> str:
        if not rel_image_path:
            return ""
        if os.path.isabs(rel_image_path):                                                                   
            return rel_image_path
        return os.path.join(base_dir, rel_image_path)

    @staticmethod
    def create_placeholder_icon(width: int = 120, height: int = 120, text: str = "No Image") -> QIcon:
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
        """
        파일 존재 여부를 확인하고 아이콘 반환
        - 지정된 파일이 없으면 기본 이미지(default.png) 탐색 후 플레이스홀더 반환
        """
        if abs_image_path and os.path.exists(abs_image_path):
            return QIcon(abs_image_path)
            
        # [추가] 기본 이미지 파일(default.png) 체크
        if abs_image_path:
            default_img_path = os.path.join(os.path.dirname(abs_image_path), "default.png")
            if os.path.exists(default_img_path):
                return QIcon(default_img_path)

        return cls.create_placeholder_icon(width, height)
    @staticmethod
    def ensure_default_sample_image(target_abs_path: str, prod_name: str = "") -> None:
        """
        target_abs_path 위치에 이미지 파일 생성:
        1. resources/images/default.png 가 있다면 이를 복사
        2. 없다면 'SAMPLE' 텍스트가 적힌 예시 PNG 이미지를 직접 생성하여 저장
        """
        os.makedirs(os.path.dirname(target_abs_path), exist_ok=True)
        
        # 1. default.png 원본이 있으면 복사
        base_dir = os.path.dirname(target_abs_path)
        default_template = os.path.join(base_dir, "default.png")
        
        if os.path.exists(default_template):
            shutil.copy(default_template, target_abs_path)
            print(f"[ImageManager] default.png 복사 완료: {target_abs_path}")
            return

        # 2. default.png도 없으면 예시 이미지 플레이스홀더 파일 자동 생성
        pixmap = QPixmap(200, 200)
        pixmap.fill(QColor("#F0F0F0"))
        
        painter = QPainter(pixmap)
        painter.setPen(QColor("#CCCCCC"))
        painter.drawRect(0, 0, 199, 199)
        painter.setPen(QColor("#555555"))
        painter.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        display_text = f"SAMPLE\n({prod_name})" if prod_name else "SAMPLE\n(No Image)"
        painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, display_text)
        painter.end()

        pixmap.save(target_abs_path, "PNG")
        print(f"[ImageManager] 기본 예시 샘플 이미지 자동 생성: {target_abs_path}")