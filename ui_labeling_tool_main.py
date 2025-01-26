# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'labeling_tool_main.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1139, 731)
        MainWindow.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.actionOpen_Workspace = QAction(MainWindow)
        self.actionOpen_Workspace.setObjectName(u"actionOpen_Workspace")
        self.actionCreate_New_Database = QAction(MainWindow)
        self.actionCreate_New_Database.setObjectName(u"actionCreate_New_Database")
        self.actionBlob_Detector_With_Face_Parsing = QAction(MainWindow)
        self.actionBlob_Detector_With_Face_Parsing.setObjectName(u"actionBlob_Detector_With_Face_Parsing")
        self.actionParse_Current_Image = QAction(MainWindow)
        self.actionParse_Current_Image.setObjectName(u"actionParse_Current_Image")
        self.actionUpdate_Database = QAction(MainWindow)
        self.actionUpdate_Database.setObjectName(u"actionUpdate_Database")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.rightGroupBox = QGroupBox(self.centralwidget)
        self.rightGroupBox.setObjectName(u"rightGroupBox")
        self.rightGroupBox.setGeometry(QRect(810, 0, 321, 499))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rightGroupBox.sizePolicy().hasHeightForWidth())
        self.rightGroupBox.setSizePolicy(sizePolicy)
        self.rightGroupBox.setMinimumSize(QSize(0, 321))
        self.rightGroupBox.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.rightGroupBox.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.rightGroupBox.setAutoFillBackground(False)
        self.rightGroupBox.setStyleSheet(u"")
        self.rightGroupBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.rightGroupBox.setFlat(True)
        self.verticalLayoutWidget = QWidget(self.rightGroupBox)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(20, 20, 281, 459))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.keybindHLayout = QHBoxLayout()
        self.keybindHLayout.setSpacing(20)
        self.keybindHLayout.setObjectName(u"keybindHLayout")
        self.keybindHLayout.setContentsMargins(20, -1, 20, -1)
        self.keyBindTitle = QLabel(self.verticalLayoutWidget)
        self.keyBindTitle.setObjectName(u"keyBindTitle")
        self.keyBindTitle.setScaledContents(True)

        self.keybindHLayout.addWidget(self.keyBindTitle)

        self.keyBindEdit = QLineEdit(self.verticalLayoutWidget)
        self.keyBindEdit.setObjectName(u"keyBindEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.keyBindEdit.sizePolicy().hasHeightForWidth())
        self.keyBindEdit.setSizePolicy(sizePolicy1)

        self.keybindHLayout.addWidget(self.keyBindEdit)


        self.verticalLayout.addLayout(self.keybindHLayout)

        self.labelNameHLayout = QHBoxLayout()
        self.labelNameHLayout.setSpacing(20)
        self.labelNameHLayout.setObjectName(u"labelNameHLayout")
        self.labelNameHLayout.setContentsMargins(20, -1, 20, -1)
        self.labelNameTitle = QLabel(self.verticalLayoutWidget)
        self.labelNameTitle.setObjectName(u"labelNameTitle")
        self.labelNameTitle.setScaledContents(True)

        self.labelNameHLayout.addWidget(self.labelNameTitle)

        self.labelNameEdit = QLineEdit(self.verticalLayoutWidget)
        self.labelNameEdit.setObjectName(u"labelNameEdit")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.labelNameEdit.sizePolicy().hasHeightForWidth())
        self.labelNameEdit.setSizePolicy(sizePolicy2)

        self.labelNameHLayout.addWidget(self.labelNameEdit)


        self.verticalLayout.addLayout(self.labelNameHLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(20, -1, 20, -1)
        self.addLabelButton = QPushButton(self.verticalLayoutWidget)
        self.addLabelButton.setObjectName(u"addLabelButton")
        sizePolicy1.setHeightForWidth(self.addLabelButton.sizePolicy().hasHeightForWidth())
        self.addLabelButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.addLabelButton)

        self.removeLabelButton = QPushButton(self.verticalLayoutWidget)
        self.removeLabelButton.setObjectName(u"removeLabelButton")
        sizePolicy1.setHeightForWidth(self.removeLabelButton.sizePolicy().hasHeightForWidth())
        self.removeLabelButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.removeLabelButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.labelListTitle = QLabel(self.verticalLayoutWidget)
        self.labelListTitle.setObjectName(u"labelListTitle")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.labelListTitle.sizePolicy().hasHeightForWidth())
        self.labelListTitle.setSizePolicy(sizePolicy3)
        self.labelListTitle.setScaledContents(True)

        self.verticalLayout.addWidget(self.labelListTitle)

        self.labelList = QListWidget(self.verticalLayoutWidget)
        self.labelList.setObjectName(u"labelList")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.labelList.sizePolicy().hasHeightForWidth())
        self.labelList.setSizePolicy(sizePolicy4)
        self.labelList.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.verticalLayout.addWidget(self.labelList)

        self.curImageLabelTitle = QLabel(self.verticalLayoutWidget)
        self.curImageLabelTitle.setObjectName(u"curImageLabelTitle")
        self.curImageLabelTitle.setScaledContents(True)

        self.verticalLayout.addWidget(self.curImageLabelTitle)

        self.curImageLabelsList = QListWidget(self.verticalLayoutWidget)
        self.curImageLabelsList.setObjectName(u"curImageLabelsList")

        self.verticalLayout.addWidget(self.curImageLabelsList)

        self.focusModeHLayout = QHBoxLayout()
        self.focusModeHLayout.setSpacing(20)
        self.focusModeHLayout.setObjectName(u"focusModeHLayout")
        self.focusModeHLayout.setContentsMargins(20, -1, 20, -1)
        self.focusModeButton = QPushButton(self.verticalLayoutWidget)
        self.focusModeButton.setObjectName(u"focusModeButton")

        self.focusModeHLayout.addWidget(self.focusModeButton)

        self.focusStatus_2 = QLabel(self.verticalLayoutWidget)
        self.focusStatus_2.setObjectName(u"focusStatus_2")
        self.focusStatus_2.setScaledContents(True)

        self.focusModeHLayout.addWidget(self.focusStatus_2)


        self.verticalLayout.addLayout(self.focusModeHLayout)

        self.imageSwitchButtonHLayout = QHBoxLayout()
        self.imageSwitchButtonHLayout.setSpacing(20)
        self.imageSwitchButtonHLayout.setObjectName(u"imageSwitchButtonHLayout")
        self.imageSwitchButtonHLayout.setContentsMargins(20, -1, 20, -1)
        self.prevImageButton = QPushButton(self.verticalLayoutWidget)
        self.prevImageButton.setObjectName(u"prevImageButton")

        self.imageSwitchButtonHLayout.addWidget(self.prevImageButton)

        self.nextImageButton = QPushButton(self.verticalLayoutWidget)
        self.nextImageButton.setObjectName(u"nextImageButton")

        self.imageSwitchButtonHLayout.addWidget(self.nextImageButton)


        self.verticalLayout.addLayout(self.imageSwitchButtonHLayout)

        self.imageTab = QTabWidget(self.centralwidget)
        self.imageTab.setObjectName(u"imageTab")
        self.imageTab.setGeometry(QRect(0, 70, 811, 511))
        sizePolicy.setHeightForWidth(self.imageTab.sizePolicy().hasHeightForWidth())
        self.imageTab.setSizePolicy(sizePolicy)
        self.imageTab.setUsesScrollButtons(False)
        self.imageTab.setTabBarAutoHide(True)
        self.imageRawTab = QWidget()
        self.imageRawTab.setObjectName(u"imageRawTab")
        self.imageLabelTabRaw = QLabel(self.imageRawTab)
        self.imageLabelTabRaw.setObjectName(u"imageLabelTabRaw")
        self.imageLabelTabRaw.setGeometry(QRect(0, 0, 801, 481))
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.imageLabelTabRaw.sizePolicy().hasHeightForWidth())
        self.imageLabelTabRaw.setSizePolicy(sizePolicy5)
        self.imageLabelTabRaw.setAutoFillBackground(True)
        self.imageLabelTabRaw.setScaledContents(False)
        self.imageTab.addTab(self.imageRawTab, "")
        self.imageSegTab = QWidget()
        self.imageSegTab.setObjectName(u"imageSegTab")
        self.imageLabelTabSeg = QLabel(self.imageSegTab)
        self.imageLabelTabSeg.setObjectName(u"imageLabelTabSeg")
        self.imageLabelTabSeg.setGeometry(QRect(0, 0, 706, 509))
        sizePolicy5.setHeightForWidth(self.imageLabelTabSeg.sizePolicy().hasHeightForWidth())
        self.imageLabelTabSeg.setSizePolicy(sizePolicy5)
        self.imageLabelTabSeg.setAutoFillBackground(True)
        self.imageLabelTabSeg.setScaledContents(False)
        self.imageTab.addTab(self.imageSegTab, "")
        self.imageBlobTab = QWidget()
        self.imageBlobTab.setObjectName(u"imageBlobTab")
        self.imageLabelTabBlob = QLabel(self.imageBlobTab)
        self.imageLabelTabBlob.setObjectName(u"imageLabelTabBlob")
        self.imageLabelTabBlob.setGeometry(QRect(0, 0, 801, 481))
        sizePolicy5.setHeightForWidth(self.imageLabelTabBlob.sizePolicy().hasHeightForWidth())
        self.imageLabelTabBlob.setSizePolicy(sizePolicy5)
        self.imageLabelTabBlob.setAutoFillBackground(True)
        self.imageLabelTabBlob.setScaledContents(False)
        self.imageTab.addTab(self.imageBlobTab, "")
        self.upperGroupBox = QGroupBox(self.centralwidget)
        self.upperGroupBox.setObjectName(u"upperGroupBox")
        self.upperGroupBox.setEnabled(True)
        self.upperGroupBox.setGeometry(QRect(0, 0, 811, 71))
        self.horizontalLayoutWidget_6 = QWidget(self.upperGroupBox)
        self.horizontalLayoutWidget_6.setObjectName(u"horizontalLayoutWidget_6")
        self.horizontalLayoutWidget_6.setGeometry(QRect(10, 20, 781, 31))
        self.topInfoHLayout = QHBoxLayout(self.horizontalLayoutWidget_6)
        self.topInfoHLayout.setSpacing(20)
        self.topInfoHLayout.setObjectName(u"topInfoHLayout")
        self.topInfoHLayout.setContentsMargins(20, 0, 20, 0)
        self.imageIDCount = QLabel(self.horizontalLayoutWidget_6)
        self.imageIDCount.setObjectName(u"imageIDCount")
        self.imageIDCount.setScaledContents(True)

        self.topInfoHLayout.addWidget(self.imageIDCount)

        self.dbStatus = QLabel(self.horizontalLayoutWidget_6)
        self.dbStatus.setObjectName(u"dbStatus")
        self.dbStatus.setScaledContents(True)
        self.dbStatus.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.topInfoHLayout.addWidget(self.dbStatus)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1139, 21))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuDatabase = QMenu(self.menubar)
        self.menuDatabase.setObjectName(u"menuDatabase")
        self.menuTools = QMenu(self.menubar)
        self.menuTools.setObjectName(u"menuTools")
        self.menuBlob_Detector = QMenu(self.menuTools)
        self.menuBlob_Detector.setObjectName(u"menuBlob_Detector")
        self.menuFace_Parsing_Tool = QMenu(self.menuTools)
        self.menuFace_Parsing_Tool.setObjectName(u"menuFace_Parsing_Tool")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuDatabase.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())
        self.menuFile.addAction(self.actionOpen_Workspace)
        self.menuDatabase.addAction(self.actionCreate_New_Database)
        self.menuDatabase.addAction(self.actionUpdate_Database)
        self.menuTools.addAction(self.menuFace_Parsing_Tool.menuAction())
        self.menuTools.addAction(self.menuBlob_Detector.menuAction())
        self.menuBlob_Detector.addAction(self.actionBlob_Detector_With_Face_Parsing)
        self.menuFace_Parsing_Tool.addAction(self.actionParse_Current_Image)

        self.retranslateUi(MainWindow)

        self.imageTab.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Labeling Tool", None))
        self.actionOpen_Workspace.setText(QCoreApplication.translate("MainWindow", u"Open Workspace", None))
        self.actionCreate_New_Database.setText(QCoreApplication.translate("MainWindow", u"Create New Database", None))
        self.actionBlob_Detector_With_Face_Parsing.setText(QCoreApplication.translate("MainWindow", u"Blob Detector With Face Parsing", None))
        self.actionParse_Current_Image.setText(QCoreApplication.translate("MainWindow", u"Parse Current Image", None))
        self.actionUpdate_Database.setText(QCoreApplication.translate("MainWindow", u"Update Database", None))
        self.rightGroupBox.setTitle("")
        self.keyBindTitle.setText(QCoreApplication.translate("MainWindow", u"Keybind:", None))
        self.labelNameTitle.setText(QCoreApplication.translate("MainWindow", u"Label Name:", None))
        self.addLabelButton.setText(QCoreApplication.translate("MainWindow", u"Add Label", None))
        self.removeLabelButton.setText(QCoreApplication.translate("MainWindow", u"Remove Label", None))
        self.labelListTitle.setText(QCoreApplication.translate("MainWindow", u"Label List:", None))
        self.curImageLabelTitle.setText(QCoreApplication.translate("MainWindow", u"Current Image Labels:", None))
        self.focusModeButton.setText(QCoreApplication.translate("MainWindow", u"Focus Mode", None))
        self.focusStatus_2.setText(QCoreApplication.translate("MainWindow", u"OFF", None))
        self.prevImageButton.setText(QCoreApplication.translate("MainWindow", u"Prev", None))
        self.nextImageButton.setText(QCoreApplication.translate("MainWindow", u"Next", None))
        self.imageLabelTabRaw.setText("")
        self.imageTab.setTabText(self.imageTab.indexOf(self.imageRawTab), QCoreApplication.translate("MainWindow", u"Raw", None))
        self.imageLabelTabSeg.setText("")
        self.imageTab.setTabText(self.imageTab.indexOf(self.imageSegTab), QCoreApplication.translate("MainWindow", u"Seg", None))
        self.imageLabelTabBlob.setText("")
        self.imageTab.setTabText(self.imageTab.indexOf(self.imageBlobTab), QCoreApplication.translate("MainWindow", u"blob", None))
        self.upperGroupBox.setTitle("")
        self.imageIDCount.setText(QCoreApplication.translate("MainWindow", u"image_id", None))
        self.dbStatus.setText(QCoreApplication.translate("MainWindow", u"dbStatus", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.menuDatabase.setTitle(QCoreApplication.translate("MainWindow", u"Database", None))
        self.menuTools.setTitle(QCoreApplication.translate("MainWindow", u"Tools", None))
        self.menuBlob_Detector.setTitle(QCoreApplication.translate("MainWindow", u"Blob Detector", None))
        self.menuFace_Parsing_Tool.setTitle(QCoreApplication.translate("MainWindow", u"Face Parsing Tool", None))
    # retranslateUi

