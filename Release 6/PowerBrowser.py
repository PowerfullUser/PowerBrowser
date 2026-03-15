import os
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *
from PyQt6.QtPrintSupport import *
from PyQt6.QtPdfWidgets import *
from PyQt6.QtPdf import *
import datetime
import sqlite3
import random

name = "PowerBrowser"
version = 6
display_name = f"PowerBrowser {version}"
chromium_version = qWebEngineChromiumVersion()
chromium_security_version = qWebEngineChromiumSecurityPatchVersion()
framework = PYQT_VERSION_STR
theme = open("Information/theme").read().strip()

light_mode = """
QTabBar:tab {
    border-radius: 10px;
    padding: 7px;
    margin-left: 2px;
    margin-top: 3px;
    margin-bottom: 3px;
    background-color: #5aa2fa;
    font-size: 15px;
}

QTabBar:tab::selected {
    border-radius: 12px;
    padding: 7px;
    margin-left: 2px;
    margin-top: 4px;
    margin-bottom: 2px;
    background-color: #479aff;
    font-size: 15px;
}

QTabBar:tab:hover {
    border-radius: 10px;
    padding: 7px;
    margin-left: 2px;
    margin-top: 4px;
    margin-bottom: 2px;
    background-color: #318cfc;
    font-size: 15px;
    border: 2px solid #000;
}

QToolBar {
    background-color: #d0d4d6;
    border-radius: 10px;
    margin: 5px;
    padding: 3px;
}

QToolButton {
    background-color: #5aa2fa;
    border-radius: 10px;
    padding: 2.5px;
    margin: 3px;
}

QToolButton:checked {
    background-color: #479aff;
    border-radius: 12px;
    padding: 2.5px;
    margin: 3px;
    border: 2px solid #312f2f;
}

QToolButton:hover {
    background-color: #318cfc;
    border-radius: 12px;
    padding: 3px;
    margin: 2px;
    border: 2px solid #312f2f;
}

QLineEdit {
    background-color: #5aa2fa;
    padding: 5px;
    margin: 2px;
    border-radius: 10px;
}

QLineEdit:hover {
    background-color: #5aa2fa;
    padding: 3px;
    margin: 2px;
    border-radius: 10px;
    border: 2px solid #312f2f;
}

QListWidget {
    border: 2px solid #312f2f;
    border-radius: 15px;
    background-color: #d0d4d6;
}

QListWidget:item {
    border: 2px solid #312f2f;
    border-radius: 12px;
    background-color: #5aa2fa;
    padding: 5px;
    margin: 5px;
}

QListWidget:item:hover {
    border: 2px solid #312f2f;
    border-radius: 12px;
    background-color: #479aff;
    padding: 5px;
    margin: 5px;
}

QTextEdit {
    border: 2px solid #312f2f;
    border-radius: 15px;
    background-color: #d0d4d6;
    font-size: 20px;
    color: #000;
    margin: 10px;
    padding: 10px;
}

"""

dark_mode = """
QWidget {
    background-color: #2f3030;
    color: #fff;
}

QTabBar:tab {
    border-radius: 10px;
    background-color: #007ef2;
    margin-left: 2px;
    padding: 7px;
    margin-top: 3px;
    margin-bottom: 3px;
    font-size: 15px;
}

QTabBar:tab::selected {
    border-radius: 12px;
    background-color: blue;
    margin-left: 2px;
    padding: 7px;
    margin-top: 4px;
    margin-bottom: 2px;
    font-size: 15px;
}

QTabBar:tab:hover {
    border-radius: 12px;
    background-color: darkblue;
    margin-left: 2px;
    padding: 7px;
    margin-top: 4px;
    margin-bottom: 2px;
    font-size: 15px;
    border: 2px solid #000;
}

QLineEdit {
    padding: 5px;
    margin: 2px;
    border-radius: 10px;
    background-color: #a2a7b0;
    color: #000;
}

QLineEdit:hover {
    padding: 3px;
    margin: 2px;
    border-radius: 10px;
    background-color: gray;
    color: #000;
    border: 2px solid #000;
}

QToolBar {
    background-color: #434445;
    margin: 5px;
    border-radius: 10px;
    padding: 2px;
}

QToolButton {
    background-color: #a2a7b0;
    border-radius: 10px;
    padding: 2.5px;
    margin: 3px;
    color: #000;
}

QToolButton:checked {
    background-color: blue;
    border-radius: 12px;
    padding: 2.5px;
    margin: 3px;
    border: 2px solid #000;
    color: #fff;
}

QToolButton:hover {
    background-color: gray;
    border-radius: 12px;
    padding: 3px;
    margin: 3px;
    border: 2px solid #000;
}

QListWidget {
    border: 2px solid #000;
    border-radius: 15px;
    background-color: #312f2f;
}

QListWidget:item {
    border: 2px solid #000;
    border-radius: 12px;
    background-color: #a2a7b0;
    padding: 5px;
    margin: 5px;
    color: #000;
}

QListWidget:item:hover {
    border: 2px solid #000;
    border-radius: 12px;
    background-color: gray;
    padding: 5px;
    margin: 5px;
    color: #000;
}

QTextEdit {
    border: 2px solid #000;
    border-radius: 15px;
    background-color: #312f2f;
    font-size: 20px;
    margin: 10px;
    padding: 10px;
}

"""

user = open("Information/username").read()
registered = f"{name} registered to {user}"

class WebEnginePage(QWebEnginePage):
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
        self.data_base_path = "Information/browser_data.db"
    
        super(MainWindow, self).__init__(*args, **kwargs)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.tab_close)
        self.tabs.tabBarDoubleClicked.connect(lambda index: self.main_tab())
        self.tabs.currentChanged.connect(self.update_tab)
        self.tabs.setIconSize(QSize(20, 20))
        self.setCentralWidget(self.tabs)

        plus_button = QToolButton()
        plus_button.setText("+")
        plus_button.setIcon(QIcon("Icons/new-window.png"))
        plus_button.setIconSize(QSize(18, 18))
        plus_button.setAutoRaise(True)
        plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        plus_button.clicked.connect(self.main_tab)

        self.tabs.setCornerWidget(plus_button, Qt.Corner.TopRightCorner)

        context_menu = self.tabs.tabBar()
        context_menu.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        context_menu.customContextMenuRequested.connect(self.custom_context_menu)

        self.download_status_bar = QStatusBar()

        self.download_progress_bar = QProgressBar()
        self.download_progress_bar.setValue(0)
        self.download_status_bar.addPermanentWidget(self.download_progress_bar)

        self.setStatusBar(self.download_status_bar)
        self.download_status_bar.setHidden(True)

        self.data_path = os.path.join(os.path.expanduser("~"), f".{name}{version}_data")

        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        self.main_profile = QWebEngineProfile(f"{name}{version}_Profile", self)
        self.main_profile.setPersistentStoragePath(self.data_path)
        self.main_profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        self.main_profile.setCachePath(self.data_path)
        self.main_profile.defaultProfile()

        self.toolbar()
        self.main_tab()
        self.confirm_theme()
        self.initialize_db()
        self.shortcuts()
        self.update_browser()

    def initialize_db(self):
        try:
            server = sqlite3.connect(self.data_base_path)
            cursor = server.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY,
                    url TEXT NOT NULL,
                    title TEXT,
                    timestamp TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookmarks (
                    id INTEGER PRIMARY KEY,
                    url TEXT NOT NULL,
                    title TEXT
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS download (
                    id INTEGER PRIMARY KEY,
                    downloadpoint TEXT NOT NULL,
                    downloadpath TEXT
                )
            """)

            server.commit()
            server.close()
        except Exception as e:
            with open("Information/error_log.txt", "a") as f:
                f.write(f"{str(e)}\n")

    def confirm_theme(self):
        if theme == "d":
            self.setStyleSheet(dark_mode)
        else:
            self.setStyleSheet(light_mode)

    def main_tab(self):
        tab = QWebEngineView()

        page = WebEnginePage(self.main_profile, self)
        tab.setPage(page)

        tab.setUrl(QUrl("https://sites.google.com/view/powerbrowser-official-website"))

        download_profile = tab.page().profile()
        download_profile.downloadRequested.connect(self.download_requested)

        page.fullScreenRequested.connect(self.toggle_fullscreen)

        new_tab_required = tab.page()
        new_tab_required.createWindow = self.handle_new_tab_request

        i = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(i)

        tab.urlChanged.connect(self.update_url)
        tab.loadFinished.connect(self.save_history)
        tab.iconChanged.connect(self.update_icon)
        tab.titleChanged.connect(self.update_title)

        tab.setToolTip(tab.title())

    def toggle_fullscreen(self, enabled):
        if enabled:
            self.tabs.hide()
        else:
            self.tabs.show()

    def download_requested(self, download):
        try:
            path, _ = QFileDialog.getSaveFileName(self, "Set Download Path", download.downloadFileName())

            if path:
                directory = os.path.dirname(path)
                file_name = os.path.basename(path)

                download.setDownloadDirectory(directory)
                download.setDownloadFileName(file_name)

                download.accept()
                self.download_status_bar.setHidden(False)

                download.receivedBytesChanged.connect(lambda: self.download_progress(download))
                download.totalBytesChanged.connect(lambda: self.download_progress(download))
                download.isFinishedChanged.connect(self.download_finished)

                self.download_path = os.path.abspath(file_name)
            else:
                download.cancel()
                return
        except Exception as e:
            with open("Information/error_log.txt", "a") as f:
                error = str(e)
                f.write(f"{error}\n")

    def download_progress(self, download):
        try:
            received = download.receivedBytes()
            total = download.totalBytes()

            progress = int(round(received / total * 100))
            self.download_progress_bar.setValue(progress)
        except Exception as e:
            with open("Information/error_log.txt", "a") as f:
                error = str(e)
                f.write(f"{error}\n")

    def download_finished(self):
        try:
            QMessageBox.information(self, "Information", "Download Finished!")
            self.download_progress_bar.setValue(0)
            self.download_status_bar.setHidden(True)
            self.note_download()
        except Exception as e:
            with open("Information/error_log.txt", "a") as f:
                error = str(e)
                f.write(f"{error}\n")

    def note_download(self):
        try:
            server = sqlite3.connect(self.data_base_path)
            cursor = server.cursor()
            time = datetime.datetime.now()

            cursor.execute(
                "INSERT INTO download (downloadpoint, downloadpath) values (?, ?)",
                (time, self.download_path)
            )

            server.commit()
            server.close()
        except Exception as e:
            with open("Information/error_log.txt", "a") as f:
                error = str(e)
                f.write(f"{error}\n")

    def tab_close(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def custom_context_menu(self, pos):
        current_widget = self.tabs.currentWidget()

        if isinstance(current_widget, QWebEngineView):
            menu = QMenu()

            back = QAction(QIcon("Icons/left-arrow.png"), "Back", self)
            back.triggered.connect(current_widget.back)

            forward = QAction(QIcon("Icons/right-arrow.png"), "Forward", self)
            forward.triggered.connect(current_widget.forward)

            reload_action = QAction(QIcon("Icons/refresh.png"), "Reload", self)
            reload_action.triggered.connect(current_widget.reload)

            stop = QAction(QIcon("Icons/stop.png"), "Stop", self)
            stop.triggered.connect(current_widget.stop)

            mute_site = QAction("Mute Site", self)
            mute_site.setCheckable(True)
            mute_site.triggered.connect(self.mute_site)

            add_bookmark = QAction("Add Website to Bookmarks List", self)
            add_bookmark.triggered.connect(self.auto_bookmark)

            self.quick_dark_mode = QAction("Switch to Dark mode", self)
            self.quick_dark_mode.setCheckable(True)
            self.quick_dark_mode.triggered.connect(self.quick_dark_mode_function)

            if current_widget.page().isAudioMuted():
                mute_site.setChecked(True)
            else:
                mute_site.setChecked(False)

            if open("Information/theme").read() == "l":
                self.quick_dark_mode.setChecked(False)
            elif open("Information/theme").read() == "d":
                self.quick_dark_mode.setChecked(True)
            else:
                self.quick_dark_mode.setChecked(False)

            menu.addActions([back, forward, reload_action, stop])
            menu.addSeparator()
            menu.addActions([mute_site, add_bookmark])
            menu.addSeparator()
            menu.addActions([self.quick_dark_mode])

            position = self.tabs.tabBar().mapToGlobal(pos)
            menu.exec(position)

    def handle_new_tab_request(self, _type):
        new_tab = QWebEngineView()
        new_page = WebEnginePage(self.main_profile, self)
        new_tab.setPage(new_page)

        new_page.createWindow = self.handle_new_tab_request
        new_page.profile().downloadRequested.connect(self.download_requested)

        i = self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentIndex(i)

        new_tab.urlChanged.connect(self.update_url)
        new_tab.loadFinished.connect(self.save_history)
        new_tab.iconChanged.connect(self.update_icon)
        new_tab.titleChanged.connect(self.update_title)

        new_tab.setToolTip(new_tab.title())

        return new_page

    def toolbar(self):
        navigation_bar = QToolBar("Navigation", self)
        navigation_bar.setIconSize(QSize(28, 28))
        navigation_bar.setMovable(False)

        back = QAction(QIcon("Icons/left-arrow.png"), "Back", self)
        back.triggered.connect(self.back)

        forward = QAction(QIcon("Icons/right-arrow.png"), "Forward", self)
        forward.triggered.connect(self.forward)

        reload = QAction(QIcon("Icons/refresh.png"), "Reload", self)
        reload.triggered.connect(self.reload)

        home = QAction(QIcon("Icons/home-button.png"), "Home", self)
        home.triggered.connect(self.home)

        stop = QAction(QIcon("Icons/stop.png"), "Stop", self)
        stop.triggered.connect(self.stop)

        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Type a URL or a search")
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        settings = QAction(QIcon("Icons/settings.png"), "Settings", self)
        settings.triggered.connect(self.settings_tab)

        instant_search = QAction(QIcon("Icons/magnifier.png"), "Instant Search", self)
        instant_search.triggered.connect(self.instant_search_dialog)

        download_manager = QAction(QIcon("Icons/download.png"), "Download Manager", self)
        download_manager.triggered.connect(self.download_manager)

        navigation_bar.addActions([back, forward])
        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.url_bar)
        navigation_bar.addSeparator()
        navigation_bar.addActions([reload, stop, home])
        navigation_bar.addSeparator()
        navigation_bar.addActions([settings, instant_search, download_manager])

        self.addToolBar(navigation_bar)

    def settings_tab(self):
        settings_tab = QWidget()

        layout = QVBoxLayout()

        toolbar = QToolBar("Settings", self)

        full_screen = QAction("Fullscreen", self)
        full_screen.triggered.connect(lambda: self.showFullScreen())

        windowed = QAction("Windowed", self)
        windowed.triggered.connect(lambda: self.showMaximized())

        show_bookmarks = QAction("Show Bookmarks", self)
        show_bookmarks.triggered.connect(self.show_bookmarks)

        show_history = QAction("Show History", self)
        show_history.triggered.connect(self.show_history)

        self.dark_mode_function = QAction("Dark Mode", self)
        self.dark_mode_function.setCheckable(True)
        self.dark_mode_function.setChecked(False)
        self.dark_mode_function.triggered.connect(self.toggle_of_dark_mode)

        clear_history = QAction("Clear History", self)
        clear_history.triggered.connect(self.delete_history)

        clear_bookmarks = QAction("Clear Bookmarks", self)
        clear_bookmarks.triggered.connect(self.delete_bookmarks)

        about_browser = QAction("About", self)
        about_browser.triggered.connect(self.about_tab)

        update_theme = open("Information/theme").read().strip()

        if update_theme == "d":
            self.dark_mode_function.setChecked(True)
        else:
            self.dark_mode_function.setChecked(False)
        
        toolbar.addActions([full_screen, windowed])
        toolbar.addSeparator()
        toolbar.addActions([show_bookmarks, show_history])
        toolbar.addSeparator()
        toolbar.addActions([clear_history, clear_bookmarks])
        toolbar.addSeparator()
        toolbar.addActions([self.dark_mode_function])
        toolbar.addSeparator()
        toolbar.addActions([about_browser])

        layout.addWidget(toolbar)

        self.list_widget = QListWidget()
        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        layout.addWidget(self.list_widget)

        settings_tab.setLayout(layout)

        self.url_bar.clear()

        i = self.tabs.addTab(settings_tab, "Settings")
        self.tabs.setCurrentIndex(i)

    def back(self):
        browser = self.tabs.currentWidget()

        if isinstance(browser, QWebEngineView):
            browser.back()

    def forward(self):
        browser = self.tabs.currentWidget()

        if isinstance(browser, QWebEngineView):
            browser.forward()

    def reload(self):
        browser = self.tabs.currentWidget()

        if isinstance(browser, QWebEngineView):
            browser.reload()

    def home(self):
        browser = self.tabs.currentWidget()

        if isinstance(browser, QWebEngineView):
            browser.setUrl(QUrl("https://sites.google.com/view/powerbrowser-official-website"))

    def stop(self):
        browser = self.tabs.currentWidget()

        if isinstance(browser, QWebEngineView):
            browser.stop()

    def update_url(self):
        browser = self.tabs.currentWidget()

        if isinstance(browser, QWebEngineView):
            url = browser.url().toString()
            self.url_bar.setText(url)
            browser.setToolTip(browser.title())

    def update_icon(self):
        browser = self.tabs.currentWidget()

        if isinstance(browser, QWebEngineView):
            self.tabs.setTabIcon(self.tabs.currentIndex(), browser.icon())

    def update_title(self):
        browser = self.tabs.currentWidget()

        if isinstance(browser, QWebEngineView):
            title = browser.title()

            if len(title) > 10:
                updated_title = f"{title[:10]}..."
                self.tabs.setTabText(self.tabs.currentIndex(), updated_title)
            else:
                self.tabs.setTabText(self.tabs.currentIndex(), title)

    def update_tab(self):
        browser = self.tabs.currentWidget()

        if isinstance(browser, QWebEngineView):
            self.update_icon()
            self.update_url()
            self.update_title()
        elif isinstance(browser, QWidget):
            self.url_bar.clear()

    def mute_site(self):
        current_tab = self.tabs.currentWidget()

        if isinstance(current_tab, QWebEngineView):
            audio_controller = current_tab.page()

            if audio_controller.isAudioMuted():
                audio_controller.setAudioMuted(False)
            else:
                audio_controller.setAudioMuted(True)

    def navigate_to_url(self):
        current_tab = self.tabs.currentWidget()

        if isinstance(current_tab, QWebEngineView):
            url = self.url_bar.text().lower()

            if url == "yt":
                current_tab.setUrl(QUrl("https://www.youtube.com"))
            elif url == "insearch":
                self.instant_search_dialog()
            elif url == "settings":
                self.settings_tab()
            elif url == "about":
                self.about_tab()
            elif url == "ng":
                self.number_guesser()
            else:
                current_tab.setUrl(QUrl.fromUserInput(url))

    def save_history(self):
        try:
            browser = self.tabs.currentWidget()

            if isinstance(browser, QWebEngineView):
                url = browser.url().toString()
                title = browser.title()
                time = datetime.datetime.now()

                server = sqlite3.connect(self.data_base_path)
                cursor = server.cursor()

                cursor.execute(
                    "INSERT INTO history (url, title, timestamp) values (?, ?, ?)",
                    (url, title, time)
                )
                server.commit()
                server.close()
            else:
                return
        except Exception as e:
            with open("Information/error_log.txt", "a") as f:
                f.write(f"{str(e)}\n")

    def auto_bookmark(self):
        browser = self.tabs.currentWidget()

        if isinstance(browser, QWebEngineView):
            server = sqlite3.connect(self.data_base_path)
            cursor = server.cursor()
            url = browser.url().toString()
            title = browser.title()

            cursor.execute(
                "INSERT INTO bookmarks (url, title) values (?, ?)",
                (url, title)
            )
            server.commit()
            server.close()

            QMessageBox.information(self, "PowerBrowser", "Bookmared Sucessfully")
        else:
            return

    def show_bookmarks(self):
        self.list_widget.clear()

        try:
            server = sqlite3.connect(self.data_base_path)
            cursor = server.cursor()

            cursor.execute("SELECT title, url FROM BOOKMARKS ORDER BY title ASC")
            data = cursor.fetchall()

            server.close()

            if not data:
                self.list_widget.addItem("No bookmarks are stored currently.")
            else:
                for title, url in data:
                    self.list_widget.addItem(f"{title} - {url}")
        except Exception as e:
            with open("Information/error_log.txt", "w") as f:
                f.write(f"{str(e)}\n")

    def show_history(self):
        self.list_widget.clear()

        try:
            server = sqlite3.connect(self.data_base_path)
            cursor = server.cursor()

            cursor.execute("SELECT url, title, timestamp FROM HISTORY")
            data = cursor.fetchall()

            server.close()

            if not data:
                self.list_widget.addItem("No history has been recorded.")
            else:
                for url, title, timestamp in data:
                    self.list_widget.addItem(f"{url} ({title}) - {timestamp}")
        except Exception as e:
            with open("Information/error_log.txt", "a") as f:
                f.write(f"{str(e)}\n")

    def toggle_of_dark_mode(self):
        if not self.dark_mode_function.isChecked():
            self.setStyleSheet(light_mode)

            with open("Information/theme", "w") as f:
                f.write("l")
        else:
            self.setStyleSheet(dark_mode)

            with open("Information/theme", "w") as f:
                f.write("d")

    def about_tab(self):
        about_tab = QTextEdit()

        text = f"{open("Information/about").read()}\n Chromium Version = {str(chromium_version)}\n Chromium Security Patch Version {str(chromium_security_version)}\n Framework: PyQt {framework}\n {registered}"

        about_tab.setText(text)
        about_tab.setEnabled(False)

        i = self.tabs.addTab(about_tab, "About")
        self.tabs.setCurrentIndex(i)

    def delete_history(self):
        try:
            server = sqlite3.connect(self.data_base_path)
            cursor = server.cursor()

            cursor.execute("DELETE FROM history")
            server.commit()
            cursor.execute("VACUUM")
            server.close()

            QMessageBox.information(self, name, "History has been cleared!")
            self.list_widget.clear()
        except Exception as e:
            with open("Information/error_log.txt", "a") as f:
                f.write(f"{str(e)}\n")

    def delete_bookmarks(self):
        try:
            server = sqlite3.connect(self.data_base_path)
            cursor = server.cursor()

            cursor.execute("DELETE FROM bookmarks")
            server.commit()
            cursor.execute("VACUUM")
            server.close()

            QMessageBox.information(self, name, "All Bookmarks have been cleared!")
            self.list_widget.clear()
        except Exception as e:
            with open("Information/error_log.txt", "a") as f:
                f.write(f"{str(e)}\n")

    def instant_search_dialog(self):
        self.dialog = QDialog()

        layout = QVBoxLayout()

        self.input_dialog = QLineEdit()
        self.input_dialog.setFont(QFont("Segoe UI", 20))
        self.input_dialog.setFixedWidth(550)
        self.input_dialog.setPlaceholderText("Search anything using Google.")
        self.input_dialog.returnPressed.connect(self.instant_search_tab)
        layout.addWidget(self.input_dialog)

        toolbar = QToolBar()

        wikipedia = QAction("Wikipedia", self)
        wikipedia.triggered.connect(self.wiki_search)

        britainica = QAction("Britannica", self)
        britainica.triggered.connect(self.britannica_search)

        load_local = QAction("Load Local File", self)
        load_local.triggered.connect(self.local_search_tab)

        load_as_pdf = QAction("Load as PDF", self)
        load_as_pdf.triggered.connect(lambda: self.pdf_view(self.input_dialog.text()))

        toolbar.addActions([wikipedia, britainica, load_local, load_as_pdf])

        layout.addWidget(toolbar)

        self.dialog.setLayout(layout)
        self.dialog.exec()

    def instant_search_tab(self):
        query = self.input_dialog.text().replace(" ", "+")

        tab = QWebEngineView()

        page = WebEnginePage(self.main_profile, self)
        tab.setPage(page)

        tab.setUrl(QUrl(f"https://www.google.com/search?q={query}"))

        download_profile = tab.page().profile()
        download_profile.downloadRequested.connect(self.download_requested)

        new_tab_required = tab.page()
        new_tab_required.createWindow = self.handle_new_tab_request

        i = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(i)

        tab.urlChanged.connect(self.update_url)
        tab.loadFinished.connect(self.save_history)
        tab.iconChanged.connect(self.update_icon)
        tab.titleChanged.connect(self.update_title)

        tab.setToolTip(tab.title())
        self.dialog.destroy()

    def local_search_tab(self):
        query = self.input_dialog.text()

        page = WebEnginePage(self.main_profile, self)

        tab = QWebEngineView()
        tab.setPage(page)

        tab.setUrl(QUrl.fromLocalFile(query))

        download_profile = tab.page().profile()
        download_profile.downloadRequested.connect(self.download_requested)

        new_tab_required = tab.page()
        new_tab_required.createWindow = self.handle_new_tab_request

        i = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(i)

        tab.urlChanged.connect(self.update_url)
        tab.loadFinished.connect(self.save_history)
        tab.iconChanged.connect(self.update_icon)
        tab.titleChanged.connect(self.update_title)

        tab.setToolTip(tab.title())
        self.dialog.destroy()

    def wiki_search(self):
        query = self.input_dialog.text().replace(" ", "_")

        tab = QWebEngineView()

        page = WebEnginePage(self.main_profile, self)
        tab.setPage(page)

        tab.setUrl(QUrl(f"https://www.wikipedia.org/wiki/{query}"))

        download_profile = tab.page().profile()
        download_profile.downloadRequested.connect(self.download_requested)

        new_tab_required = tab.page()
        new_tab_required.createWindow = self.handle_new_tab_request

        i = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(i)

        tab.urlChanged.connect(self.update_url)
        tab.loadFinished.connect(self.save_history)
        tab.iconChanged.connect(self.update_icon)
        tab.titleChanged.connect(self.update_title)

        tab.setToolTip(tab.title())
        self.dialog.destroy()

    def britannica_search(self):
        query = self.input_dialog.text().replace(" ", "+")

        tab = QWebEngineView()

        page = WebEnginePage(self.main_profile, self)
        tab.setPage(page)

        tab.setUrl(QUrl(f"https://www.britannica.com/search?query={query}"))

        download_profile = tab.page().profile()
        download_profile.downloadRequested.connect(self.download_requested)

        new_tab_required = tab.page()
        new_tab_required.createWindow = self.handle_new_tab_request

        i = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(i)

        tab.urlChanged.connect(self.update_url)
        tab.loadFinished.connect(self.save_history)
        tab.iconChanged.connect(self.update_icon)
        tab.titleChanged.connect(self.update_title)

        tab.setToolTip(tab.title())
        self.dialog.destroy()

    def download_manager(self):
        manager = QDialog()

        layout = QVBoxLayout()

        label = QLabel()
        label.setText("Download History")

        font = QFont()
        font.setPointSize(13)
        font.setBold(True)
        label.setFont(font)

        layout.addWidget(label)

        self.download_list_widget = QListWidget()
        self.download_list_widget.setFixedWidth(500)

        server = sqlite3.connect(self.data_base_path)
        cursor = server.cursor()

        cursor.execute("SELECT downloadpoint, downloadpath FROM download")
        data = cursor.fetchall()

        server.close()

        if not data:
            self.download_list_widget.addItem("No Download History Available at this moment.")
        else:
            for downloadpoint, downloadpath in data:
                self.download_list_widget.addItem(f"{os.path.basename(downloadpath)} ({downloadpoint})")

        layout.addWidget(self.download_list_widget)

        toolbar = QToolBar()

        clear_download_history = QAction("Clear Download History", self)
        clear_download_history.triggered.connect(self.clear_download_history)

        toolbar.addActions([clear_download_history])

        layout.addWidget(toolbar)

        manager.setLayout(layout)

        manager.exec()

    def clear_download_history(self):
        try:
            server = sqlite3.connect(self.data_base_path)
            cursor = server.cursor()

            cursor.execute("DELETE FROM download")
            server.commit()
            cursor.execute("VACUUM")
            server.close()

            QMessageBox.information(self, name, "All Download History has been cleared!")
            self.download_list_widget.clear()
            self.download_list_widget.addItem("No Download History Available at this moment.")
        except Exception as e:
            with open("Information/error_log.txt", "a") as f:
                f.write(f"{str(e)}\n")

    def number_guesser(self):
        self.mainwidget_guesser = QDialog()

        layout = QVBoxLayout()

        label1 = QLabel()
        label1.setText("Number Guesser")

        font = QFont()
        font.setPointSize(15)
        font.setBold(True)
        label1.setFont(font)

        layout.addWidget(label1)

        self.guess_bar = QLineEdit()
        self.guess_bar.setFixedWidth(450)
        self.guess_bar.returnPressed.connect(self.guesser)
        self.guess_bar.setPlaceholderText("Enter a number between 1 till 20,000")

        layout.addWidget(self.guess_bar)

        label2 = QLabel()
        label2.setText("Result")

        font = QFont()
        font.setPointSize(15)
        font.setBold(True)

        layout.addWidget(label2)

        self.result = QListWidget()
        layout.addWidget(self.result)

        self.mainwidget_guesser.setLayout(layout)

        self.number = random.randint(1, 20000)

        self.mainwidget_guesser.show()
        self.mainwidget_guesser.exec()

    def guesser(self):
        try:
            number = int(self.guess_bar.text())

            if number > 20000:
                self.result.addItem("Your number is over the guessing limit")

            elif number == self.number:
                self.result.addItem("Your guess is correct!")
                self.number = random.randint(1, 20000)

            elif number < self.number:
                self.result.addItem("Your guess is lower than the number")

            elif number > self.number:
                self.result.addItem("Your guess is higher than the number")

            else:
                pass
        except Exception as e:
            with open("Information/error_log.txt", "a") as f:
                f.write(f"{str(e)}\n")

    def shortcuts(self):
        new_tab = QShortcut(QKeySequence("Ctrl+T"), self)
        new_tab.activated.connect(self.main_tab)

        settings_tab = QShortcut(QKeySequence("Ctrl+Alt+T"), self)
        settings_tab.activated.connect(self.settings_tab)

        instant_search = QShortcut(QKeySequence("Ctrl+I"), self)
        instant_search.activated.connect(self.instant_search_dialog)

        close_tab = QShortcut(QKeySequence("Ctrl+W"), self)
        close_tab.activated.connect(lambda: self.tab_close(self.tabs.currentIndex()))

        make_bookmark = QShortcut(QKeySequence("Ctrl+D"), self)
        make_bookmark.activated.connect(self.auto_bookmark)

        download_history = QShortcut(QKeySequence("Ctrl+Alt+D"), self)
        download_history.activated.connect(self.download_manager)

    def pdf_view(self, get_path):
        try:
            pdf_tab = QWidget()

            layout = QVBoxLayout()

            viewer = QPdfView(self)

            document = QPdfDocument(self)

            url = str(get_path)
            document.load(url)

            viewer.setDocument(document)
            viewer.setPageMode(QPdfView.PageMode.MultiPage)

            layout.addWidget(viewer)
            pdf_tab.setLayout(layout)

            i = self.tabs.addTab(pdf_tab, str(os.path.basename(get_path)))
            self.tabs.setCurrentIndex(i)

            self.dialog.destroy()
        except Exception as e:
            with open("Information/error_log.txt", "a") as f:
                f.write(f"{str(e)}\n")

    def quick_dark_mode_function(self):
        if not self.quick_dark_mode.isChecked():
            with open("Information/theme", "w") as f:
                f.write("l")
                f.close()

            self.setStyleSheet(light_mode)
        else:
            with open("Information/theme", "w") as f:
                f.write("d")
                f.close()

            self.setStyleSheet(dark_mode)

    def update_browser(self):
        date = datetime.date.today()
        cutoff = datetime.date(2026, 4, 5)

        if cutoff <= date:
            self.dialog_box = QDialog()

            layout = QVBoxLayout()

            label = QLabel()
            label.setText("A new update is likely to be available. Would you like to download now?")
            label.setWordWrap(50)
            label.setStyle(QStyleFactory.create("fusion"))
            layout.addWidget(label)

            toolbox = QHBoxLayout()

            update_now = QPushButton("Update Now", self, clicked=self.update_confirmed)
            update_now.setStyle(QStyleFactory.create("fusion"))

            later = QPushButton("Remind Later", self, clicked=lambda: self.dialog_box.destroy())
            later.setStyle(QStyleFactory.create("fusion"))

            toolbox.addWidget(update_now)
            toolbox.addWidget(later)

            layout.addLayout(toolbox)

            self.dialog_box.setLayout(layout)

            self.dialog_box.exec()

    def update_confirmed(self):
        browser = self.tabs.currentWidget()

        if isinstance(browser, QWebEngineView):
            browser.setUrl(QUrl("https://github.com/PowerfullUser/PowerBrowser/releases"))
            self.dialog_box.destroy()
                      
app = QApplication(sys.argv)
app.setApplicationName(name)
app.setApplicationVersion(str(version))
app.setApplicationDisplayName(display_name)
app.setWindowIcon(QIcon("Icons/PowerBrowser.png"))
window = MainWindow()
window.setMinimumWidth(1000)
window.setMinimumHeight(600)
window.showMaximized()
app.exec()
