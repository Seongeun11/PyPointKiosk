# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'order_menu_confirm_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLineEdit,
    QPushButton, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(720, 720)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        font = QFont()
        font.setPointSize(40)
        self.lineEdit.setFont(font)
        self.lineEdit.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.lineEdit.setStyleSheet(u"background-color: transparent;")
        self.lineEdit.setFrame(False)
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lineEdit)

        self.txt_payment_list = QTextEdit(Dialog)
        self.txt_payment_list.setObjectName(u"txt_payment_list")
        font1 = QFont()
        font1.setPointSize(20)
        self.txt_payment_list.setFont(font1)
        self.txt_payment_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.verticalLayout.addWidget(self.txt_payment_list)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_order_complated = QPushButton(Dialog)
        self.btn_order_complated.setObjectName(u"btn_order_complated")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_order_complated.sizePolicy().hasHeightForWidth())
        self.btn_order_complated.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setPointSize(30)
        self.btn_order_complated.setFont(font2)

        self.horizontalLayout.addWidget(self.btn_order_complated)

        self.btn_back = QPushButton(Dialog)
        self.btn_back.setObjectName(u"btn_back")
        sizePolicy.setHeightForWidth(self.btn_back.sizePolicy().hasHeightForWidth())
        self.btn_back.setSizePolicy(sizePolicy)
        self.btn_back.setFont(font2)

        self.horizontalLayout.addWidget(self.btn_back)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.verticalLayout_2.setStretch(0, 7)
        self.verticalLayout_2.setStretch(1, 1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lineEdit.setText(QCoreApplication.translate("Dialog", u"\ucd5c\uc885 \uc8fc\ubb38\ub0b4\uc5ed\uc744 \ud655\uc778\ud569\ub2c8\ub2e4.", None))
        self.btn_order_complated.setText(QCoreApplication.translate("Dialog", u"\uc8fc\ubb38\uc644\ub8cc", None))
        self.btn_back.setText(QCoreApplication.translate("Dialog", u"\ub4a4\ub85c\uac00\uae30", None))
    # retranslateUi

