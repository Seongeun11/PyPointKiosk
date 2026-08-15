# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'receipt_menu.ui'
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
    QTextEdit, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(720, 716)
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.le_title = QLineEdit(Form)
        self.le_title.setObjectName(u"le_title")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_title.sizePolicy().hasHeightForWidth())
        self.le_title.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(40)
        self.le_title.setFont(font)
        self.le_title.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.le_title.setStyleSheet(u"background-color: transparent;")
        self.le_title.setFrame(False)
        self.le_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.le_title)

        self.txt_payment_list = QTextEdit(Form)
        self.txt_payment_list.setObjectName(u"txt_payment_list")
        font1 = QFont()
        font1.setPointSize(20)
        self.txt_payment_list.setFont(font1)
        self.txt_payment_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout.addWidget(self.txt_payment_list)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btn_payment_completed = QPushButton(Form)
        self.btn_payment_completed.setObjectName(u"btn_payment_completed")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_payment_completed.sizePolicy().hasHeightForWidth())
        self.btn_payment_completed.setSizePolicy(sizePolicy1)
        self.btn_payment_completed.setFont(font)

        self.verticalLayout_2.addWidget(self.btn_payment_completed)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout_3.setStretch(0, 7)
        self.verticalLayout_3.setStretch(1, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.le_title.setText(QCoreApplication.translate("Form", u"\uc8fc\ubb38\uc774 \uc644\ub8cc\ub418\uc5c8\uc2b5\ub2c8\ub2e4.", None))
        self.btn_payment_completed.setText(QCoreApplication.translate("Form", u"\ucc98\uc74c\uc73c\ub85c \ub3cc\uc544\uac00\uae30", None))
    # retranslateUi

