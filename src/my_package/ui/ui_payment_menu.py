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
from PySide6.QtWidgets import (QApplication, QGridLayout, QLineEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

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
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(8, 8, 8, 8)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.btn_student_discount = QPushButton(Form)
        self.btn_student_discount.setObjectName(u"btn_student_discount")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_student_discount.sizePolicy().hasHeightForWidth())
        self.btn_student_discount.setSizePolicy(sizePolicy1)
        self.btn_student_discount.setFont(font)

        self.gridLayout.addWidget(self.btn_student_discount, 2, 0, 1, 1)

        self.le_academy_discount = QPushButton(Form)
        self.le_academy_discount.setObjectName(u"le_academy_discount")
        sizePolicy1.setHeightForWidth(self.le_academy_discount.sizePolicy().hasHeightForWidth())
        self.le_academy_discount.setSizePolicy(sizePolicy1)
        self.le_academy_discount.setFont(font)
        self.le_academy_discount.setAutoFillBackground(False)

        self.gridLayout.addWidget(self.le_academy_discount, 2, 1, 1, 1)

        self.lineEdit_3 = QLineEdit(Form)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy2)
        self.lineEdit_3.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit_3.setStyleSheet(u"background-color: transparent;")
        self.lineEdit_3.setFrame(False)
        self.lineEdit_3.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.lineEdit_3, 1, 0, 1, 2)

        self.le_select_discount = QLineEdit(Form)
        self.le_select_discount.setObjectName(u"le_select_discount")
        sizePolicy2.setHeightForWidth(self.le_select_discount.sizePolicy().hasHeightForWidth())
        self.le_select_discount.setSizePolicy(sizePolicy2)
        self.le_select_discount.setFont(font)
        self.le_select_discount.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.le_select_discount.setStyleSheet(u"background-color: transparent;")
        self.le_select_discount.setFrame(False)
        self.le_select_discount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_select_discount.setReadOnly(True)

        self.gridLayout.addWidget(self.le_select_discount, 0, 0, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy2.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setPointSize(20)
        font1.setHintingPreference(QFont.PreferDefaultHinting)
        self.lineEdit_2.setFont(font1)
        self.lineEdit_2.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit_2.setStyleSheet(u"background-color: transparent;")
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit_2, 1, 0, 1, 3)

        self.btn_bank_transfer_payment = QPushButton(Form)
        self.btn_bank_transfer_payment.setObjectName(u"btn_bank_transfer_payment")
        sizePolicy1.setHeightForWidth(self.btn_bank_transfer_payment.sizePolicy().hasHeightForWidth())
        self.btn_bank_transfer_payment.setSizePolicy(sizePolicy1)
        self.btn_bank_transfer_payment.setFont(font)

        self.gridLayout_3.addWidget(self.btn_bank_transfer_payment, 2, 1, 1, 1)

        self.btn_cash_payment = QPushButton(Form)
        self.btn_cash_payment.setObjectName(u"btn_cash_payment")
        sizePolicy1.setHeightForWidth(self.btn_cash_payment.sizePolicy().hasHeightForWidth())
        self.btn_cash_payment.setSizePolicy(sizePolicy1)
        self.btn_cash_payment.setFont(font)

        self.gridLayout_3.addWidget(self.btn_cash_payment, 2, 0, 1, 1)

        self.btn_academy_point_payment = QPushButton(Form)
        self.btn_academy_point_payment.setObjectName(u"btn_academy_point_payment")
        sizePolicy1.setHeightForWidth(self.btn_academy_point_payment.sizePolicy().hasHeightForWidth())
        self.btn_academy_point_payment.setSizePolicy(sizePolicy1)
        self.btn_academy_point_payment.setFont(font)

        self.gridLayout_3.addWidget(self.btn_academy_point_payment, 2, 2, 1, 1)

        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy2.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy2)
        self.lineEdit.setFont(font1)
        self.lineEdit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit.setStyleSheet(u"background-color: transparent;")
        self.lineEdit.setFrame(False)
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_3.addWidget(self.lineEdit, 0, 0, 1, 3)


        self.verticalLayout.addLayout(self.gridLayout_3)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.le_discount_amount_num = QLineEdit(Form)
        self.le_discount_amount_num.setObjectName(u"le_discount_amount_num")
        sizePolicy1.setHeightForWidth(self.le_discount_amount_num.sizePolicy().hasHeightForWidth())
        self.le_discount_amount_num.setSizePolicy(sizePolicy1)
        self.le_discount_amount_num.setFont(font)
        self.le_discount_amount_num.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.le_discount_amount_num.setFrame(False)
        self.le_discount_amount_num.setReadOnly(True)

        self.gridLayout_2.addWidget(self.le_discount_amount_num, 1, 1, 1, 1)

        self.le_payment_amount = QLineEdit(Form)
        self.le_payment_amount.setObjectName(u"le_payment_amount")
        sizePolicy1.setHeightForWidth(self.le_payment_amount.sizePolicy().hasHeightForWidth())
        self.le_payment_amount.setSizePolicy(sizePolicy1)
        self.le_payment_amount.setFont(font)
        self.le_payment_amount.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.le_payment_amount.setFrame(False)
        self.le_payment_amount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_payment_amount.setReadOnly(True)

        self.gridLayout_2.addWidget(self.le_payment_amount, 2, 0, 1, 1)

        self.le_purchase_amount_num = QLineEdit(Form)
        self.le_purchase_amount_num.setObjectName(u"le_purchase_amount_num")
        sizePolicy1.setHeightForWidth(self.le_purchase_amount_num.sizePolicy().hasHeightForWidth())
        self.le_purchase_amount_num.setSizePolicy(sizePolicy1)
        self.le_purchase_amount_num.setFont(font)
        self.le_purchase_amount_num.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.le_purchase_amount_num.setFrame(False)
        self.le_purchase_amount_num.setReadOnly(True)

        self.gridLayout_2.addWidget(self.le_purchase_amount_num, 0, 1, 1, 1)

        self.le_purchase_amount = QLineEdit(Form)
        self.le_purchase_amount.setObjectName(u"le_purchase_amount")
        sizePolicy1.setHeightForWidth(self.le_purchase_amount.sizePolicy().hasHeightForWidth())
        self.le_purchase_amount.setSizePolicy(sizePolicy1)
        self.le_purchase_amount.setFont(font)
        self.le_purchase_amount.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.le_purchase_amount.setStyleSheet(u"background-color: transparent;")
        self.le_purchase_amount.setFrame(False)
        self.le_purchase_amount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_purchase_amount.setReadOnly(True)

        self.gridLayout_2.addWidget(self.le_purchase_amount, 0, 0, 1, 1)

        self.le_payment_amount_num = QLineEdit(Form)
        self.le_payment_amount_num.setObjectName(u"le_payment_amount_num")
        sizePolicy1.setHeightForWidth(self.le_payment_amount_num.sizePolicy().hasHeightForWidth())
        self.le_payment_amount_num.setSizePolicy(sizePolicy1)
        self.le_payment_amount_num.setFont(font)
        self.le_payment_amount_num.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.le_payment_amount_num.setFrame(False)
        self.le_payment_amount_num.setReadOnly(True)

        self.gridLayout_2.addWidget(self.le_payment_amount_num, 2, 1, 1, 1)

        self.le_discount_amount = QLineEdit(Form)
        self.le_discount_amount.setObjectName(u"le_discount_amount")
        sizePolicy1.setHeightForWidth(self.le_discount_amount.sizePolicy().hasHeightForWidth())
        self.le_discount_amount.setSizePolicy(sizePolicy1)
        self.le_discount_amount.setFont(font)
        self.le_discount_amount.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.le_discount_amount.setFrame(False)
        self.le_discount_amount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.le_discount_amount.setReadOnly(True)

        self.gridLayout_2.addWidget(self.le_discount_amount, 1, 0, 1, 1)

        self.btn_back = QPushButton(Form)
        self.btn_back.setObjectName(u"btn_back")
        sizePolicy.setHeightForWidth(self.btn_back.sizePolicy().hasHeightForWidth())
        self.btn_back.setSizePolicy(sizePolicy)
        font2 = QFont()
        font2.setPointSize(30)
        self.btn_back.setFont(font2)

        self.gridLayout_2.addWidget(self.btn_back, 3, 0, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout_2)

        self.verticalLayout.setStretch(0, 2)
        self.verticalLayout.setStretch(1, 2)
        self.verticalLayout.setStretch(2, 2)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.btn_student_discount.setText(QCoreApplication.translate("Form", u"\uc218\ub828\uc0dd \ud560\uc778", None))
        self.le_academy_discount.setText(QCoreApplication.translate("Form", u"\uc544\uce74\ub370\ubbf8 \ud560\uc778", None))
        self.lineEdit_3.setText(QCoreApplication.translate("Form", u"\ub450\ubc88 \ud074\ub9ad\ud558\uba74 \ud560\uc778\uc774 \ucde8\uc18c\ub429\ub2c8\ub2e4.", None))
        self.le_select_discount.setText(QCoreApplication.translate("Form", u"\ud560\uc778\uc744 \uc120\ud0dd\ud574\uc8fc\uc138\uc694", None))
        self.lineEdit_2.setText(QCoreApplication.translate("Form", u"\uce74\ub4dc \uacb0\uc81c\ub294 \uc9c0\uc6d0\ud558\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4.", None))
        self.btn_bank_transfer_payment.setText(QCoreApplication.translate("Form", u"\uacc4\uc88c \uc774\uccb4", None))
        self.btn_cash_payment.setText(QCoreApplication.translate("Form", u"\ud604\uae08 \uacb0\uc81c", None))
        self.btn_academy_point_payment.setText(QCoreApplication.translate("Form", u"\uc544\uce74\ub370\ubbf8 \ud3ec\uc778\ud2b8", None))
        self.lineEdit.setText(QCoreApplication.translate("Form", u"\uacb0\uc81c \uc218\ub2e8\uc744 \uc120\ud0dd\ud574\uc8fc\uc138\uc694", None))
        self.le_discount_amount_num.setStyleSheet(QCoreApplication.translate("Form", u"background-color: transparent;", None))
        self.le_payment_amount.setStyleSheet(QCoreApplication.translate("Form", u"background-color: transparent;", None))
        self.le_payment_amount.setText(QCoreApplication.translate("Form", u"\uacb0\uc81c \uae08\uc561", None))
        self.le_purchase_amount_num.setStyleSheet(QCoreApplication.translate("Form", u"background-color: transparent;", None))
        self.le_purchase_amount.setText(QCoreApplication.translate("Form", u"\uad6c\ub9e4 \uae08\uc561", None))
        self.le_payment_amount_num.setStyleSheet(QCoreApplication.translate("Form", u"background-color: transparent;", None))
        self.le_discount_amount.setStyleSheet(QCoreApplication.translate("Form", u"background-color: transparent;", None))
        self.le_discount_amount.setText(QCoreApplication.translate("Form", u"\ud560\uc778 \uae08\uc561", None))
        self.btn_back.setText(QCoreApplication.translate("Form", u"\ub4a4\ub85c\uac00\uae30", None))
    # retranslateUi

