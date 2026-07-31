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
    QLayout, QLineEdit, QListView, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(640, 720)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QSize(640, 720))
        font = QFont()
        font.setBold(False)
        Form.setFont(font)
        Form.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        Form.setAutoFillBackground(False)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies([u"\ub9d1\uc740 \uace0\ub515"])
        font1.setPointSize(16)
        font1.setBold(True)
        self.label.setFont(font1)
        self.label.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.label.setAutoFillBackground(False)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

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
        self.listView = QListView(Form)
        self.listView.setObjectName(u"listView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.listView.sizePolicy().hasHeightForWidth())
        self.listView.setSizePolicy(sizePolicy2)
        self.listView.setMinimumSize(QSize(0, 100))
        self.listView.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.horizontalLayout_3.addWidget(self.listView)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        sizePolicy1.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy1)
        font2 = QFont()
        font2.setPointSize(18)
        font2.setBold(False)
        font2.setKerning(True)
        self.lineEdit.setFont(font2)
        self.lineEdit.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.lineEdit.setMouseTracking(False)
        self.lineEdit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setStyleSheet(u"background-color: transparent; border: none;")
        self.lineEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit, 0, 1, 1, 2)

        self.lineEdit_3 = QLineEdit(Form)
        self.lineEdit_3.setObjectName(u"lineEdit_3")
        sizePolicy1.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy1)
        font3 = QFont()
        font3.setPointSize(20)
        font3.setBold(False)
        font3.setKerning(True)
        self.lineEdit_3.setFont(font3)
        self.lineEdit_3.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.lineEdit_3.setMouseTracking(False)
        self.lineEdit_3.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit_3.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.lineEdit_3.setAutoFillBackground(False)
        self.lineEdit_3.setStyleSheet(u"background-color: transparent; border: none;")
        self.lineEdit_3.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.lineEdit_3, 1, 1, 1, 1)

        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        sizePolicy1.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy1)
        self.lineEdit_2.setFont(font3)
        self.lineEdit_2.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.lineEdit_2.setMouseTracking(False)
        self.lineEdit_2.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit_2.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.lineEdit_2.setAutoFillBackground(False)
        self.lineEdit_2.setStyleSheet(u"background-color: transparent; border: none;")
        self.lineEdit_2.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.gridLayout_2.addWidget(self.lineEdit_2, 1, 2, 1, 1)

        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy1.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy1)
        self.pushButton.setMinimumSize(QSize(0, 180))
        font4 = QFont()
        font4.setPointSize(20)
        font4.setBold(False)
        self.pushButton.setFont(font4)
        self.pushButton.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.pushButton.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.pushButton.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)

        self.gridLayout_2.addWidget(self.pushButton, 3, 1, 1, 2)

        self.lineEdit_4 = QLineEdit(Form)
        self.lineEdit_4.setObjectName(u"lineEdit_4")
        sizePolicy1.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy1)
        font5 = QFont()
        font5.setPointSize(18)
        font5.setBold(False)
        font5.setUnderline(False)
        font5.setKerning(True)
        self.lineEdit_4.setFont(font5)
        self.lineEdit_4.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.lineEdit_4.setMouseTracking(False)
        self.lineEdit_4.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.lineEdit_4.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.lineEdit_4.setAutoFillBackground(False)
        self.lineEdit_4.setStyleSheet(u"background: transparent; border: none; border-bottom: 2px solid black; ")
        self.lineEdit_4.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout_2.addWidget(self.lineEdit_4, 2, 1, 1, 2)


        self.horizontalLayout_3.addLayout(self.gridLayout_2)

        self.horizontalLayout_3.setStretch(0, 3)
        self.horizontalLayout_3.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"\uc544\uce74\ub370\ubbf8 \ud3ec\uc778\ud2b8 \ud0a4\uc624\uc2a4\ud06c", None))
        self.lineEdit.setText(QCoreApplication.translate("Form", u"\ub0a8\uc740 \uc2dc\uac04", None))
        self.lineEdit_3.setText(QCoreApplication.translate("Form", u"0", None))
        self.lineEdit_2.setText(QCoreApplication.translate("Form", u"\ucd08", None))
        self.pushButton.setText(QCoreApplication.translate("Form", u"\uacb0\uc81c\ud558\uae30", None))
        self.lineEdit_4.setText(QCoreApplication.translate("Form", u"\uc120\ud0dd\ud55c \uc0c1\ud488", None))
    # retranslateUi

