# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'order_menu_fhd.ui'
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
    QLayout, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(809, 1920)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(720, 1280))
        font = QFont()
        font.setBold(False)
        Form.setFont(font)
        Form.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        Form.setAutoFillBackground(False)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_title = QLabel(Form)
        self.lbl_title.setObjectName(u"lbl_title")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lbl_title.sizePolicy().hasHeightForWidth())
        self.lbl_title.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font1.setPointSize(16)
        font1.setBold(True)
        self.lbl_title.setFont(font1)
        self.lbl_title.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.lbl_title.setAutoFillBackground(False)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_title.setWordWrap(True)

        self.verticalLayout.addWidget(self.lbl_title)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.lst_my_order_details = QListWidget(Form)
        QListWidgetItem(self.lst_my_order_details)
        self.lst_my_order_details.setObjectName(u"lst_my_order_details")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lst_my_order_details.sizePolicy().hasHeightForWidth())
        self.lst_my_order_details.setSizePolicy(sizePolicy2)
        font2 = QFont()
        font2.setPointSize(20)
        font2.setBold(False)
        self.lst_my_order_details.setFont(font2)

        self.horizontalLayout_3.addWidget(self.lst_my_order_details)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.le_time_num = QLineEdit(Form)
        self.le_time_num.setObjectName(u"le_time_num")
        sizePolicy1.setHeightForWidth(self.le_time_num.sizePolicy().hasHeightForWidth())
        self.le_time_num.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setPointSize(20)
        font3.setBold(False)
        font3.setKerning(True)
        self.le_time_num.setFont(font3)
        self.le_time_num.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.le_time_num.setMouseTracking(False)
        self.le_time_num.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.le_time_num.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.le_time_num.setAutoFillBackground(False)
        self.le_time_num.setStyleSheet(u"background-color: transparent; border: none;")
        self.le_time_num.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.le_time_num, 1, 1, 1, 2)

        self.btn_payment = QPushButton(Form)
        self.btn_payment.setObjectName(u"btn_payment")
        sizePolicy1.setHeightForWidth(self.btn_payment.sizePolicy().hasHeightForWidth())
        self.btn_payment.setSizePolicy(sizePolicy1)
        self.btn_payment.setMinimumSize(QSize(0, 150))
        self.btn_payment.setFont(font2)
        self.btn_payment.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.btn_payment.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_payment.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.gridLayout_2.addWidget(self.btn_payment, 4, 1, 1, 3)

        self.le_time_counter = QLineEdit(Form)
        self.le_time_counter.setObjectName(u"le_time_counter")
        sizePolicy1.setHeightForWidth(self.le_time_counter.sizePolicy().hasHeightForWidth())
        self.le_time_counter.setSizePolicy(sizePolicy1)
        self.le_time_counter.setFont(font3)
        self.le_time_counter.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.le_time_counter.setMouseTracking(False)
        self.le_time_counter.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.le_time_counter.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.le_time_counter.setAutoFillBackground(False)
        self.le_time_counter.setStyleSheet(u"background-color: transparent; border: none;")
        self.le_time_counter.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.le_time_counter, 0, 1, 1, 2)

        self.btn_all_delete = QPushButton(Form)
        self.btn_all_delete.setObjectName(u"btn_all_delete")
        sizePolicy.setHeightForWidth(self.btn_all_delete.sizePolicy().hasHeightForWidth())
        self.btn_all_delete.setSizePolicy(sizePolicy)
        self.btn_all_delete.setFont(font2)

        self.gridLayout_2.addWidget(self.btn_all_delete, 0, 3, 2, 1)

        self.le_total_price = QLineEdit(Form)
        self.le_total_price.setObjectName(u"le_total_price")
        sizePolicy1.setHeightForWidth(self.le_total_price.sizePolicy().hasHeightForWidth())
        self.le_total_price.setSizePolicy(sizePolicy1)
        font4 = QFont()
        font4.setPointSize(20)
        font4.setBold(False)
        font4.setUnderline(False)
        font4.setKerning(True)
        self.le_total_price.setFont(font4)
        self.le_total_price.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.le_total_price.setMouseTracking(False)
        self.le_total_price.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.le_total_price.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.le_total_price.setAutoFillBackground(False)
        self.le_total_price.setStyleSheet(u"background: transparent; border: none; border-bottom: 2px solid black; ")
        self.le_total_price.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.le_total_price, 3, 1, 1, 3)

        self.le_select_products = QLineEdit(Form)
        self.le_select_products.setObjectName(u"le_select_products")
        self.le_select_products.setFont(font2)
        self.le_select_products.setStyleSheet(u"background: transparent; border: none;")
        self.le_select_products.setCursorPosition(6)
        self.le_select_products.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.le_select_products, 2, 1, 1, 3)


        self.horizontalLayout_3.addLayout(self.gridLayout_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lbl_title.setText(QCoreApplication.translate("Form", u"\uc544\uce74\ub370\ubbf8 \ud3ec\uc778\ud2b8 \ud0a4\uc624\uc2a4\ud06c", None))

        __sortingEnabled = self.lst_my_order_details.isSortingEnabled()
        self.lst_my_order_details.setSortingEnabled(False)
        ___qlistwidgetitem = self.lst_my_order_details.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("Form", u"1\ubc88", None))
        self.lst_my_order_details.setSortingEnabled(__sortingEnabled)

        self.le_time_num.setText(QCoreApplication.translate("Form", u"0", None))
        self.btn_payment.setText(QCoreApplication.translate("Form", u"\uacb0\uc81c\ud558\uae30", None))
        self.le_time_counter.setText(QCoreApplication.translate("Form", u"\ub0a8\uc740 \uc2dc\uac04", None))
        self.btn_all_delete.setText(QCoreApplication.translate("Form", u"\uc804\uccb4\uc0ad\uc81c", None))
        self.le_total_price.setText(QCoreApplication.translate("Form", u"\uc120\ud0dd\ud55c \uc0c1\ud488", None))
        self.le_select_products.setText(QCoreApplication.translate("Form", u"\uc120\ud0dd\ud55c \uc0c1\ud488", None))
    # retranslateUi

