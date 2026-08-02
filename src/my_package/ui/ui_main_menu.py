# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_menu.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLineEdit, QPushButton, QSizePolicy,
    QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(720, 1280)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(720, 1280))
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.le_title = QLineEdit(Form)
        self.le_title.setObjectName(u"le_title")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.le_title.sizePolicy().hasHeightForWidth())
        self.le_title.setSizePolicy(sizePolicy1)
        font = QFont()
        font.setPointSize(40)
        self.le_title.setFont(font)
        self.le_title.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.le_title.setStyleSheet(u"background-color: transparent;")
        self.le_title.setFrame(False)
        self.le_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.le_title)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.le_sub_title = QLineEdit(Form)
        self.le_sub_title.setObjectName(u"le_sub_title")
        font1 = QFont()
        font1.setPointSize(20)
        self.le_sub_title.setFont(font1)
        self.le_sub_title.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.le_sub_title.setStyleSheet(u"background-color: transparent;")
        self.le_sub_title.setFrame(False)
        self.le_sub_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_3.addWidget(self.le_sub_title)


        self.verticalLayout.addLayout(self.verticalLayout_3)

        self.btn_start_main_menu = QPushButton(Form)
        self.btn_start_main_menu.setObjectName(u"btn_start_main_menu")
        sizePolicy.setHeightForWidth(self.btn_start_main_menu.sizePolicy().hasHeightForWidth())
        self.btn_start_main_menu.setSizePolicy(sizePolicy)
        self.btn_start_main_menu.setFont(font1)
        self.btn_start_main_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout.addWidget(self.btn_start_main_menu)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.le_title.setText(QCoreApplication.translate("Form", u"\ud658\uc601\ud569\ub2c8\ub2e4", None))
        self.le_sub_title.setText(QCoreApplication.translate("Form", u"\uc8fc\ubb38 \uc2dc\uc791\uc744 \ub20c\ub7ec\uc8fc\uc138\uc694", None))
        self.btn_start_main_menu.setText(QCoreApplication.translate("Form", u"\uc8fc\ubb38 \uc2dc\uc791", None))
    # retranslateUi

