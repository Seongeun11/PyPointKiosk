# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'payment_menu.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QPushButton, QSizePolicy, QVBoxLayout,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(720, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(720, 720))
        font = QFont()
        font.setPointSize(20)
        Form.setFont(font)
        Form.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(Form)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lb_select_discount = QLabel(Form)
        self.lb_select_discount.setObjectName(u"lb_select_discount")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.lb_select_discount.sizePolicy().hasHeightForWidth())
        self.lb_select_discount.setSizePolicy(sizePolicy1)
        self.lb_select_discount.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout.addWidget(self.lb_select_discount)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_student_discount = QPushButton(Form)
        self.btn_student_discount.setObjectName(u"btn_student_discount")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_student_discount.sizePolicy().hasHeightForWidth())
        self.btn_student_discount.setSizePolicy(sizePolicy2)

        self.horizontalLayout.addWidget(self.btn_student_discount)

        self.btn_academy_discount = QPushButton(Form)
        self.btn_academy_discount.setObjectName(u"btn_academy_discount")
        sizePolicy2.setHeightForWidth(self.btn_academy_discount.sizePolicy().hasHeightForWidth())
        self.btn_academy_discount.setSizePolicy(sizePolicy2)
        self.btn_academy_discount.setAutoFillBackground(False)

        self.horizontalLayout.addWidget(self.btn_academy_discount)

        self.btn_coupon_discount = QPushButton(Form)
        self.btn_coupon_discount.setObjectName(u"btn_coupon_discount")
        self.btn_coupon_discount.setEnabled(True)
        sizePolicy.setHeightForWidth(self.btn_coupon_discount.sizePolicy().hasHeightForWidth())
        self.btn_coupon_discount.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.btn_coupon_discount)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.verticalLayout_3.addLayout(self.verticalLayout)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_cash_payment = QPushButton(Form)
        self.btn_cash_payment.setObjectName(u"btn_cash_payment")
        sizePolicy2.setHeightForWidth(self.btn_cash_payment.sizePolicy().hasHeightForWidth())
        self.btn_cash_payment.setSizePolicy(sizePolicy2)

        self.gridLayout_3.addWidget(self.btn_cash_payment, 2, 0, 1, 1)

        self.btn_bank_transfer_payment = QPushButton(Form)
        self.btn_bank_transfer_payment.setObjectName(u"btn_bank_transfer_payment")
        sizePolicy.setHeightForWidth(self.btn_bank_transfer_payment.sizePolicy().hasHeightForWidth())
        self.btn_bank_transfer_payment.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.btn_bank_transfer_payment, 2, 1, 1, 1)

        self.btn_academy_point_payment = QPushButton(Form)
        self.btn_academy_point_payment.setObjectName(u"btn_academy_point_payment")
        sizePolicy.setHeightForWidth(self.btn_academy_point_payment.sizePolicy().hasHeightForWidth())
        self.btn_academy_point_payment.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.btn_academy_point_payment, 2, 2, 1, 1)

        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label, 0, 0, 1, 3)

        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.label_2, 1, 0, 1, 3)


        self.verticalLayout_3.addLayout(self.gridLayout_3)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.lb_payment_amount = QLabel(Form)
        self.lb_payment_amount.setObjectName(u"lb_payment_amount")
        sizePolicy.setHeightForWidth(self.lb_payment_amount.sizePolicy().hasHeightForWidth())
        self.lb_payment_amount.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.lb_payment_amount, 5, 0, 2, 1)

        self.lb_remaining_amount_num = QLabel(Form)
        self.lb_remaining_amount_num.setObjectName(u"lb_remaining_amount_num")
        sizePolicy.setHeightForWidth(self.lb_remaining_amount_num.sizePolicy().hasHeightForWidth())
        self.lb_remaining_amount_num.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.lb_remaining_amount_num, 11, 1, 2, 1)

        self.btn_amount_received = QPushButton(Form)
        self.btn_amount_received.setObjectName(u"btn_amount_received")
        sizePolicy.setHeightForWidth(self.btn_amount_received.sizePolicy().hasHeightForWidth())
        self.btn_amount_received.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.btn_amount_received, 8, 2, 5, 1)

        self.lb_purchase_amount = QLabel(Form)
        self.lb_purchase_amount.setObjectName(u"lb_purchase_amount")
        sizePolicy.setHeightForWidth(self.lb_purchase_amount.sizePolicy().hasHeightForWidth())
        self.lb_purchase_amount.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.lb_purchase_amount, 2, 0, 2, 1)

        self.btn_all_clear_discount = QPushButton(Form)
        self.btn_all_clear_discount.setObjectName(u"btn_all_clear_discount")
        sizePolicy.setHeightForWidth(self.btn_all_clear_discount.sizePolicy().hasHeightForWidth())
        self.btn_all_clear_discount.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.btn_all_clear_discount, 2, 2, 5, 1)

        self.lb_remaining_amount = QLabel(Form)
        self.lb_remaining_amount.setObjectName(u"lb_remaining_amount")
        sizePolicy.setHeightForWidth(self.lb_remaining_amount.sizePolicy().hasHeightForWidth())
        self.lb_remaining_amount.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.lb_remaining_amount, 11, 0, 2, 1)

        self.lb_received_coupon_num = QLabel(Form)
        self.lb_received_coupon_num.setObjectName(u"lb_received_coupon_num")

        self.gridLayout_2.addWidget(self.lb_received_coupon_num, 10, 1, 1, 1)

        self.lb_purchase_amount_num = QLabel(Form)
        self.lb_purchase_amount_num.setObjectName(u"lb_purchase_amount_num")
        sizePolicy.setHeightForWidth(self.lb_purchase_amount_num.sizePolicy().hasHeightForWidth())
        self.lb_purchase_amount_num.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.lb_purchase_amount_num, 2, 1, 2, 1)

        self.lb_discount_amount = QLabel(Form)
        self.lb_discount_amount.setObjectName(u"lb_discount_amount")
        sizePolicy.setHeightForWidth(self.lb_discount_amount.sizePolicy().hasHeightForWidth())
        self.lb_discount_amount.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.lb_discount_amount, 4, 0, 1, 1)

        self.lb_amount_received = QLabel(Form)
        self.lb_amount_received.setObjectName(u"lb_amount_received")
        sizePolicy.setHeightForWidth(self.lb_amount_received.sizePolicy().hasHeightForWidth())
        self.lb_amount_received.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.lb_amount_received, 8, 0, 2, 1)

        self.lb_amount_received_num = QLabel(Form)
        self.lb_amount_received_num.setObjectName(u"lb_amount_received_num")
        sizePolicy.setHeightForWidth(self.lb_amount_received_num.sizePolicy().hasHeightForWidth())
        self.lb_amount_received_num.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.lb_amount_received_num, 8, 1, 2, 1)

        self.lb_received_coupon = QLabel(Form)
        self.lb_received_coupon.setObjectName(u"lb_received_coupon")

        self.gridLayout_2.addWidget(self.lb_received_coupon, 10, 0, 1, 1)

        self.lb_payment_amount_num = QLabel(Form)
        self.lb_payment_amount_num.setObjectName(u"lb_payment_amount_num")
        sizePolicy.setHeightForWidth(self.lb_payment_amount_num.sizePolicy().hasHeightForWidth())
        self.lb_payment_amount_num.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.lb_payment_amount_num, 5, 1, 2, 1)

        self.lb_discount_amount_num = QLabel(Form)
        self.lb_discount_amount_num.setObjectName(u"lb_discount_amount_num")
        sizePolicy.setHeightForWidth(self.lb_discount_amount_num.sizePolicy().hasHeightForWidth())
        self.lb_discount_amount_num.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.lb_discount_amount_num, 4, 1, 1, 1)

        self.horizn_line = QFrame(Form)
        self.horizn_line.setObjectName(u"horizn_line")
        self.horizn_line.setFrameShadow(QFrame.Shadow.Plain)
        self.horizn_line.setLineWidth(2)
        self.horizn_line.setFrameShape(QFrame.Shape.HLine)

        self.gridLayout_2.addWidget(self.horizn_line, 7, 0, 1, 3)


        self.verticalLayout_3.addLayout(self.gridLayout_2)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btn_back = QPushButton(Form)
        self.btn_back.setObjectName(u"btn_back")
        sizePolicy.setHeightForWidth(self.btn_back.sizePolicy().hasHeightForWidth())
        self.btn_back.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.btn_back)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        self.verticalLayout_3.setStretch(0, 1)
        self.verticalLayout_3.setStretch(1, 2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.lb_select_discount.setText(QCoreApplication.translate("Form", u"\ud560\uc778\uc744 \uc120\ud0dd\ud574\uc8fc\uc138\uc694", None))
        self.btn_student_discount.setText(QCoreApplication.translate("Form", u"\uc218\ub828\uc0dd \ud560\uc778", None))
        self.btn_academy_discount.setText(QCoreApplication.translate("Form", u"\uc544\uce74\ub370\ubbf8 \ud560\uc778", None))
        self.btn_coupon_discount.setText(QCoreApplication.translate("Form", u"\ucfe0\ud3f0 \ud560\uc778", None))
        self.btn_cash_payment.setText(QCoreApplication.translate("Form", u"\ud604\uae08 \uacb0\uc81c", None))
        self.btn_bank_transfer_payment.setText(QCoreApplication.translate("Form", u"\uacc4\uc88c \uc774\uccb4", None))
        self.btn_academy_point_payment.setText(QCoreApplication.translate("Form", u"\uc544\uce74\ub370\ubbf8\n"
"\ud3ec\uc778\ud2b8", None))
        self.label.setText(QCoreApplication.translate("Form", u"\uacb0\uc81c \uc218\ub2e8\uc744 \uc120\ud0dd\ud574\uc8fc\uc138\uc694", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\uce74\ub4dc \uacb0\uc81c\ub294 \uc9c0\uc6d0\ud558\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4.", None))
        self.lb_payment_amount.setText(QCoreApplication.translate("Form", u"\ud560\uc778 \ud6c4 \uae08\uc561", None))
        self.lb_remaining_amount_num.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.btn_amount_received.setText(QCoreApplication.translate("Form", u"\ubc1b\uc740 \uae08\uc561", None))
        self.lb_purchase_amount.setText(QCoreApplication.translate("Form", u"\uad6c\ub9e4 \uae08\uc561", None))
        self.btn_all_clear_discount.setText(QCoreApplication.translate("Form", u"\uc804\uccb4 \ucde8\uc18c", None))
        self.lb_remaining_amount.setText(QCoreApplication.translate("Form", u"\uac70\uc2a4\ub984\ub3c8", None))
        self.lb_received_coupon_num.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lb_purchase_amount_num.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lb_discount_amount.setText(QCoreApplication.translate("Form", u"\ud560\uc778 \uae08\uc561", None))
        self.lb_amount_received.setText(QCoreApplication.translate("Form", u"\ubc1b\uc740 \ud604\uae08", None))
        self.lb_amount_received_num.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lb_received_coupon.setText(QCoreApplication.translate("Form", u"\ubc1b\uc740 \ucfe0\ud3f0", None))
        self.lb_payment_amount_num.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.lb_discount_amount_num.setText(QCoreApplication.translate("Form", u"TextLabel", None))
        self.btn_back.setText(QCoreApplication.translate("Form", u"\ub4a4\ub85c\uac00\uae30", None))
    # retranslateUi

