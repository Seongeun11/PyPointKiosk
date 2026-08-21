# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'order_menu.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QLayout, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(720, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(720, 720))
        font = QFont()
        font.setPointSize(20)
        font.setBold(False)
        Form.setFont(font)
        Form.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        Form.setAutoFillBackground(False)
        self.verticalLayout_2 = QVBoxLayout(Form)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btn_title = QPushButton(Form)
        self.btn_title.setObjectName(u"btn_title")
        sizePolicy.setHeightForWidth(self.btn_title.sizePolicy().hasHeightForWidth())
        self.btn_title.setSizePolicy(sizePolicy)
        self.btn_title.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_title.setStyleSheet(u"background-color: transparent; border: none;")

        self.verticalLayout_2.addWidget(self.btn_title)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addLayout(self.gridLayout)

        self.btn_back = QPushButton(Form)
        self.btn_back.setObjectName(u"btn_back")
        sizePolicy.setHeightForWidth(self.btn_back.sizePolicy().hasHeightForWidth())
        self.btn_back.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.btn_back)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.lst_my_order_details = QListWidget(Form)
        QListWidgetItem(self.lst_my_order_details)
        self.lst_my_order_details.setObjectName(u"lst_my_order_details")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lst_my_order_details.sizePolicy().hasHeightForWidth())
        self.lst_my_order_details.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.lst_my_order_details)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.btn_all_delete = QPushButton(Form)
        self.btn_all_delete.setObjectName(u"btn_all_delete")
        sizePolicy.setHeightForWidth(self.btn_all_delete.sizePolicy().hasHeightForWidth())
        self.btn_all_delete.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.btn_all_delete)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lb_select_products = QLabel(Form)
        self.lb_select_products.setObjectName(u"lb_select_products")
        sizePolicy.setHeightForWidth(self.lb_select_products.sizePolicy().hasHeightForWidth())
        self.lb_select_products.setSizePolicy(sizePolicy)
        self.lb_select_products.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.lb_select_products)

        self.lb_total_price = QLabel(Form)
        self.lb_total_price.setObjectName(u"lb_total_price")
        sizePolicy.setHeightForWidth(self.lb_total_price.sizePolicy().hasHeightForWidth())
        self.lb_total_price.setSizePolicy(sizePolicy)
        self.lb_total_price.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout_2.addWidget(self.lb_total_price)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.btn_payment = QPushButton(Form)
        self.btn_payment.setObjectName(u"btn_payment")
        sizePolicy1.setHeightForWidth(self.btn_payment.sizePolicy().hasHeightForWidth())
        self.btn_payment.setSizePolicy(sizePolicy1)
        self.btn_payment.setMinimumSize(QSize(0, 0))
        self.btn_payment.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.btn_payment.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_payment.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.verticalLayout.addWidget(self.btn_payment)


        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(1, 2)

        self.verticalLayout_2.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_title.setText(QCoreApplication.translate("Form", u"\uc544\uce74\ub370\ubbf8 \uad00\ub9ac\uc790\uc804\uc6a9 \ud3ec\uc2a4\uae30 POS", None))
        self.btn_back.setText(QCoreApplication.translate("Form", u"\ub4a4\ub85c\uac00\uae30", None))

        __sortingEnabled = self.lst_my_order_details.isSortingEnabled()
        self.lst_my_order_details.setSortingEnabled(False)
        ___qlistwidgetitem = self.lst_my_order_details.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Form", u"1\ubc88", None))
        self.lst_my_order_details.setSortingEnabled(__sortingEnabled)

        self.btn_all_delete.setText(QCoreApplication.translate("Form", u"\uc804\uccb4\uc0ad\uc81c", None))
        self.lb_select_products.setText(QCoreApplication.translate("Form", u"0\uac1c", None))
        self.lb_total_price.setText(QCoreApplication.translate("Form", u"\ucd1d 0\uc6d0", None))
        self.btn_payment.setText(QCoreApplication.translate("Form", u"\uacb0\uc81c\ud558\uae30", None))
    # retranslateUi

