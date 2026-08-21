# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'order_cancel_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDateEdit, QDialog, QHBoxLayout,
    QHeaderView, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QTableWidget, QTableWidgetItem, QTextEdit,
    QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(720, 720)
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_title = QLabel(Dialog)
        self.lbl_title.setObjectName(u"lbl_title")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_title.sizePolicy().hasHeightForWidth())
        self.lbl_title.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.lbl_title)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lbl_date = QLabel(Dialog)
        self.lbl_date.setObjectName(u"lbl_date")
        sizePolicy.setHeightForWidth(self.lbl_date.sizePolicy().hasHeightForWidth())
        self.lbl_date.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.lbl_date)

        self.dted_date = QDateEdit(Dialog)
        self.dted_date.setObjectName(u"dted_date")
        sizePolicy.setHeightForWidth(self.dted_date.sizePolicy().hasHeightForWidth())
        self.dted_date.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.dted_date)

        self.horizontalSpacer = QSpacerItem(80, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.horizontalLayout.setStretch(2, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.tbw_table = QTableWidget(Dialog)
        self.tbw_table.setObjectName(u"tbw_table")
        sizePolicy.setHeightForWidth(self.tbw_table.sizePolicy().hasHeightForWidth())
        self.tbw_table.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.tbw_table)

        self.txt_detail = QTextEdit(Dialog)
        self.txt_detail.setObjectName(u"txt_detail")
        sizePolicy.setHeightForWidth(self.txt_detail.sizePolicy().hasHeightForWidth())
        self.txt_detail.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.txt_detail)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btn_cancel_order = QPushButton(Dialog)
        self.btn_cancel_order.setObjectName(u"btn_cancel_order")
        sizePolicy.setHeightForWidth(self.btn_cancel_order.sizePolicy().hasHeightForWidth())
        self.btn_cancel_order.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.btn_cancel_order)

        self.btn_close = QPushButton(Dialog)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.btn_close)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.verticalLayout_2.setStretch(2, 1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lbl_title.setText(QCoreApplication.translate("Dialog", u"\ub0a0\uc9dc\ub97c \uc120\ud0dd\ud558\uace0 \uc8fc\ubb38 \ucde8\uc18c\ud560 \ub0b4\uc5ed\uc744 \uc120\ud0dd\ud558\uc138\uc694", None))
        self.lbl_date.setText(QCoreApplication.translate("Dialog", u"\uc870\ud68c \uc77c\uc790:", None))
        self.btn_cancel_order.setText(QCoreApplication.translate("Dialog", u"\uc8fc\ubb38 \ucde8\uc18c \uc801\uc6a9", None))
        self.btn_close.setText(QCoreApplication.translate("Dialog", u"\ub2eb\uae30", None))
    # retranslateUi

