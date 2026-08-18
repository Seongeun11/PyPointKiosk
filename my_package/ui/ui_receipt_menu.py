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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
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
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.label)

        self.txt_payment_list = QTextEdit(Form)
        self.txt_payment_list.setObjectName(u"txt_payment_list")
        self.txt_payment_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout.addWidget(self.txt_payment_list)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btn_payment_completed = QPushButton(Form)
        self.btn_payment_completed.setObjectName(u"btn_payment_completed")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_payment_completed.sizePolicy().hasHeightForWidth())
        self.btn_payment_completed.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.btn_payment_completed)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout_3.setStretch(0, 7)
        self.verticalLayout_3.setStretch(1, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\uc8fc\ubb38\uc774 \uc644\ub8cc\ub418\uc5c8\uc2b5\ub2c8\ub2e4.", None))
        self.btn_payment_completed.setText(QCoreApplication.translate("Form", u"\ucc98\uc74c\uc73c\ub85c \ub3cc\uc544\uac00\uae30", None))
    # retranslateUi

