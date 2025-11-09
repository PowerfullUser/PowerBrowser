from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineCore import *

import os
import sys
import datetime as dt

name = 'PowerBrowser'
version = '2.0'
dark_mode = '''QTabWidget {
    background-color: #2b2b2b;
    color: #ffffff;
}

QTabBar::tab {
    background: #3c3c3c;
    color: #ffffff;
    padding: 6px;
    border: 1px solid #555555;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
}

QTabBar::tab:selected {
    background: #808080;
    color: #ffffff;
    border: 1px solid #808080;
}

QMenuBar {
    background-color: #2b2b2b;
    color: #ffffff;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
    border-top-right-radius: 6px;
    border-top-left-radius: 6px;
}

QMenuBar::item:selected {
    background-color: #555555;
    color: #ffffff;
}

QMenu {
    background-color: #808080;
    color: #ffffff;
    padding: 2px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
    border-top-right-radius: 6px;
    border-top-left-radius: 6px;
}

QMenu::item {
    background-color: #555555;
    color: #ffffff;
    border: 1px solid #555555;
    border-radius: 6px;
    padding: 6px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
}

QMenu::item:selected {
    background-color: #555555;
    color: #ffffff;
}

QToolBar {
    background-color: #2b2b2b;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
    border-top-right-radius: 6px;
    border-top-left-radius: 6px;
}

QToolButton {
    background-color: #808080;
    color: #ffffff;
    border: 1px solid #808080;
    border-radius: 6px;
    padding: 6px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
}

QWidget {
    background-color: #2b2b2b;
    color: #ffffff;
}

QLineEdit {
    background-color: #555555;
    color: #ffffff;
    border: 1px solid #555555;
    border-radius: 6px;
    padding: 6px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
}

QTabBar::tab:hover {
    background: #4a90e2;
    color: #ffffff;
}

QTabBar::tab:selected {
    background: #2f74c9;
    color: #ffffff;
    border: 1px solid #2f74c9;
}

QToolButton:hover {
    background-color: #3b6fa8;
    color: #ffffff;
}

QToolButton:focus {
    outline: none;
    border: 1px solid #4a90e2;
}

QMenu::item:hover {
    background-color: #3b6fa8;
    color: #ffffff;
}

QLineEdit:focus {
    border: 1px solid #4a90e2;
    background-color: #606060;
}'''

light_mode = '''QTabWidget {
    background-color: #f0f0f0;
    color: #1f1f1f;
}

QTabBar::tab {
    background: #e0e0e0;
    color: #1f1f1f;
    padding: 6px;
    border: 1px solid #cccccc;
    border-bottom: none;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
}

QTabBar::tab:selected {
    background: #ffffff;
    color: #1f1f1f;
    border: 1px solid #a0a0a0;
}

QMenuBar {
    background-color: #f0f0f0;
    color: #1f1f1f;
    border: 1px solid #cccccc;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
    border-top-right-radius: 6px;
    border-top-left-radius: 6px;
}

QMenuBar::item:selected {
    background-color: #e0e0e0;
    color: #1f1f1f;
}

QMenu {
    background-color: #ffffff;
    color: #1f1f1f;
    padding: 2px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
    border-top-right-radius: 6px;
    border-top-left-radius: 6px;
}

QMenu::item {
    background-color: #ffffff;
    color: #1f1f1f;
    border: 1px solid #ffffff;
    border-radius: 6px;
    padding: 6px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
}

QMenu::item:selected {
    background-color: #d0d0d0;
    color: #1f1f1f;
}

QToolBar {
    background-color: #f0f0f0;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
    border-top-right-radius: 6px;
    border-top-left-radius: 6px;
    border: 1px solid #cccccc;
}

QToolButton {
    background-color: transparent;
    color: #1f1f1f;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 6px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
}

QToolButton:hover {
    background-color: #e0e0e0; 
    border: 1px solid #cccccc;
}

QWidget {
    background-color: #f0f0f0;
    color: #1f1f1f;
}

QAction {
    background-color: transparent;
    color: #1f1f1f;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 6px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
}

QAction:hover {
    background-color: #e0e0e0;
    color: #1f1f1f;
    border: 1px solid #e0e0e0;
}

QLineEdit {
    background-color: #ffffff;
    color: #1f1f1f;
    border: 1px solid #cccccc;
    border-radius: 6px;
    padding: 6px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    border-bottom-left-radius: 6px;
    border-bottom-right-radius: 6px;
}

QTabBar::tab:hover {
    background: #cfe7ff;
    color: #1f1f1f;
}

QTabBar::tab:selected {
    background: #b6dcff;
    color: #1f1f1f;
    border: 1px solid #9ecffb;
}

QToolButton:hover {
    background-color: #e6f2ff;
    color: #1f1f1f;
}

QToolButton:focus {
    outline: none;
    border: 1px solid #7fbfff;
}

QMenu::item:hover {
    background-color: #e6f2ff;
    color: #1f1f1f;
}

QLineEdit:focus {
    border: 1px solid #7fbfff;
    background-color: #ffffff;
}'''

class CustomWebEnginePage(QWebEnginePage):
    def chooseFiles(self, mode, old_files, accepted_mime_types):
        file_dialog = QFileDialog()

        if mode == QWebEnginePage.FileSelectionMode.FileSelectOpen:
            file, _ = file_dialog.getOpenFileName()
            return [file] if file else []
        elif mode == QWebEnginePage.FileSelectionMode.FileSelectOpenMultiple:
            files, _ = file_dialog.getOpenFileNames()
            return files
        elif mode == QWebEnginePage.FileSelectionMode.FileSelectSave:
            file, _ = file_dialog.getSaveFileName()
            return [file] if file else []
        return []


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.center = QTabWidget()
        self.center.setTabsClosable(True)
        self.center.tabCloseRequested.connect(self.close_tab)
        self.center.tabBarDoubleClicked.connect(self.home_tab)
        self.center.currentChanged.connect(self.currenttabchanged)
        self.center.setStatusTip('Tabs')
        self.setCentralWidget(self.center)
        self.setStyleSheet(light_mode)

        self.download_status_bar = QStatusBar()
        self.download_status_bar.setStatusTip('Download Bar')
        self.setStatusBar(self.download_status_bar)

        self.download_progress = QProgressBar()
        self.download_progress.setMaximum(100)
        self.download_progress.setVisible(False)
        self.download_status_bar.addPermanentWidget(self.download_progress)

        self.data_path = os.path.join(os.path.expanduser('~'), f'.{name}{version}_data')

        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        self.profile = QWebEngineProfile(f'{name}{version}_Profile', self)
        self.profile.setPersistentStoragePath(self.data_path)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)

        self.toolbar()
        self.home_tab()
        self.menubar()
        self.suggestion_bar()

    def toolbar(self):
        self.main_toolbar = QToolBar('Navigation Bar', self)
        self.main_toolbar.setStatusTip('Navigation Bar')
        self.main_toolbar.setMovable(False)

        self.new_tab = QAction(QIcon('icons/add.png'), 'New Tab', self)
        self.new_tab.setStatusTip('Open a new tab')
        self.new_tab.triggered.connect(self.home_tab)
        self.new_tab.setShortcut(QKeySequence('Ctrl+T'))
        self.main_toolbar.addAction(self.new_tab)

        self.main_toolbar.addSeparator()

        self.forward_btn = QAction(QIcon('icons/arrow.png'), 'Forward', self)
        self.forward_btn.setStatusTip('Go forward to the next page')
        self.forward_btn.triggered.connect(lambda: self.center.currentWidget().forward())
        self.forward_btn.setShortcut(QKeySequence('Alt+Right'))

        self.back_btn = QAction(QIcon('icons/left-arrow.png'), 'Back', self)
        self.back_btn.setStatusTip('Go back to the previous page')
        self.back_btn.triggered.connect(lambda: self.center.currentWidget().back())
        self.back_btn.setShortcut(QKeySequence('Alt+Left'))

        self.main_toolbar.addActions([self.back_btn, self.forward_btn])     

        self.main_toolbar.addSeparator()

        self.url_bar = QLineEdit()
        self.url_bar.setStatusTip('Type the URL of the website here')
        self.url_bar.returnPressed.connect(self.navigate_url)
        self.url_bar.setPlaceholderText('Only type the URL of the Website')
        self.main_toolbar.addWidget(self.url_bar)

        self.clear_url = QAction(QIcon('icons/close.png'), 'Clear', self)
        self.clear_url.triggered.connect(lambda: self.url_bar.clear())
        self.clear_url.setStatusTip('Clear the URL Bar')
        self.main_toolbar.addAction(self.clear_url)

        self.main_toolbar.addSeparator()

        self.reload_btn = QAction(QIcon('icons/refresh.png'), 'Reload', self)
        self.reload_btn.setStatusTip('Reload the current page')
        self.reload_btn.triggered.connect(lambda: self.center.currentWidget().reload())

        self.stop_btn = QAction(QIcon('icons/stop.png'), 'Stop', self)
        self.stop_btn.setStatusTip('Stop loading the current page')
        self.stop_btn.triggered.connect(lambda: self.center.currentWidget().stop())

        self.home_btn = QAction(QIcon('icons/home-button.png'), 'Home', self)
        self.home_btn.setStatusTip('Go to the home page')
        self.home_btn.triggered.connect(lambda: self.center.currentWidget().setUrl(QUrl('https://www.google.com')))

        self.main_toolbar.addActions([self.reload_btn, self.stop_btn, self.home_btn])

        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.main_toolbar)

    def home_tab(self, qurl=None, label='New Tab'):
        try:
            url = qurl if qurl else (QUrl('https://www.google.com'))

            browser = QWebEngineView()

            page = CustomWebEnginePage(self.profile, self)

            browser.setPage(page)
            browser.setUrl(url)
            browser.setStatusTip('Browser')

            i = self.center.addTab(browser, label)
            self.center.setCurrentIndex(i)

            profile = browser.page().profile()
            profile.downloadRequested.connect(self.handle_download)

            browser.urlChanged.connect(lambda qurl, browser=browser:self.update_url(qurl, browser))
            browser.loadFinished.connect(lambda _, i = i, browser=browser: self.center.setTabText(i, browser.page().title()))
            browser.titleChanged.connect(lambda title, i=i: self.center.setTabText(i, title))
            browser.iconChanged.connect(lambda: self.center.setTabIcon(i, browser.icon()))
        except Exception as e:
            QMessageBox.information(self, 'Error', str(e))

    def handle_download(self, download):
        try:
            path, _ = QFileDialog.getSaveFileName(self, "Save File", download.downloadFileName())
            if path:
                directory = os.path.dirname(path)
                filename = os.path.basename(path)
                download.setDownloadDirectory(directory)
                download.setDownloadFileName(filename)
                download.accept()

                self.download_status_bar.showMessage(f'Donwloading to: {path}')
                self.download_progress.setVisible(True)
                self.download_progress.setValue(0)

                download.receivedBytesChanged.connect(lambda: self.update_download_progress(download))
                download.totalBytesChanged.connect(lambda: self.update_download_progress(download))
                download.isFinishedChanged.connect(lambda: self.download_finished(download))
        except Exception as e:
            QMessageBox.information(self, 'Download Error', str(e))

    def update_download_progress(self, download):
        try:
            received = download.receivedBytes()
            total = download.totalBytes()
            if total > 0:
                progress = int((received / total) * 100)
                self.download_progress.setValue(progress)
        except Exception as e:
            QMessageBox.information(self, 'Progress Error', str(e))


    def download_finished(self, download):
        try:
            if download.isFinished():
                self.download_status_bar.showMessage('Download complete!')
                self.download_progress.setVisible(False)
                self.download_progress.setValue(0)
        except Exception as e:
            QMessageBox.information(self, 'Donwload Finishing Error', str(e))


    def close_tab(self, i):
        try:
            if self.center.count() < 2:
                return
            else:
                self.center.removeTab(i)
        except Exception as e:
            QMessageBox.information(self, 'Error', str(e))

    def navigate_url(self):
        try:
            self.center.currentWidget().setUrl(QUrl.fromUserInput(self.url_bar.text()))

            self.browser = self.center.currentWidget()
            self.browser.loadFinished.connect(self.add_history)
        except Exception as e:
            QMessageBox.information(self, 'Navigation Error', str(e))

    def update_url(self, q, browser=None):
        try:
            self.url_bar.setText(q.toString())
        except Exception as e:
            QMessageBox.information(self, 'URL Update Error', str(e))

    def menubar(self):
        try:
            self.menu_bar = QMenuBar()
            self.menu_bar.setStatusTip('Menu Bar')

            self.functions_menu = QMenu('Functions', self)
            self.functions_menu.setStatusTip('Functions Menu')

            close_tab = QAction('Close Tab', self)
            close_tab.triggered.connect(self.close_tab)
            close_tab.setStatusTip('Close the current tab')
            close_tab.setShortcut(QKeySequence('Ctrl+W'))

            self.functions_menu.addActions([self.new_tab, close_tab])
            self.functions_menu.addSeparator()
            self.functions_menu.addActions([self.back_btn, self.forward_btn, self.reload_btn, self.stop_btn, self.home_btn])

            self.menu_bar.addMenu(self.functions_menu)

            self.view_menu = QMenu('View', self)
            self.view_menu.setStatusTip('View Menu')

            normal_mode = QAction('Normal Mode', self)
            normal_mode.setShortcut(QKeySequence('Esc'))
            normal_mode. setStatusTip('Switch to Normal Mode')
            normal_mode.triggered.connect(lambda: self.showMaximized())

            fullscreen_mode = QAction('Fullscreen Mode', self)
            fullscreen_mode.setStatusTip('Switch to Fullscreen Mode')
            fullscreen_mode.setShortcut(QKeySequence('Ctrl+F'))
            fullscreen_mode.triggered.connect(lambda: self.showFullScreen())

            self.dark_mode_action = QAction('Dark Mode', self)
            self.dark_mode_action.triggered.connect(self.dark_mode_function)
            self.dark_mode_action.setStatusTip('Switch to Dark Mode')
            self.dark_mode_action.setCheckable(True)
            self.dark_mode_action.setChecked(False)
            self.dark_mode_action.setShortcut(QKeySequence('Alt+1'))

            self.view_menu.addActions([normal_mode, fullscreen_mode, self.dark_mode_action])
            self.view_menu.addSeparator()

            self.view_bookmarks = QAction('View Bookmarks', self)
            self.view_bookmarks.setStatusTip('View Bookmarks')
            self.view_bookmarks.triggered.connect(self.read_bookmarks)

            view_history = QAction('View History', self)
            view_history.setStatusTip('View History')
            view_history.triggered.connect(lambda: os.startfile('history.txt'))

            self.view_menu.addAction(self.view_bookmarks)
            self.view_menu.addSeparator()
            self.view_menu.addAction(view_history)

            self.menu_bar.addMenu(self.view_menu)

            self.setMenuBar(self.menu_bar)
        except Exception as e:
            QMessageBox.information(self, 'Menu Bar Error', str(e))

    def read_bookmarks(self):
        try:
            os.startfile('bookmarks.txt')
        except Exception as e:
            QMessageBox.information(self, 'Error', str(e))

    def bookmark_create_requested(self):
        try:
            text, ok = QInputDialog.getText(self, 'New Bookmark', 'Type the website you want to bookmark:')

            if ok and text:
                with open('bookmarks.txt', 'a') as f:
                    f.write('\n' + text)
            else:
                return
        except Exception as e:
            QMessageBox.information(self, 'Error', str(e))
        
    def suggestion_bar(self):
        try:
            self.recommended = QToolBar('Recommended Sites', self)
            self.recommended.setMovable(False)

            chess = QAction('Chess.com', self)
            chess.setStatusTip('Go to Chess.com')
            chess.triggered.connect(lambda: self.center.currentWidget().setUrl(QUrl('https://www.chess.com')))

            wikipedia = QAction('Wikipedia', self)
            wikipedia.setStatusTip('Go to Wikipedia')
            wikipedia.triggered.connect(lambda: self.center.currentWidget().setUrl(QUrl('https://www.wikipedia.org')))

            colour_picker = QAction('Colour Picker', self)
            colour_picker.setStatusTip('Go to Colour Picker')
            colour_picker.triggered.connect(lambda: self.center.currentWidget().setUrl(QUrl('https://www.redketchup.io/color-picker')))

            youtube = QAction('Youtube', self)
            youtube.setStatusTip('Go to Youtube')
            youtube.triggered.connect(lambda: self.center.currentWidget().setUrl(QUrl('https://youtube.com/')))

            git_hub = QAction('GitHub', self)
            git_hub.setStatusTip('Go to GitHub')
            git_hub.triggered.connect(lambda: self.center.currentWidget().setUrl(QUrl('https://github.com/')))

            self.recommended.addActions([chess, wikipedia, colour_picker, youtube, git_hub])
            self.recommended.addSeparator()

            spacer = QWidget()
            spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
            self.recommended.addWidget(spacer)

            self.recommended.addSeparator()

            create_bookmarks = QAction('Create Bookmarks', self)
            create_bookmarks.triggered.connect(self.bookmark_create_requested)
            create_bookmarks.setStatusTip('Create a new bookmark')
            create_bookmarks.setShortcut(QKeySequence('Ctrl+D'))

            delete_bookmarks = QAction('Delete Bookmarks', self)
            delete_bookmarks.setStatusTip('Delete all bookmarks')
            delete_bookmarks.triggered.connect(self.delete_bookmarks)

            self.recommended.addActions([create_bookmarks, delete_bookmarks])
            self.recommended.addSeparator()

            delete_history = QAction('Delete History', self)
            delete_history.setStatusTip('Delete all history')
            delete_history.triggered.connect(self.delete_history)
            self.recommended.addAction(delete_history)

            view_history = QAction('View History', self)
            view_history.setStatusTip('View History')
            view_history.triggered.connect(lambda: os.startfile('history.txt'))
            self.recommended.addAction(view_history)       

            self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.recommended)
        except Exception as e:
            QMessageBox.information(self, 'Suggestion Bar Error', str(e))

    def currenttabchanged(self, i):
        try:
            qurl = self.center.currentWidget().url()
            self.update_url(qurl, self.center.currentWidget())
        except Exception as e:
            QMessageBox.information(self, 'Tab Change Error', str(e))

    def delete_bookmarks(self):
        try:
            with open('bookmarks.txt', 'w') as f:
                f.write("""Bookmarks
    """)
        
            QMessageBox.information(self, 'Success', 'Bookmarks Deleted Successfully')
        except Exception as e:
            QMessageBox.information(self, 'Error', str(e))

    def add_history(self):
        try:
            with open('history.txt', 'a') as f:
                f.write(f'{self.center.currentWidget().url().toString()} - {dt.datetime.now()}\n')
        except Exception as e:
            QMessageBox.information(self, 'Error', str(e))

    def delete_history(self):
        try:
            with open('history.txt', 'w') as f:
                f.write('History\n')

            QMessageBox.information(self, 'Success', 'History Deleted Successfully')
        except Exception as e:
            QMessageBox.information(self, 'Error', str(e))

    def dark_mode_function(self):
        try:
            if self.dark_mode_action.isChecked() == True:
                self.setStyleSheet(dark_mode)
            else:
                self.setStyleSheet(light_mode)
        except Exception as e:
            QMessageBox.information(self, 'Error', str(e))


app = QApplication(sys.argv)
app.setApplicationName(name + version)
app.setWindowIcon(QIcon('Icons/main.ico'))
app.setApplicationDisplayName(name + ' ' + version)
app.setApplicationVersion(version)
window = MainWindow()
window.showMaximized()
app.exec()
