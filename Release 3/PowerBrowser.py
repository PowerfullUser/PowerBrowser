# PowerBrowser - A multi-tabbed, rich-text editor built with PyQt6.
#
# Copyright 2026 Toshan Chowdhury
#
# Licensed under the GNU General Public License, Version 3.0 (GPLv3);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.en.html
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see the link above.

import datetime

from PyQt6.QtWidgets import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineCore import *

import os
import sys

name = 'PowerBrowser'
version = '3'
light_mode = '''QTabBar::tab {
    background-color: skyblue;
    color: black;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
    border-bottom-left-radius: 7px;
    border-bottom-right-radius: 7px;
    padding-left: 3px;
    padding-right: 3px;
    padding-top: 5px;
    padding-bottom: 5px;
    margin-right: 4px;
    margin-bottom: 3px;
    margin-top: 3px;
    margin-left: 3px;
    font-size: 14px;
}

QTabBar::tab::selected {
    background-color: deepskyblue;
    color: black;
    margin-bottom: 1px;
    margin-top: 5px;
    font-size: 15px;
}

QTabBar::tab:hover {
    background-color: dodgerblue;
    color: black;
    font-size: 16px;
}

QLineEdit {
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    padding: 3px;
    background-color: #dbd7ca;
    margin-right: 5px;
}

QLineEdit:hover {
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    padding: 3px;
    background-color: lightskyblue;
    margin-right: 5px;
}

QToolButton {
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    padding: 3px;
    margin-left: 3px;
    margin-right: 3px;
    background-color: #dbd7ca;
}

QToolButton:hover {
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    padding: 3px;
    margin-left: 3px;
    margin-right: 3px;
    background-color: lightskyblue;
}

QToolBar {
    background-color: #fff;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    padding: 3px;
    margin: 6px;
}

QMenuBar {
    background-color: #f0f0f0;
}

QMenuBar::item {
    background-color: #dbd7ca;
    padding: 5px;
    margin: 3px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    padding-left: 15px;
    padding-right: 15px;
    padding-bottom: 2px;
    padding-top: 2px;
}

QMenu {
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    margin: 3px;
    margin-left: 5px;
    padding: 3px;
    background-color: #dbd7ca;
}

QMenuBar::item:selected {
    background-color: lightskyblue;
    padding: 5px;
    margin: 3px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    padding-left: 15px;
    padding-right: 15px;
    padding-bottom: 2px;
    padding-top: 2px;
}

QMenu::item:selected {
    background-color: lightskyblue;
    padding: 5px;
    margin: 3px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    padding-left: 15px;
    padding-right: 15px;
    padding-bottom: 2px;
    padding-top: 2px;
}'''

dark_mode = '''QWidget {
    background-color: #2e2e2e;
    color: #f0f0f0;
}

QTabBar::tab {
    background-color: #3a3a3a;
    color: #f0f0f0;
    border-top-left-radius: 7px;
    border-top-right-radius: 7px;
    border-bottom-left-radius: 7px;
    border-bottom-right-radius: 7px;
    padding-left: 3px;
    padding-right: 3px;
    padding-top: 5px;
    padding-bottom: 5px;
    margin-right: 4px;
    margin-bottom: 3px;
    margin-top: 3px;
    margin-left: 3px;
    font-size: 14px;
}

QTabBar::tab::selected {
    background-color: #6495ed;
    color: black;
    margin-bottom: 1px;
    margin-top: 5px;
    font-size: 15px;
}

QTabBar::tab:hover {
    background-color: #4a4a4a;
    color: #f0f0f0;
    font-size: 16px;
}

QLineEdit {
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    padding: 3px;
    background-color: #2e2e2e;
    color: #f0f0f0;
    margin-right: 5px;
}

QLineEdit:hover {
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    padding: 3px;
    background-color: #3a3a3a;
    margin-right: 5px;
}

QToolButton {
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    padding: 3px;
    margin-left: 3px;
    margin-right: 3px;
    background-color: #3a3a3a;
    color: #cccccc;
}

QToolButton:hover {
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    padding: 3px;
    margin-left: 3px;
    margin-right: 3px;
    background-color: #4682b4;
    color: white;
}

QToolBar {
    background-color: #202020;
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    border-bottom-left-radius: 10px;
    border-bottom-right-radius: 10px;
    padding: 3px;
    margin: 6px;
}

QMenuBar {
    background-color: #2e2e2e;
    color: #f0f0f0;
}

QMenuBar::item {
    background-color: #3a3a3a;
    color: #f0f0f0;
    padding: 5px;
    margin: 3px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    padding-left: 15px;
    padding-right: 15px;
    padding-bottom: 2px;
    padding-top: 2px;
}

QMenu {
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    margin: 3px;
    margin-left: 5px;
    padding: 3px;
    background-color: #3a3a3a;
    color: #f0f0f0;
}

QMenuBar::item:selected {
    background-color: #4682b4;
    color: white;
    padding: 5px;
    margin: 3px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    padding-left: 15px;
    padding-right: 15px;
    padding-bottom: 2px;
    padding-top: 2px;
}

QMenu::item:selected {
    background-color: #4682b4;
    color: white;
    padding: 5px;
    margin: 3px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    border-bottom-left-radius: 5px;
    border-bottom-right-radius: 5px;
    padding-left: 15px;
    padding-right: 15px;
    padding-bottom: 2px;
    padding-top: 2px;
}

QStatusBar {
    background-color: #2e2e2e;
    color: #f0f0f0;
}'''
theme = open('Information/theme.txt', 'r').read().strip() if os.path.exists('Information/theme.txt') else 'L'


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
        self.center.setMovable(True)
        self.center.currentChanged.connect(self.current_tab_changed)
        self.center.setStatusTip('Tabs')
        self.setCentralWidget(self.center)

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
        self.setMode()

    def toolbar(self):
        self.main_toolbar = QToolBar('Navigation Bar', self)
        self.main_toolbar.setStatusTip('Navigation Bar')
        self.main_toolbar.setMovable(False)

        self.new_tab = QAction(QIcon('Icons/tab.png'), 'New Tab', self)
        self.new_tab.setStatusTip('Open a new tab')
        self.new_tab.triggered.connect(self.home_tab)
        self.new_tab.setShortcut(QKeySequence('Ctrl+T'))
        self.main_toolbar.addAction(self.new_tab)

        self.main_toolbar.addSeparator()

        self.forward_btn = QAction(QIcon('Icons/right-arrow.png'), 'Forward', self)
        self.forward_btn.setStatusTip('Go forward to the next page')
        self.forward_btn.triggered.connect(lambda: self.center.currentWidget().forward())
        self.forward_btn.setShortcut(QKeySequence('Alt+Right'))

        self.back_btn = QAction(QIcon('Icons/left-arrow.png'), 'Back', self)
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

        self.clear_url = QAction(QIcon('Icons/clear-format.png'), 'Clear', self)
        self.clear_url.triggered.connect(lambda: self.url_bar.clear())
        self.clear_url.setStatusTip('Clear the URL Bar')
        self.main_toolbar.addAction(self.clear_url)

        self.main_toolbar.addSeparator()

        self.reload_btn = QAction(QIcon('Icons/refresh.png'), 'Reload', self)
        self.reload_btn.setStatusTip('Reload the current page')
        self.reload_btn.triggered.connect(lambda: self.center.currentWidget().reload())

        self.stop_btn = QAction(QIcon('Icons/stop.png'), 'Stop', self)
        self.stop_btn.setStatusTip('Stop loading the current page')
        self.stop_btn.triggered.connect(lambda: self.center.currentWidget().stop())

        self.home_btn = QAction(QIcon('Icons/home.png'), 'Home', self)
        self.home_btn.setStatusTip('Go to the home page')
        self.home_btn.triggered.connect(lambda: self.center.currentWidget().setUrl(QUrl('https://sites.google.com/view/powerbrowser-official-website')))

        self.main_toolbar.addActions([self.reload_btn, self.stop_btn, self.home_btn])

        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.main_toolbar)

    def home_tab(self, qurl=None, label='New Tab'):
        try:
            url = qurl if qurl else (QUrl('https://sites.google.com/view/powerbrowser-official-website'))

            page = CustomWebEnginePage(self.profile, self)

            self.browser = QWebEngineView()
            self.browser.setPage(page)
            self.browser.setUrl(QUrl(url))
            self.browser.urlChanged.connect(self.add_history)

            i = self.center.addTab(self.browser, label)
            self.center.setCurrentIndex(i)

            profile = self.browser.page().profile()
            profile.downloadRequested.connect(self.handle_download)

            self.browser.urlChanged.connect(lambda qurl, browser=self.browser: self.update_url(qurl, self.browser))
            self.browser.loadFinished.connect(
                lambda _, i=i, browser=self.browser: self.center.setTabText(i, self.browser.page().title()))
            self.browser.titleChanged.connect(lambda title, i=i, browser=self.browser: self.center.setTabText(i, title))
            self.browser.iconChanged.connect(lambda: self.center.setTabIcon(i, self.browser.icon()))
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def add_history(self):
        try:
            widget = self.center.currentWidget()

            if isinstance(widget, QWebEngineView):
                with open('Information/history.txt', 'a') as f:
                    f.write(f'{str(widget.url().toString())} - {datetime.datetime.now}\n')
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def handle_download(self, download):
        try:
            path, _ = QFileDialog.getSaveFileName(self, "Save File", download.downloadFileName())
            if path:
                directory = os.path.dirname(path)
                filename = os.path.basename(path)
                download.setDownloadDirectory(directory)
                download.setDownloadFileName(filename)
                download.accept()

                self.download_status_bar.showMessage(f'Downloading to: {path}')
                self.download_progress.setVisible(True)
                self.download_progress.setValue(0)

                download.receivedBytesChanged.connect(lambda: self.update_download_progress(download))
                download.totalBytesChanged.connect(lambda: self.update_download_progress(download))
                download.isFinishedChanged.connect(lambda: self.download_finished(download))
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def update_download_progress(self, download):
        try:
            received = download.receivedBytes()
            total = download.totalBytes()

            if total > 0:
                progress = int((received / total) * 100)
                self.download_progress.setValue(progress)
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def download_finished(self, download):
        try:
            if download.isFinished():
                self.download_status_bar.showMessage('Download complete!')
                self.download_progress.setVisible(False)
                self.download_progress.setValue(0)
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def close_tab(self, i):
        try:
            if self.center.count() < 2:
                return
            else:
                self.center.removeTab(i)
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def navigate_url(self):
        try:
            current_browser = self.center.currentWidget()

            if isinstance(current_browser, QWebEngineView):
                text = self.url_bar.text()

                if text == 'yt':
                    current_browser.setUrl(QUrl('https://youtube.com'))
                elif text == 'history':
                    self.read_history()
                elif text == 'bookmark':
                    self.bookmark_create_requested()
                elif text == 'bookmarks':
                    self.read_bookmarks()
                else:
                    current_browser.setUrl(QUrl.fromUserInput(text))
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def update_url(self, q, browser=None):
        try:
            self.url_bar.setText(q.toString())
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def menubar(self):
        try:
            self.menu_bar = QMenuBar()
            self.menu_bar.setStatusTip('Menu Bar')

            self.functions_menu = QMenu('Functions', self)
            self.functions_menu.setStatusTip('Functions Menu')

            close_tab = QAction(QIcon('Icons/tab-close.png'), 'Close Tab', self)
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
            normal_mode.setStatusTip('Switch to Normal Mode')
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
            view_history.triggered.connect(self.read_history)

            self.view_menu.addAction(self.view_bookmarks)
            self.view_menu.addSeparator()
            self.view_menu.addAction(view_history)

            self.menu_bar.addMenu(self.view_menu)

            self.setMenuBar(self.menu_bar)
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def read_history(self):
        try:
            dialog = QDialog(self)

            layout = QVBoxLayout()

            label = QLabel(self)
            label.setText('History')
            label.setFont(QFont('Segoe UI', 14))
            layout.addWidget(label)

            history = QListWidget()
            history.addItem(open('Information/history.txt').read().strip())
            history.setMinimumSize(400, 400)
            history.setMaximumSize(400, 400)
            layout.addWidget(history)

            dialog.setLayout(layout)

            dialog.show()
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def read_bookmarks(self):
        try:
            dialog = QDialog(self)

            layout = QVBoxLayout()

            label = QLabel(self)
            label.setText('Bookmarks')
            label.setFont(QFont('Segoe UI', 14))
            layout.addWidget(label)

            bookmarks = QListWidget()
            bookmarks.addItem(open('Information/bookmarks.txt').read().strip())
            bookmarks.setMinimumSize(400, 400)
            bookmarks.setMaximumSize(400, 400)
            layout.addWidget(bookmarks)

            dialog.setLayout(layout)

            dialog.show()
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def bookmark_create_requested(self):
        try:
            text, ok = QInputDialog.getText(self, 'New Bookmark', 'Type the website you want to bookmark:')

            if ok and text:
                with open('Information/bookmarks.txt', 'a') as f:
                    f.write('\n' + text)
            else:
                return
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def suggestion_bar(self):
        try:
            self.recommended = QToolBar('Recommended Sites', self)
            self.recommended.setStatusTip('Recommended Sites')
            self.recommended.setMovable(False)

            chess = QAction('Chess.com', self)
            chess.setStatusTip('Go to Chess.com')
            chess.triggered.connect(lambda: self.center.currentWidget().setUrl(QUrl('https://www.chess.com')))

            wikipedia = QAction('Wikipedia', self)
            wikipedia.setStatusTip('Go to Wikipedia')
            wikipedia.triggered.connect(lambda: self.center.currentWidget().setUrl(QUrl('https://www.wikipedia.org')))

            colour_picker = QAction('Colour Picker', self)
            colour_picker.setStatusTip('Go to Colour Picker')
            colour_picker.triggered.connect(
                lambda: self.center.currentWidget().setUrl(QUrl('https://www.redketchup.io/color-picker')))

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

            view_bookmarks = QAction('View Bookmarks', self)
            view_bookmarks.setStatusTip('View all bookmarks')
            view_bookmarks.triggered.connect(self.read_bookmarks)

            self.recommended.addActions([create_bookmarks, delete_bookmarks, view_bookmarks])
            self.recommended.addSeparator()

            delete_history = QAction('Delete History', self)
            delete_history.setStatusTip('Delete all history')
            delete_history.triggered.connect(self.delete_history)
            self.recommended.addAction(delete_history)

            view_history = QAction('View History', self)
            view_history.setStatusTip('View History')
            view_history.triggered.connect(self.read_history)
            self.recommended.addAction(view_history)

            self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.recommended)
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def current_tab_changed(self, i):
        try:
            qurl = self.center.currentWidget().url()
            self.update_url(qurl, self.center.currentWidget())
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def delete_bookmarks(self):
        try:
            with open('Information/bookmarks.txt', 'w') as f:
                f.write('')

            QMessageBox.information(self, 'Success', 'Bookmarks Deleted Successfully')
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def delete_history(self):
        try:
            with open('Information/history.txt', 'w') as f:
                f.write('')

            QMessageBox.information(self, 'Success', 'History Deleted Successfully')
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def dark_mode_function(self):
        try:
            if self.dark_mode_action.isChecked() == True:
                self.setStyleSheet(dark_mode)
            else:
                self.setStyleSheet(light_mode)
        except Exception as e:
            self.download_status_bar.setStatusTip(str(e))

            with open('Information/error_log.txt', 'a') as f:
                f.write(f'{str(e)}\n')

    def setMode(self):
        if theme.lower() == 'd':
            self.setStyleSheet(dark_mode)
            self.dark_mode_action.setChecked(True)
        else:
            self.setStyleSheet(light_mode)
            self.dark_mode_action.setChecked(False)


app = QApplication(sys.argv)
app.setApplicationName(name + version)
app.setWindowIcon(QIcon('Icons/main.ico'))
app.setApplicationDisplayName(name + ' ' + version)
app.setApplicationVersion(version)
window = MainWindow()
window.showMaximized()
app.exec()
