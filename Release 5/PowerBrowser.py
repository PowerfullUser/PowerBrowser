import os
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *
from datetime import datetime
import sqlite3

name = "PowerBrowser"
version = 5
display_name = f"PowerBrowser {version}"
chromium_version = qWebEngineChromiumVersion()
chromium_security_version = qWebEngineChromiumSecurityPatchVersion()
framework = PYQT_VERSION_STR
theme = open("Information/theme").read().strip()
light_mode = open("Information/light_mode.css").read()
dark_mode = open("Information/dark_mode.css").read()

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

        self.toolbar()
        self.main_tab()
        self.confirm_theme()
        self.initialize_db()

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

        new_tab_required = tab.page()
        new_tab_required.createWindow = self.handle_new_tab_request

        i = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(i)

        tab.urlChanged.connect(self.update_url)
        tab.loadFinished.connect(self.save_history)
        tab.iconChanged.connect(self.update_icon)
        tab.titleChanged.connect(self.update_title)

        tab.setToolTip(tab.title())

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
            else:
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

            reload = QAction(QIcon("Icons/refresh.png"), "Reload", self)
            reload.triggered.connect(current_widget.reload)

            stop = QAction(QIcon("Icons/stop.png"), "Stop", self)
            stop.triggered.connect(current_widget.stop)

            mute_site = QAction("Mute Site", self)
            mute_site.setCheckable(True)
            mute_site.triggered.connect(self.mute_site)

            add_bookmark = QAction("Add Website to Bookmarks List", self)
            add_bookmark.triggered.connect(self.auto_bookmark)

            if current_widget.page().isAudioMuted():
                mute_site.setChecked(True)
            else:
                mute_site.setChecked(False)

            menu.addActions([back, forward, reload, stop])
            menu.addSeparator()
            menu.addActions([mute_site, add_bookmark])

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

        navigation_bar.addActions([back, forward])
        navigation_bar.addSeparator()
        navigation_bar.addWidget(self.url_bar)
        navigation_bar.addSeparator()
        navigation_bar.addActions([reload, stop, home])
        navigation_bar.addSeparator()
        navigation_bar.addActions([settings])

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

            if " " in url:
                query = url.replace(" ", "+")
                url = f"https://www.google.com/search?q={query}"
                current_tab.setUrl(QUrl(url))
            elif url == "yt":
                current_tab.setUrl(QUrl("https://www.youtube.com"))
            else:
                current_tab.setUrl(QUrl.fromUserInput(url))

    def save_history(self):
        try:
            browser = self.tabs.currentWidget()

            if isinstance(browser, QWebEngineView):
                url = browser.url().toString()
                title = browser.title()
                time = datetime.now()

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

        text = f"{open("Information/about").read()}\n Chromium Version = {str(chromium_version)}\n Chromium Security Patch Version {str(chromium_security_version)}\n Framework: PyQt {framework}"

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

            QMessageBox.information(self, "PowerBrowser", "History has been cleared!")
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

            QMessageBox.information(self, "PowerBrowser", "All Bookmarks have been cleared!")
            self.list_widget.clear()
        except Exception as e:
            with open("Information/error_log.txt", "a") as f:
                f.write(f"{str(e)}\n")
    
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

