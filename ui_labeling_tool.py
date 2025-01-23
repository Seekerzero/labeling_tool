# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'labeling_tool.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QGroupBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSizePolicy,
    QWidget,
)


class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName("Widget")
        Widget.resize(995, 616)
        Widget.setAutoFillBackground(False)
        self.imageLabel = QLabel(Widget)
        self.imageLabel.setObjectName("imageLabel")
        self.imageLabel.setGeometry(QRect(20, 80, 691, 481))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setAutoFillBackground(True)
        self.imageLabel.setScaledContents(False)
        self.rightUpperGroupBox = QGroupBox(Widget)
        self.rightUpperGroupBox.setObjectName("rightUpperGroupBox")
        self.rightUpperGroupBox.setGeometry(QRect(740, 10, 251, 321))
        self.rightUpperGroupBox.setMinimumSize(QSize(0, 321))
        self.rightUpperGroupBox.setContextMenuPolicy(Qt.NoContextMenu)
        self.rightUpperGroupBox.setLayoutDirection(Qt.LeftToRight)
        self.rightUpperGroupBox.setAutoFillBackground(False)
        self.rightUpperGroupBox.setStyleSheet("")
        self.rightUpperGroupBox.setAlignment(Qt.AlignCenter)
        self.rightUpperGroupBox.setFlat(True)
        self.labelList = QListWidget(self.rightUpperGroupBox)
        self.labelList.setObjectName("labelList")
        self.labelList.setGeometry(QRect(20, 180, 221, 121))
        self.labelListTitle = QLabel(self.rightUpperGroupBox)
        self.labelListTitle.setObjectName("labelListTitle")
        self.labelListTitle.setGeometry(QRect(20, 160, 91, 16))
        self.labelListTitle.setScaledContents(True)
        self.addLabelButton = QPushButton(self.rightUpperGroupBox)
        self.addLabelButton.setObjectName("addLabelButton")
        self.addLabelButton.setGeometry(QRect(20, 90, 151, 21))
        self.keyBindEdit = QLineEdit(self.rightUpperGroupBox)
        self.keyBindEdit.setObjectName("keyBindEdit")
        self.keyBindEdit.setGeometry(QRect(110, 60, 121, 20))
        self.keyBindTitle = QLabel(self.rightUpperGroupBox)
        self.keyBindTitle.setObjectName("keyBindTitle")
        self.keyBindTitle.setGeometry(QRect(20, 60, 71, 16))
        self.keyBindTitle.setScaledContents(True)
        self.labelNameEdit = QLineEdit(self.rightUpperGroupBox)
        self.labelNameEdit.setObjectName("labelNameEdit")
        self.labelNameEdit.setGeometry(QRect(110, 30, 121, 20))
        self.labelNameTitle = QLabel(self.rightUpperGroupBox)
        self.labelNameTitle.setObjectName("labelNameTitle")
        self.labelNameTitle.setGeometry(QRect(20, 30, 91, 16))
        self.labelNameTitle.setScaledContents(True)
        self.removeLabelButton = QPushButton(self.rightUpperGroupBox)
        self.removeLabelButton.setObjectName("removeLabelButton")
        self.removeLabelButton.setGeometry(QRect(20, 120, 151, 21))
        self.upperGroupBox = QGroupBox(Widget)
        self.upperGroupBox.setObjectName("upperGroupBox")
        self.upperGroupBox.setGeometry(QRect(10, 10, 711, 51))
        self.openDirButton = QPushButton(self.upperGroupBox)
        self.openDirButton.setObjectName("openDirButton")
        self.openDirButton.setGeometry(QRect(10, 10, 131, 31))
        self.createDBButton = QPushButton(self.upperGroupBox)
        self.createDBButton.setObjectName("createDBButton")
        self.createDBButton.setGeometry(QRect(530, 10, 171, 31))
        self.dbStatus = QLabel(self.upperGroupBox)
        self.dbStatus.setObjectName("dbStatus")
        self.dbStatus.setGeometry(QRect(340, 10, 181, 31))
        self.dbStatus.setScaledContents(True)
        self.imageIDCount = QLabel(self.upperGroupBox)
        self.imageIDCount.setObjectName("imageIDCount")
        self.imageIDCount.setGeometry(QRect(160, 10, 161, 31))
        self.imageIDCount.setScaledContents(True)
        self.rightBelowGroupBox = QGroupBox(Widget)
        self.rightBelowGroupBox.setObjectName("rightBelowGroupBox")
        self.rightBelowGroupBox.setGeometry(QRect(740, 340, 251, 261))
        self.curImageLabelTitle = QLabel(self.rightBelowGroupBox)
        self.curImageLabelTitle.setObjectName("curImageLabelTitle")
        self.curImageLabelTitle.setGeometry(QRect(20, 10, 171, 16))
        self.curImageLabelTitle.setScaledContents(True)
        self.curImageLabelsList = QListWidget(self.rightBelowGroupBox)
        self.curImageLabelsList.setObjectName("curImageLabelsList")
        self.curImageLabelsList.setGeometry(QRect(20, 40, 221, 121))
        self.prevImageButton = QPushButton(self.rightBelowGroupBox)
        self.prevImageButton.setObjectName("prevImageButton")
        self.prevImageButton.setGeometry(QRect(20, 214, 91, 31))
        self.nextImageButton = QPushButton(self.rightBelowGroupBox)
        self.nextImageButton.setObjectName("nextImageButton")
        self.nextImageButton.setGeometry(QRect(150, 214, 91, 31))
        self.focusModeButton = QPushButton(self.rightBelowGroupBox)
        self.focusModeButton.setObjectName("focusModeButton")
        self.focusModeButton.setGeometry(QRect(20, 170, 91, 31))
        self.focusStatus = QLabel(self.rightBelowGroupBox)
        self.focusStatus.setObjectName("focusStatus")
        self.focusStatus.setGeometry(QRect(150, 170, 81, 31))
        self.focusStatus.setScaledContents(True)

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)

    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", "Widget", None))
        self.imageLabel.setText("")
        self.rightUpperGroupBox.setTitle("")
        self.labelListTitle.setText(
            QCoreApplication.translate("Widget", "Label List:", None)
        )
        self.addLabelButton.setText(
            QCoreApplication.translate("Widget", "Add Label", None)
        )
        self.keyBindTitle.setText(
            QCoreApplication.translate("Widget", "Keybind:", None)
        )
        self.labelNameTitle.setText(
            QCoreApplication.translate("Widget", "Label Name:", None)
        )
        self.removeLabelButton.setText(
            QCoreApplication.translate("Widget", "Remove Label", None)
        )
        self.upperGroupBox.setTitle("")
        self.openDirButton.setText(
            QCoreApplication.translate("Widget", "Open Workspace", None)
        )
        self.createDBButton.setText(
            QCoreApplication.translate("Widget", "Create New Database", None)
        )
        self.dbStatus.setText(QCoreApplication.translate("Widget", "dbStatus", None))
        self.imageIDCount.setText(
            QCoreApplication.translate("Widget", "image_id", None)
        )
        self.rightBelowGroupBox.setTitle("")
        self.curImageLabelTitle.setText(
            QCoreApplication.translate("Widget", "Current Image Labels:", None)
        )
        self.prevImageButton.setText(QCoreApplication.translate("Widget", "Prev", None))
        self.nextImageButton.setText(QCoreApplication.translate("Widget", "Next", None))
        self.focusModeButton.setText(
            QCoreApplication.translate("Widget", "Focus Mode", None)
        )
        self.focusStatus.setText(QCoreApplication.translate("Widget", "OFF", None))

    # retranslateUi
