# Libraries required to be imported
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
import sys

# Details of Browser
name = 'PowerBrowser'
version = '0.1'
font = 'Calibri'
size = 14

# Light and Dark Mode
browser_style_dark = """
    QMainWindow {
    background-color: #121212;
    color: #ffffff;
    }

    QToolBar {
    background-color: #1e1e1e;
    spacing: 6px;
    padding: 4px;
    border: none;
    color: #ffffff;
    }

    QToolButton {
    color: #ffffff;
    background-color: transparent;
    border: none;
    padding: 4px;
    }


    QAction {
        background-color: #1e1e1e;
        spacing: 6px;
        padding: 4px;
        border: none;
    }

    QLineEdit {
        padding: 6px;
        border-radius: 6px;
        border: 1px solid #555;
        background-color: #2c2c2c;
        color: #ffffff;
    }

    QTabWidget::pane {
        border: 1px solid #333;
    }

    QMenuBar {
        padding: 6px;
        border-radius: 6px;
        border: 1px solid #555;
        background-color: #2c2c2c;
        color: #ffffff
    }

    QTabBar::tab {
    background-color: #2c2c2c;
    color: #ffffff;
    padding: 6px;
    border: 1px solid #444;
    border-bottom: none;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    }

    QMenu {
        padding: 6px;
        border-radius: 6px;
        border: 1px solid #555;
        background-color: #2c2c2c;
        color: #ffffff
    }
"""

browser_style = """
    QMainWindow {
    background-color: #fdfdfd;
    color: #000000;
    }


    QToolBar {
    background-color: #eaeaea;
    spacing: 6px;
    padding: 4px;
    border: none;
    }

    QAction {
    background-color: #eaeaea;
    spacing: 6px;
    padding: 4px;
    border: none;
    }

    QLineEdit {
        padding: 6px;
        border-radius: 6px;
    border: 1px solid #ccc;
        background-color: #ffffff;
        color: #000000;
    }

    QTabWidget::pane {
        border: 1px solid #bbb;
    }

    QMenuBar {
        padding: 6px;
    border-radius: 6px;
        border: 1px solid #ccc;
        background-color: #f0f0f0;
        color: #000000;
    }

    QMenu {
        padding: 6px;
    border-radius: 6px;
        border: 1px solid #ccc;
        background-color: #f0f0f0;
        color: #000000;
    }
"""

# Seperate Page for uploadability
class CustomWebEnginePage(QWebEnginePage):
    def chooseFiles(self, mode, old_files, accepted_mime_types):
        file_dialog = QFileDialog()
        if mode == QWebEnginePage.FileSelectOpen:
            file, _ = file_dialog.getOpenFileName()
            return [file] if file else []
        elif mode == QWebEnginePage.FileSelectOpenMultiple:
            files, _ = file_dialog.getOpenFileNames()
            return files
        elif mode == QWebEnginePage.FileSelectSave:
            file, _ = file_dialog.getSaveFileName()
            return [file] if file else []
        return []


# Main Class to be used
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # UI Customization
        self.setStyleSheet(browser_style)

        # The Central Widget
        self.mainwidget = QTabWidget()
        self.mainwidget.setTabsClosable(True)
        self.mainwidget.setFont(QFont(font, size))
        self.mainwidget.setDocumentMode(True)
        self.mainwidget.tabCloseRequested.connect(self.close_tab)
        self.mainwidget.currentChanged.connect(self.currenttabchanged)
        self.mainwidget.tabBarDoubleClicked.connect(self.tab_bar_open_doubleclick)
        self.setCentralWidget(self.mainwidget)

        # Making toolbar appear
        self.toolbar()

        # Making home tab appear
        self.home_tab()

        # Making menu bar appear
        self.menu_bar()

        # Making recommendation bar appear
        self.recommendation_bar()

        self.resize(1280, 800)
        self.show()
        self.setWindowState(Qt.WindowMaximized)


    # The main tab
    def home_tab(self, qurl=None, label='New Tab'):
        url = qurl if qurl else QUrl.fromLocalFile(os.path.abspath('homepage.html'))

        browser = QWebEngineView()
        browser.setPage(CustomWebEnginePage(browser))
        browser.setUrl(url)

        i = self.mainwidget.addTab(browser, label)
        self.mainwidget.setCurrentIndex(i)

        profile = browser.page().profile()
        profile.downloadRequested.connect(self.handle_download)

        browser.urlChanged.connect(lambda qurl, browser=browser:self.update_url(qurl, browser))
        browser.loadFinished.connect(lambda _, i = i, browser=browser: self.mainwidget.setTabText(i, browser.page().title()))

    def recommendation_bar(self):
        self.recommendation_bar = QToolBar('Recommendation Bar', self)
        self.recommendation_bar.setMovable(False)
        self.recommendation_bar.setFont(QFont(font, size-2))

        self.google = QAction('Google', self)
        self.google.triggered.connect(lambda: self.mainwidget.currentWidget().setUrl(QUrl('https://www.google.com')))

        self.chess = QAction('Chess.com', self)
        self.chess.triggered.connect(lambda: self.mainwidget.currentWidget().setUrl(QUrl('https://www.chess.com')))

        self.youtube = QAction('Youtube', self)
        self.youtube.triggered.connect(lambda: self.mainwidget.currentWidget().setUrl(QUrl('https://www.youtube.com')))

        self.wikipedia = QAction('Wikipedia', self)
        self.wikipedia.triggered.connect(lambda: self.mainwidget.currentWidget().setUrl(QUrl('https://www.wikipedia.org')))

        self.github = QAction('GitHub', self)
        self.github.triggered.connect(lambda: self.mainwidget.currentWidget().setUrl(QUrl('https://www.github.com')))
        
        self.recommendation_bar.addActions([self.google, self.chess, self.youtube, self.wikipedia, self.github])

        self.addToolBar(Qt.TopToolBarArea, self.recommendation_bar)

    def menu_bar(self):
        self.menubar = QMenuBar(self)
        self.menubar.setFont(QFont(font, size))

        functions = QMenu('Functions', self)
        functions.setFont(QFont(font, size))
        functions.addAction(self.new_tab)
        functions.addSeparator()
        functions.addActions([self.back_btn, self.forward_btn, self.reload_btn, self.stop_btn, self.home_btn])
        self.menubar.addMenu(functions)

        view = QMenu('View', self)
        view.setFont(QFont(font, size))

        self.dark_mode = QAction('Dark Mode', self)
        self.dark_mode.triggered.connect(lambda: self.setStyleSheet(browser_style_dark))

        self.light_mode = QAction('Light Mode', self)
        self.light_mode.triggered.connect(lambda: self.setStyleSheet(browser_style))

        self.fullscreen = QAction('Fullscreen', self)
        self.fullscreen.triggered.connect(lambda: self.showFullScreen())

        self.normal = QAction('Normal Screen', self)
        self.normal.triggered.connect(lambda: self.showMaximized())

        view.addActions([self.dark_mode, self.light_mode])
        view.addSeparator()
        view.addActions([self.fullscreen, self.normal])
         
        self.menubar.addMenu(view)

        self.setMenuBar(self.menubar)

    # Closing of the tab
    def close_tab(self, i):
        if self.mainwidget.count() < 2:
            return
        else:
            self.mainwidget.removeTab(i)

    # The toolbar
    def toolbar(self):
        self.main_toolbar = QToolBar('Toolbar', self)
        self.main_toolbar.setFont(QFont(font, size))
        self.main_toolbar.setIconSize(QSize(25, 25))
        self.main_toolbar.setMovable(False)

        # Add New Tab
        self.new_tab = QAction(QIcon('icons/new-tab.png'), 'New Tab', self)
        self.new_tab.triggered.connect(self.home_tab)
        self.new_tab.setShortcut(QKeySequence('Ctrl+T'))
        self.main_toolbar.addAction(self.new_tab)

        # Adding Seperator
        self.main_toolbar.addSeparator()

        # Forward Button
        self.forward_btn = QAction(QIcon('icons/arrow.png'), 'Forward', self)
        self.forward_btn.triggered.connect(lambda: self.mainwidget.currentWidget().forward())
        self.forward_btn.setShortcut(QKeySequence.Forward)
    
        # Back Button
        self.back_btn = QAction(QIcon('icons/previous.png'), 'Back', self)
        self.back_btn.triggered.connect(lambda: self.mainwidget.currentWidget().back())
        self.back_btn.setShortcut(QKeySequence.Back)

        # Adding Actions
        self.main_toolbar.addActions([self.back_btn, self.forward_btn])     

        # Adding Seperator
        self.main_toolbar.addSeparator()

        # Adding the Url Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_url)
        self.url_bar.setFont(QFont(font, size))
        self.main_toolbar.addWidget(self.url_bar)

        # Adding Seperator
        self.main_toolbar.addSeparator()

        # Reload/Refresh Button
        self.reload_btn = QAction(QIcon('icons/refresh.png'), 'Reload', self)
        self.reload_btn.triggered.connect(lambda: self.mainwidget.currentWidget().reload())

        # Stop Button
        self.stop_btn = QAction(QIcon('icons/stop.png'), 'Stop', self)
        self.stop_btn.triggered.connect(lambda: self.mainwidget.currentWidget().stop())

        self.home_btn = QAction(QIcon('icons/home-button.png'), 'Home', self)
        self.home_btn.triggered.connect(lambda: self.mainwidget.currentWidget().setUrl(QUrl.fromLocalFile(os.path.abspath('homepage.html'))))

        # Adding Actions
        self.main_toolbar.addActions([self.reload_btn, self.stop_btn, self.home_btn])

        self.addToolBar(Qt.BottomToolBarArea, self.main_toolbar)

    # Updating of Url to Url Text Bar
    def update_url(self, q, browser=None):
        self.url_bar.setText(q.toString())

    def tab_bar_open_doubleclick(self, i):
        if i == -1:
            self.home_tab()

    def currenttabchanged(self, i):
        qurl = self.mainwidget.currentWidget().url()
        self.update_url(qurl, self.mainwidget.currentWidget())

    def navigate_url(self):
        text = self.url_bar.text().strip()

        if not text.startswith(('http://', 'https://')):
            text = 'https://' + text
        
        self.mainwidget.currentWidget().setUrl(QUrl(text))

    def handle_download(self, download):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", download.downloadFileName())
        if path:
            download.setPath(path)
            download.accept()
            self.statusBar().showMessage(f'Donwloading to: {path}')


# Running the class
application = QApplication(sys.argv)
application.setApplicationName(name)
application.setWindowIcon(QIcon('icons/main.png'))
application.setApplicationVersion(version)
window = MainWindow()
application.exec_()
