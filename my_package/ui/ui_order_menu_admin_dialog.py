# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'order_menu_admin_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpinBox, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(720, 720)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lbl_title = QLabel(Dialog)
        self.lbl_title.setObjectName(u"lbl_title")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_title.sizePolicy().hasHeightForWidth())
        self.lbl_title.setSizePolicy(sizePolicy)
        self.lbl_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout.addWidget(self.lbl_title)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 2, 0, 1, 1)

        self.btn_export_excel = QPushButton(Dialog)
        self.btn_export_excel.setObjectName(u"btn_export_excel")
        sizePolicy.setHeightForWidth(self.btn_export_excel.sizePolicy().hasHeightForWidth())
        self.btn_export_excel.setSizePolicy(sizePolicy)

        self.gridLayout_2.addWidget(self.btn_export_excel, 0, 0, 1, 1)

        self.tbw_table = QTableWidget(Dialog)
        self.tbw_table.setObjectName(u"tbw_table")

        self.gridLayout_2.addWidget(self.tbw_table, 1, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btn_toggle_soldout = QPushButton(Dialog)
        self.btn_toggle_soldout.setObjectName(u"btn_toggle_soldout")
        sizePolicy.setHeightForWidth(self.btn_toggle_soldout.sizePolicy().hasHeightForWidth())
        self.btn_toggle_soldout.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.btn_toggle_soldout)

        self.btn_delete = QPushButton(Dialog)
        self.btn_delete.setObjectName(u"btn_delete")
        sizePolicy.setHeightForWidth(self.btn_delete.sizePolicy().hasHeightForWidth())
        self.btn_delete.setSizePolicy(sizePolicy)

        self.horizontalLayout_4.addWidget(self.btn_delete)


        self.gridLayout_2.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)

        self.gridLayout_2.setRowStretch(1, 1)

        self.verticalLayout.addLayout(self.gridLayout_2)

        self.gbox_cat_group = QGroupBox(Dialog)
        self.gbox_cat_group.setObjectName(u"gbox_cat_group")
        sizePolicy.setHeightForWidth(self.gbox_cat_group.sizePolicy().hasHeightForWidth())
        self.gbox_cat_group.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.gbox_cat_group)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.le_new_category = QLineEdit(self.gbox_cat_group)
        self.le_new_category.setObjectName(u"le_new_category")
        sizePolicy.setHeightForWidth(self.le_new_category.sizePolicy().hasHeightForWidth())
        self.le_new_category.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.le_new_category)

        self.btn_add_category = QPushButton(self.gbox_cat_group)
        self.btn_add_category.setObjectName(u"btn_add_category")
        sizePolicy.setHeightForWidth(self.btn_add_category.sizePolicy().hasHeightForWidth())
        self.btn_add_category.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.btn_add_category)

        self.line = QFrame(self.gbox_cat_group)
        self.line.setObjectName(u"line")
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setLineWidth(2)
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.line)

        self.cb_delete_category = QComboBox(self.gbox_cat_group)
        self.cb_delete_category.setObjectName(u"cb_delete_category")
        sizePolicy.setHeightForWidth(self.cb_delete_category.sizePolicy().hasHeightForWidth())
        self.cb_delete_category.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.cb_delete_category)

        self.btn_edit_category = QPushButton(self.gbox_cat_group)
        self.btn_edit_category.setObjectName(u"btn_edit_category")
        sizePolicy.setHeightForWidth(self.btn_edit_category.sizePolicy().hasHeightForWidth())
        self.btn_edit_category.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.btn_edit_category)

        self.btn_move_up = QPushButton(self.gbox_cat_group)
        self.btn_move_up.setObjectName(u"btn_move_up")
        sizePolicy.setHeightForWidth(self.btn_move_up.sizePolicy().hasHeightForWidth())
        self.btn_move_up.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.btn_move_up)

        self.btn_move_down = QPushButton(self.gbox_cat_group)
        self.btn_move_down.setObjectName(u"btn_move_down")
        sizePolicy.setHeightForWidth(self.btn_move_down.sizePolicy().hasHeightForWidth())
        self.btn_move_down.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.btn_move_down)

        self.line_2 = QFrame(self.gbox_cat_group)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setLineWidth(2)
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_3.addWidget(self.line_2)

        self.btn_delete_category = QPushButton(self.gbox_cat_group)
        self.btn_delete_category.setObjectName(u"btn_delete_category")
        sizePolicy.setHeightForWidth(self.btn_delete_category.sizePolicy().hasHeightForWidth())
        self.btn_delete_category.setSizePolicy(sizePolicy)

        self.horizontalLayout_3.addWidget(self.btn_delete_category)


        self.verticalLayout.addWidget(self.gbox_cat_group)

        self.gbox_prod_group = QGroupBox(Dialog)
        self.gbox_prod_group.setObjectName(u"gbox_prod_group")
        sizePolicy.setHeightForWidth(self.gbox_prod_group.sizePolicy().hasHeightForWidth())
        self.gbox_prod_group.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.gbox_prod_group)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.sb_price_ja = QSpinBox(self.gbox_prod_group)
        self.sb_price_ja.setObjectName(u"sb_price_ja")
        sizePolicy.setHeightForWidth(self.sb_price_ja.sizePolicy().hasHeightForWidth())
        self.sb_price_ja.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.sb_price_ja, 3, 3, 1, 1)

        self.lbl_price_ja = QLabel(self.gbox_prod_group)
        self.lbl_price_ja.setObjectName(u"lbl_price_ja")
        sizePolicy.setHeightForWidth(self.lbl_price_ja.sizePolicy().hasHeightForWidth())
        self.lbl_price_ja.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lbl_price_ja, 3, 2, 1, 1)

        self.sb_disc_ja = QSpinBox(self.gbox_prod_group)
        self.sb_disc_ja.setObjectName(u"sb_disc_ja")
        sizePolicy.setHeightForWidth(self.sb_disc_ja.sizePolicy().hasHeightForWidth())
        self.sb_disc_ja.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.sb_disc_ja, 4, 3, 1, 1)

        self.lbl_disc_ja = QLabel(self.gbox_prod_group)
        self.lbl_disc_ja.setObjectName(u"lbl_disc_ja")
        sizePolicy.setHeightForWidth(self.lbl_disc_ja.sizePolicy().hasHeightForWidth())
        self.lbl_disc_ja.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lbl_disc_ja, 4, 2, 1, 1)

        self.sb_disc_student = QSpinBox(self.gbox_prod_group)
        self.sb_disc_student.setObjectName(u"sb_disc_student")
        sizePolicy.setHeightForWidth(self.sb_disc_student.sizePolicy().hasHeightForWidth())
        self.sb_disc_student.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.sb_disc_student, 4, 1, 1, 1)

        self.lbl_price_ko = QLabel(self.gbox_prod_group)
        self.lbl_price_ko.setObjectName(u"lbl_price_ko")
        sizePolicy.setHeightForWidth(self.lbl_price_ko.sizePolicy().hasHeightForWidth())
        self.lbl_price_ko.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lbl_price_ko, 3, 0, 1, 1)

        self.lbl_disc_student = QLabel(self.gbox_prod_group)
        self.lbl_disc_student.setObjectName(u"lbl_disc_student")
        sizePolicy.setHeightForWidth(self.lbl_disc_student.sizePolicy().hasHeightForWidth())
        self.lbl_disc_student.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lbl_disc_student, 4, 0, 1, 1)

        self.sb_proce_ko = QSpinBox(self.gbox_prod_group)
        self.sb_proce_ko.setObjectName(u"sb_proce_ko")
        sizePolicy.setHeightForWidth(self.sb_proce_ko.sizePolicy().hasHeightForWidth())
        self.sb_proce_ko.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.sb_proce_ko, 3, 1, 1, 1)

        self.sb_disc_academy = QSpinBox(self.gbox_prod_group)
        self.sb_disc_academy.setObjectName(u"sb_disc_academy")
        sizePolicy.setHeightForWidth(self.sb_disc_academy.sizePolicy().hasHeightForWidth())
        self.sb_disc_academy.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.sb_disc_academy, 5, 1, 1, 1)

        self.lbl_name_ko = QLabel(self.gbox_prod_group)
        self.lbl_name_ko.setObjectName(u"lbl_name_ko")
        sizePolicy.setHeightForWidth(self.lbl_name_ko.sizePolicy().hasHeightForWidth())
        self.lbl_name_ko.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lbl_name_ko, 2, 0, 1, 1)

        self.cb_category = QComboBox(self.gbox_prod_group)
        self.cb_category.setObjectName(u"cb_category")
        sizePolicy.setHeightForWidth(self.cb_category.sizePolicy().hasHeightForWidth())
        self.cb_category.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.cb_category, 0, 1, 2, 3)

        self.lbl_cat_name = QLabel(self.gbox_prod_group)
        self.lbl_cat_name.setObjectName(u"lbl_cat_name")
        sizePolicy.setHeightForWidth(self.lbl_cat_name.sizePolicy().hasHeightForWidth())
        self.lbl_cat_name.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.lbl_cat_name, 0, 0, 2, 1)

        self.txt_name_ko = QLineEdit(self.gbox_prod_group)
        self.txt_name_ko.setObjectName(u"txt_name_ko")
        sizePolicy.setHeightForWidth(self.txt_name_ko.sizePolicy().hasHeightForWidth())
        self.txt_name_ko.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.txt_name_ko, 2, 1, 1, 3)

        self.lbl_disc_academy = QLabel(self.gbox_prod_group)
        self.lbl_disc_academy.setObjectName(u"lbl_disc_academy")
        sizePolicy.setHeightForWidth(self.lbl_disc_academy.sizePolicy().hasHeightForWidth())
        self.lbl_disc_academy.setSizePolicy(sizePolicy)
        self.lbl_disc_academy.setFrameShadow(QFrame.Shadow.Plain)

        self.gridLayout.addWidget(self.lbl_disc_academy, 5, 0, 2, 1)


        self.horizontalLayout_2.addLayout(self.gridLayout)


        self.verticalLayout.addWidget(self.gbox_prod_group)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.btn_add = QPushButton(Dialog)
        self.btn_add.setObjectName(u"btn_add")
        sizePolicy.setHeightForWidth(self.btn_add.sizePolicy().hasHeightForWidth())
        self.btn_add.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.btn_add)

        self.btn_close = QPushButton(Dialog)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.btn_close)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.lbl_title.setText(QCoreApplication.translate("Dialog", u"\uad00\ub9ac\uc790 \uc0c1\ud488 \ubc0f \uce74\ud14c\uace0\ub9ac \uc124\uc815", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\uba54\ub274\uc5d0\uc11c ID\ub97c \ub9c8\uc6b0\uc2a4\ub85c \ub4dc\ub798\uadf8\ud558\uba74 \uba54\ub274\uc758 \uc21c\uc11c\ub97c \ubcc0\uacbd\ud560 \uc218 \uc788\uc2b5\ub2c8\ub2e4.", None))
        self.btn_export_excel.setText(QCoreApplication.translate("Dialog", u"\uc77c\uc77c \ub9e4\ucd9c \uc5d1\uc140 \ub0b4\ubcf4\ub0b4\uae30", None))
        self.btn_toggle_soldout.setText(QCoreApplication.translate("Dialog", u"\ud310\ub9e4/\ud488\uc808 \uc804\ud658", None))
        self.btn_delete.setText(QCoreApplication.translate("Dialog", u"\uc120\ud0dd \uc0c1\ud488 \uc0ad\uc81c", None))
        self.gbox_cat_group.setTitle(QCoreApplication.translate("Dialog", u"\uce74\ud14c\uace0\ub9ac \uad00\ub9ac", None))
        self.le_new_category.setText(QCoreApplication.translate("Dialog", u"\uc0c8 \uce74\ud14c\uace0\ub9ac\uba85", None))
        self.btn_add_category.setText(QCoreApplication.translate("Dialog", u"\uce74\ud14c\uace0\ub9ac \ucd94\uac00", None))
        self.btn_edit_category.setText(QCoreApplication.translate("Dialog", u"\uc218\uc815", None))
        self.btn_move_up.setText(QCoreApplication.translate("Dialog", u"\uc704\ub85c", None))
        self.btn_move_down.setText(QCoreApplication.translate("Dialog", u"\uc544\ub798\ub85c", None))
        self.btn_delete_category.setText(QCoreApplication.translate("Dialog", u"\uce74\ud14c\uace0\ub9ac \uc0ad\uc81c", None))
        self.gbox_prod_group.setTitle(QCoreApplication.translate("Dialog", u"\uc2e0\uaddc \uc0c1\ud488 \ucd94\uac00", None))
        self.lbl_price_ja.setText(QCoreApplication.translate("Dialog", u"\uac00\uaca9(\uc5d4\ud654):", None))
        self.lbl_disc_ja.setText(QCoreApplication.translate("Dialog", u"\uc5d4\ud654 \uace0\uc815 \ud560\uc778\uc561:", None))
        self.lbl_price_ko.setText(QCoreApplication.translate("Dialog", u"\uac00\uaca9(\uc6d0\ud654):", None))
        self.lbl_disc_student.setText(QCoreApplication.translate("Dialog", u"\uc218\ub828\uc0dd \uace0\uc815 \ud560\uc778\uc561:", None))
        self.lbl_name_ko.setText(QCoreApplication.translate("Dialog", u"\uc0c1\ud488\uba85:", None))
        self.lbl_cat_name.setText(QCoreApplication.translate("Dialog", u"\uce74\ud14c\uace0\ub9ac:", None))
        self.lbl_disc_academy.setText(QCoreApplication.translate("Dialog", u"\uc544\uce74\ub370\ubbf8 \uace0\uc815 \ud560\uc778\uc561:", None))
        self.btn_add.setText(QCoreApplication.translate("Dialog", u"\uc0c1\ud488 \ucd94\uac00", None))
        self.btn_close.setText(QCoreApplication.translate("Dialog", u"\ub2eb\uae30", None))
    # retranslateUi

