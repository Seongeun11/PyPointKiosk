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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QVBoxLayout, QWidget)

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
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lb_title = QLabel(Form)
        self.lb_title.setObjectName(u"lb_title")
        self.lb_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.lb_title)

        self.lb_subtitle = QLabel(Form)
        self.lb_subtitle.setObjectName(u"lb_subtitle")
        self.lb_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_2.addWidget(self.lb_subtitle)

        self.btn_font_resize = QPushButton(Form)
        self.btn_font_resize.setObjectName(u"btn_font_resize")
        sizePolicy.setHeightForWidth(self.btn_font_resize.sizePolicy().hasHeightForWidth())
        self.btn_font_resize.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.btn_font_resize)


        self.verticalLayout.addLayout(self.verticalLayout_2)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.btn_korean_ja_cash = QPushButton(Form)
        self.btn_korean_ja_cash.setObjectName(u"btn_korean_ja_cash")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_korean_ja_cash.sizePolicy().hasHeightForWidth())
        self.btn_korean_ja_cash.setSizePolicy(sizePolicy1)
        self.btn_korean_ja_cash.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout.addWidget(self.btn_korean_ja_cash, 0, 1, 1, 1)

        self.btn_korean = QPushButton(Form)
        self.btn_korean.setObjectName(u"btn_korean")
        sizePolicy1.setHeightForWidth(self.btn_korean.sizePolicy().hasHeightForWidth())
        self.btn_korean.setSizePolicy(sizePolicy1)
        self.btn_korean.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.gridLayout.addWidget(self.btn_korean, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_cencel_my_order = QPushButton(Form)
        self.btn_cencel_my_order.setObjectName(u"btn_cencel_my_order")
        self.btn_cencel_my_order.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.btn_cencel_my_order.sizePolicy().hasHeightForWidth())
        self.btn_cencel_my_order.setSizePolicy(sizePolicy1)
        self.btn_cencel_my_order.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.btn_cencel_my_order.setCheckable(False)

        self.horizontalLayout.addWidget(self.btn_cencel_my_order)

        self.btn_start_main_menu = QPushButton(Form)
        self.btn_start_main_menu.setObjectName(u"btn_start_main_menu")
        sizePolicy1.setHeightForWidth(self.btn_start_main_menu.sizePolicy().hasHeightForWidth())
        self.btn_start_main_menu.setSizePolicy(sizePolicy1)
        self.btn_start_main_menu.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout.addWidget(self.btn_start_main_menu)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lb_title.setText(QCoreApplication.translate("Form", u"\ud658\uc601\ud569\ub2c8\ub2e4", None))
        self.lb_subtitle.setText(QCoreApplication.translate("Form", u"\uc8fc\ubb38 \uc2dc\uc791\uc744 \ub20c\ub7ec\uc8fc\uc138\uc694", None))
        self.btn_font_resize.setText(QCoreApplication.translate("Form", u"\ud3f0\ud2b8 \uc0ac\uc774\uc988 \uc870\uc808", None))
        self.btn_korean_ja_cash.setText(QCoreApplication.translate("Form", u"\ud55c\uad6d\uc5b4(\uc5d4\ud654)", None))
        self.btn_korean.setText(QCoreApplication.translate("Form", u"\ud55c\uad6d\uc5b4", None))
        self.btn_cencel_my_order.setText(QCoreApplication.translate("Form", u"\ud658\ubd88 \ubc0f \uc8fc\ubb38\ucde8\uc18c", None))
        self.btn_start_main_menu.setText(QCoreApplication.translate("Form", u"\uc8fc\ubb38 \uc2dc\uc791", None))
    # retranslateUi

