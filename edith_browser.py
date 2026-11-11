
import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QAction,
    QLineEdit, QStatusBar, QProgressBar, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView


class EdithBrowser(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Edith | Your Personal Browser")
        self.setMinimumSize(1050, 700)
        self.resize(1400, 850)

        # Browser engine
        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)

        # Main application theme
        self.setStyleSheet("""
            QMainWindow {
                background: #11111B;
            }

            QToolBar {
                background: #191927;
                border: none;
                spacing: 10px;
                padding: 12px;
            }

            QToolButton {
                color: #D9C9FF;
                background: #29263B;
                border: none;
                border-radius: 10px;
                padding: 9px;
                min-width: 28px;
                min-height: 25px;
                font-size: 17px;
            }

            QToolButton:hover {
                background: #51416F;
                color: white;
            }

            QLineEdit {
                color: white;
                background: #29263B;
                border: 1px solid #51416F;
                border-radius: 14px;
                padding: 11px 16px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 1px solid #B99AFF;
            }

            QStatusBar {
                background: #191927;
                color: #B9A9D8;
                border-top: 1px solid #39334D;
                padding: 4px;
            }

            QProgressBar {
                background: #29263B;
                border: none;
                height: 3px;
            }

            QProgressBar::chunk {
                background: #B99AFF;
            }
        """)

        # Toolbar
        toolbar = QToolBar("Edith Navigation")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Branding
        brand = QLabel("  ✦ EDITH  ")
        brand.setFont(QFont("Segoe UI", 17, QFont.Bold))
        brand.setStyleSheet("color: #C6A7FF; padding: 5px;")
        toolbar.addWidget(brand)

        # Navigation buttons
        back = QAction("❮", self)
        back.setToolTip("Back")
        back.triggered.connect(self.browser.back)
        toolbar.addAction(back)

        forward = QAction("❯", self)
        forward.setToolTip("Forward")
        forward.triggered.connect(self.browser.forward)
        toolbar.addAction(forward)

        reload = QAction("⟳", self)
        reload.setToolTip("Reload")
        reload.triggered.connect(self.browser.reload)
        toolbar.addAction(reload)

        home = QAction("⌂", self)
        home.setToolTip("Edith Home")
        home.triggered.connect(self.show_home)
        toolbar.addAction(home)

        # Address bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText(
            "Search or enter a website address..."
        )
        self.url_bar.returnPressed.connect(self.navigate)
        toolbar.addWidget(self.url_bar)

        # Progress indicator
        self.progress = QProgressBar()
        self.progress.setMaximumWidth(140)
        self.progress.setTextVisible(False)
        self.progress.hide()

        # Status bar
        status = QStatusBar()
        self.setStatusBar(status)
        status.showMessage("✦ Welcome to Edith")
        status.addPermanentWidget(self.progress)

        self.status = status

        # Browser signals
        self.browser.urlChanged.connect(self.update_url)
        self.browser.loadProgress.connect(self.update_progress)
        self.browser.loadStarted.connect(self.loading_started)
        self.browser.loadFinished.connect(self.loading_finished)
        self.browser.titleChanged.connect(self.update_title)

        # Keyboard shortcuts
        back.setShortcut("Alt+Left")
        forward.setShortcut("Alt+Right")
        reload.setShortcut("Ctrl+R")
        home.setShortcut("Alt+Home")

        # Load custom Edith homepage
        self.show_home()

    # Custom Edith homepage
    def show_home(self):

        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, initial-scale=1.0">

            <title>Edith - Home</title>

            <style>
                * {
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                }

                body {
                    font-family: 'Segoe UI', sans-serif;
                    min-height: 100vh;
                    background:
                        radial-gradient(
                            circle at 15% 20%,
                            #382957 0%,
                            transparent 35%
                        ),
                        radial-gradient(
                            circle at 85% 75%,
                            #33204E 0%,
                            transparent 35%
                        ),
                        linear-gradient(
                            135deg,
                            #11111B,
                            #1B172A,
                            #171323
                        );

                    color: white;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    overflow-x: hidden;
                    position: relative;
                }

                .top {
                    position: absolute;
                    top: 30px;
                    left: 45px;
                    right: 45px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                .logo-small {
                    color: #C9A8FF;
                    font-size: 22px;
                    font-weight: bold;
                    letter-spacing: 4px;
                }

                .date {
                    color: #A99BBE;
                    font-size: 14px;
                }

                .container {
                    width: 90%;
                    max-width: 850px;
                    text-align: center;
                    margin-top: -30px;
                }

                .symbol {
                    font-size: 55px;
                    color: #C5A4FF;
                    margin-bottom: 8px;
                    text-shadow: 0 0 35px #A477FF;
                }

                h1 {
                    font-size: clamp(55px, 10vw, 90px);
                    letter-spacing: 12px;
                    font-weight: 700;
                    background: linear-gradient(
                        90deg,
                        #DCC9FF,
                        #A980F3,
                        #E2D3FF
                    );
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                }

                .subtitle {
                    color: #AFA2C8;
                    font-size: 16px;
                    letter-spacing: 3px;
                    margin-top: 8px;
                    margin-bottom: 48px;
                }

                .clock {
                    font-size: 38px;
                    color: #E7DCFF;
                    font-weight: 300;
                    margin-bottom: 8px;
                }

                .greeting {
                    color: #AFA2C8;
                    font-size: 14px;
                    margin-bottom: 28px;
                }

                .search-box {
                    width: 100%;
                    display: flex;
                    align-items: center;
                    background: rgba(255,255,255,0.07);
                    border: 1px solid rgba(194,166,255,0.35);
                    border-radius: 18px;
                    padding: 8px 10px 8px 22px;
                    backdrop-filter: blur(15px);
                    box-shadow: 0 15px 50px rgba(0,0,0,0.2);
                    transition: 0.3s;
                }

                .search-box:focus-within {
                    border-color: #B99AFF;
                    box-shadow: 0 0 25px rgba(185,154,255,0.15);
                }

                .search-icon {
                    color: #C9A8FF;
                    font-size: 23px;
                    margin-right: 12px;
                }

                input {
                    flex: 1;
                    background: transparent;
                    border: none;
                    outline: none;
                    color: white;
                    font-size: 16px;
                    padding: 13px 0;
                    min-width: 0;
                }

                input::placeholder {
                    color: #A49AB7;
                }

                .search-btn {
                    background: linear-gradient(
                        135deg,
                        #A980F3,
                        #7651BA
                    );
                    color: white;
                    border: none;
                    border-radius: 12px;
                    padding: 13px 23px;
                    font-size: 14px;
                    cursor: pointer;
                    transition: 0.3s;
                }

                .search-btn:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 5px 20px #7651BA55;
                }

                .quick-title {
                    color: #AFA2C8;
                    font-size: 12px;
                    letter-spacing: 3px;
                    margin-top: 50px;
                    margin-bottom: 22px;
                }

                .shortcuts {
                    display: flex;
                    justify-content: center;
                    flex-wrap: wrap;
                    gap: 20px;
                }

                .shortcut {
                    text-decoration: none;
                    color: #D9D0EB;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 10px;
                    font-size: 13px;
                    transition: 0.3s;
                }

                .shortcut:hover {
                    color: white;
                    transform: translateY(-5px);
                }

                .shortcut-icon {
                    width: 55px;
                    height: 55px;
                    border-radius: 17px;
                    background: rgba(255,255,255,0.07);
                    border: 1px solid rgba(194,166,255,0.2);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-size: 23px;
                }

                .footer {
                    position: absolute;
                    bottom: 25px;
                    color: #776D8C;
                    font-size: 12px;
                    letter-spacing: 1px;
                }

                @media(max-width: 600px) {
                    .top {
                        left: 20px;
                        right: 20px;
                    }

                    h1 {
                        letter-spacing: 6px;
                    }

                    .subtitle {
                        font-size: 11px;
                    }

                    .search-btn {
                        padding: 12px;
                    }
                }

            </style>
        </head>

        <body>

            <div class="top">
                <div class="logo-small">✦ EDITH</div>
                <div class="date" id="date"></div>
            </div>

            <div class="container">

                <div class="symbol">✦</div>

                <h1>EDITH</h1>

                <div class="subtitle">
                    YOUR SPACE. YOUR WORLD.
                </div>

                <div class="clock" id="clock">00:00:00</div>

                <div class="greeting">
                    A little space for everything.
                </div>

                <form class="search-box"
                      onsubmit="searchGoogle(event)">

                    <span class="search-icon">⌕</span>

                    <input
                        type="text"
                        id="search"
                        placeholder="What would you like to explore?"
                        autocomplete="off"
                        autofocus
                    >

                    <button class="search-btn" type="submit">
                        Explore →
                    </button>

                </form>

                <div class="quick-title">
                    QUICK ACCESS
                </div>

                <div class="shortcuts">

                    <a class="shortcut"
                       href="https://www.google.com">
                        <div class="shortcut-icon">G</div>
                        Google
                    </a>

                    <a class="shortcut"
                       href="https://www.youtube.com">
                        <div class="shortcut-icon">▶</div>
                        YouTube
                    </a>

                    <a class="shortcut"
                       href="https://github.com">
                        <div class="shortcut-icon">⌘</div>
                        GitHub
                    </a>

                    <a class="shortcut"
                       href="https://www.linkedin.com">
                        <div class="shortcut-icon">in</div>
                        LinkedIn
                    </a>

                    <a class="shortcut"
                       href="https://mail.google.com">
                        <div class="shortcut-icon">✉</div>
                        Gmail
                    </a>

                </div>

            </div>

            <div class="footer">
                ✦ DESIGNED TO EXPLORE ✦
            </div>

            <script>

                function updateClock() {
                    const now = new Date();

                    document.getElementById("clock")
                        .innerText = now.toLocaleTimeString(
                            "en-US",
                            {
                                hour: "2-digit",
                                minute: "2-digit",
                                second: "2-digit",
                                hour12: true
                            }
                        );

                    document.getElementById("date")
                        .innerText = now.toLocaleDateString(
                            "en-US",
                            {
                                weekday: "long",
                                month: "long",
                                day: "numeric",
                                year: "numeric"
                            }
                        );
                }

                function searchGoogle(event) {
                    event.preventDefault();

                    const query = document
                        .getElementById("search")
                        .value.trim();

                    if (query) {
                        window.location.href =
                            "https://www.google.com/search?q=" +
                            encodeURIComponent(query);
                    }
                }

                updateClock();
                setInterval(updateClock, 1000);

            </script>

        </body>
        </html>
        """

        self.browser.setHtml(
            html,
            QUrl("https://edith.local/")
        )

        self.url_bar.clear()
        self.setWindowTitle("Edith | Your Personal Browser")
        self.status.showMessage("✦ Welcome to Edith")

    # Navigate using address bar
    def navigate(self):

        text = self.url_bar.text().strip()

        if not text:
            return

        if " " in text or (
            "." not in text and not text.startswith("localhost")
        ):
            url = "https://www.google.com/search?q=" + QUrl.toPercentEncoding(text).data().decode()
        else:
            if not text.startswith(("https://", "http://")):
                text = "https://" + text

            url = text

        self.browser.setUrl(QUrl(url))

    # Update address bar
    def update_url(self, url):

        if url.host() == "edith.local":
            self.url_bar.clear()
        else:
            self.url_bar.setText(url.toString())

    # Loading progress
    def update_progress(self, value):

        self.progress.show()
        self.progress.setValue(value)

    def loading_started(self):

        self.status.showMessage("✦ Edith is exploring...")
        self.progress.show()

    def loading_finished(self, success):

        self.progress.hide()

        if success:
            self.status.showMessage("✦ Page loaded successfully", 3000)
        else:
            self.status.showMessage("Unable to load the page", 5000)

    # Update window title
    def update_title(self, title):

        if title:
            self.setWindowTitle(f"{title} | Edith")


# Application entry point
if __name__ == "__main__":

    app = QApplication(sys.argv)

    app.setApplicationName("Edith")
    app.setOrganizationName("Edith Studio")
    app.setFont(QFont("Segoe UI", 10))

    window = EdithBrowser()
    window.show()

    sys.exit(app.exec_())
