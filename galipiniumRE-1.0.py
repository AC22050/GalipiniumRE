import sys
import os
import random
import socket
import struct
import math
from datetime import datetime
from PyQt6.QtCore import QUrl, QSize, Qt, QPoint, QSettings, QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QToolBar, QLineEdit, QPushButton, QLabel,
    QStatusBar, QFileDialog, QDialog, QFormLayout, QStyle
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import (
    QWebEngineProfile, QWebEngineSettings, QWebEnginePage,
    QWebEngineDownloadRequest, QWebEngineScript
)

from fakefpu import get_virtual_fpu_instance
from faketcpip import get_virtual_tcpip_instance
from fakewebgl import get_hyper_sophisticated_webgl_canvas_shield_instance

class CustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.fpu_instance = get_virtual_fpu_instance()
        self.tcpip_instance = get_virtual_tcpip_instance()
        self.webgl_shield_instance = get_hyper_sophisticated_webgl_canvas_shield_instance()
        self.fullScreenRequested.connect(self.handle_fullscreen)

    def handle_fullscreen(self, request):
        request.accept()

    def certificateError(self, error):
        return False


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GalipiniumRE - Amnesic Secure Core")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(1024, 650)
        self.setMinimumSize(640, 400)

        self.settings = QSettings(QSettings.Scope.UserScope, "GalipiniumRE_Amnesic", "Browser")
        
        self.fpu_stack = get_virtual_fpu_instance()
        self.tcpip_stack = get_virtual_tcpip_instance()
        self.webgl_shield = get_hyper_sophisticated_webgl_canvas_shield_instance()
        
        self.search_engine = "https://html.duckduckgo.com/html/?q="

        self.profile = QWebEngineProfile(str(random.randint(10000, 99999)), self)
        self.configure_profile()
        self.profile.downloadRequested.connect(self.handle_download)

        self.inject_global_anti_fingerprint_script()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.title_bar = self.create_title_bar()
        main_layout.addWidget(self.title_bar)

        self.toolbar = self.create_toolbar()
        main_layout.addWidget(self.toolbar)

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.setDocumentMode(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self.tab_changed)
        main_layout.addWidget(self.tabs, 1)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.apply_stylesheet()
        self.add_new_tab()

        self.url_bar.returnPressed.connect(self.navigate_to_url)

        self.nmea_timer = QTimer(self)
        self.nmea_timer.timeout.connect(self.feed_realtime_nmea)
        self.nmea_timer.start(3000)

    def inject_global_anti_fingerprint_script(self):
        script_code = """
        (function() {
            'use strict';

            const VirtualJSSpoofEngine = {
                init: function() {
                    this.spoofNavigator();
                    this.spoofScreen();
                    this.spoofPerformance();
                    this.spoofTiming();
                    this.spoofStorage();
                    this.spoofNetwork();
                    this.spoofMedia();
                    this.spoofErrors();
                    this.spoofWebGLCanvas();
                },

                spoofNavigator: function() {
                    const navKeys = {
                        webdriver: { get: () => false },
                        hardwareConcurrency: { get: () => 8 },
                        deviceMemory: { get: () => 8 },
                        maxTouchPoints: { get: () => 0 },
                        platform: { get: () => 'Win32' },
                        vendor: { get: () => 'Google Inc.' },
                        vendorSub: { get: () => '' },
                        product: { get: () => 'Gecko' },
                        productSub: { get: () => '20030107' },
                        languages: { get: () => ['en-US', 'en'] },
                        language: { get: () => 'en-US' },
                        doNotTrack: { get: () => null },
                        cookieEnabled: { get: () => true },
                        onLine: { get: () => true }
                    };

                    for (const [key, descriptor] of Object.entries(navKeys)) {
                        try {
                            Object.defineProperty(navigator, key, {
                                get: descriptor.get,
                                enumerable: true,
                                configurable: true
                            });
                        } catch (e) {}
                    }

                    if (navigator.plugins) {
                        try {
                            const fakePlugins = {
                                length: 0,
                                item: function(index) { return null; },
                                namedItem: function(name) { return null; },
                                refresh: function() {}
                            };
                            Object.defineProperty(navigator, 'plugins', {
                                get: () => fakePlugins,
                                enumerable: true,
                                configurable: true
                            });
                        } catch (e) {}
                    }

                    if (navigator.mimeTypes) {
                        try {
                            const fakeMimeTypes = {
                                length: 0,
                                item: function(index) { return null; },
                                namedItem: function(name) { return null; }
                            };
                            Object.defineProperty(navigator, 'mimeTypes', {
                                get: () => fakeMimeTypes,
                                enumerable: true,
                                configurable: true
                            });
                        } catch (e) {}
                    }
                },

                spoofScreen: function() {
                    const screenProps = {
                        width: 1920,
                        height: 1080,
                        availWidth: 1920,
                        availHeight: 1040,
                        colorDepth: 24,
                        pixelDepth: 24
                    };

                    for (const [key, val] of Object.entries(screenProps)) {
                        try {
                            Object.defineProperty(screen, key, {
                                get: () => val,
                                enumerable: true,
                                configurable: true
                            });
                        } catch (e) {}
                    }
                },

                spoofPerformance: function() {
                    if (window.performance && window.performance.now) {
                        const originalNow = window.performance.now.bind(window.performance);
                        const jitterOffset = Math.random() * 0.05;
                        try {
                            Object.defineProperty(window.performance, 'now', {
                                value: function() {
                                    return originalNow() + jitterOffset;
                                },
                                writable: true,
                                configurable: true
                            });
                        } catch (e) {}
                    }

                    if (window.performance && window.performance.memory) {
                        try {
                            const fakeMemory = {
                                jsHeapSizeLimit: 2172649472,
                                totalJSHeapSize: 16777216,
                                usedJSHeapSize: 10485760
                            };
                            Object.defineProperty(window.performance, 'memory', {
                                get: () => fakeMemory,
                                enumerable: true,
                                configurable: true
                            });
                        } catch (e) {}
                    }
                },

                spoofTiming: function() {
                    if (window.Date) {
                        const OriginalDate = window.Date;
                        const spoofedDateObject = function(...args) {
                            if (args.length === 0) {
                                const d = new OriginalDate();
                                return d;
                            }
                            return new OriginalDate(...args);
                        };
                        spoofedDateObject.now = function() {
                            return OriginalDate.now();
                        };
                        spoofedDateObject.parse = OriginalDate.parse;
                        spoofedDateObject.UTC = OriginalDate.UTC;
                        window.Date = spoofedDateObject;
                    }
                },

                spoofStorage: function() {
                    try {
                        const dummyStorage = {
                            getItem: function(key) { return null; },
                            setItem: function(key, val) {},
                            removeItem: function(key) {},
                            clear: function() {},
                            key: function(index) { return null; },
                            length: 0
                        };
                        Object.defineProperty(window, 'localStorage', {
                            get: () => dummyStorage,
                            configurable: true
                        });
                        Object.defineProperty(window, 'sessionStorage', {
                            get: () => dummyStorage,
                            configurable: true
                        });
                    } catch (e) {}
                },

                spoofNetwork: function() {
                    if (navigator.connection) {
                        try {
                            const fakeConnection = {
                                downlink: 10,
                                effectiveType: '4g',
                                rtt: 50,
                                saveData: false
                            };
                            Object.defineProperty(navigator, 'connection', {
                                get: () => fakeConnection,
                                enumerable: true,
                                configurable: true
                            });
                        } catch (e) {}
                    }
                },

                spoofMedia: function() {
                    if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
                        try {
                            navigator.mediaDevices.enumerateDevices = async function() {
                                return [
                                    {deviceId: 'default', kind: 'audioinput', label: 'Default Audio Input', groupId: 'default'},
                                    {deviceId: 'default', kind: 'videoinput', label: 'Default Video Input', groupId: 'default'}
                                ];
                            };
                        } catch (e) {}
                    }
                },

                spoofErrors: function() {
                    const originalErrorCaptureStackTrace = Error.captureStackTrace;
                    if (originalErrorCaptureStackTrace) {
                        Error.captureStackTrace = function(targetObject, constructorOpt) {
                            originalErrorCaptureStackTrace(targetObject, constructorOpt);
                            if (targetObject && targetObject.stack) {
                                targetObject.stack = targetObject.stack.replace(/at\s+.+?\s+\(.+?\)/g, 'at secure_context (native)');
                            }
                        };
                    }
                },

                spoofWebGLCanvas: function() {
                    try {
                        delete window.WebGLRenderingContext;
                        delete window.WebGL2RenderingContext;
                    } catch (e) {}

                    const originalGetContext = HTMLCanvasElement.prototype.getContext;
                    HTMLCanvasElement.prototype.getContext = function(contextType) {
                        if (contextType && (contextType.includes('webgl') || contextType.includes('experimental-webgl'))) {
                            return null;
                        }
                        if (contextType === '2d') {
                            const ctx = originalGetContext.apply(this, arguments);
                            if (ctx) {
                                ctx.getImageData = function() {
                                    throw new Error("getImageData blocked by security policy.");
                                };
                            }
                            return ctx;
                        }
                        return originalGetContext.apply(this, arguments);
                    };

                    HTMLCanvasElement.prototype.toDataURL = function() {
                        throw new Error("Canvas data export blocked by security policy.");
                    };
                }
            };

            VirtualJSSpoofEngine.init();
        })();
        """
        
        script = QWebEngineScript()
        script.setName("VirtualJSSpoofEmulationShield")
        script.setSourceCode(script_code)
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        script.setWorldId(QWebEngineScript.ScriptWorldId.MainWorld)
        script.setRunsOnSubFrames(True)
        self.profile.scripts().insert(script)

    def feed_realtime_nmea(self):
        lat = 41.0082 + random.uniform(-0.001, 0.001)
        lon = 28.9784 + random.uniform(-0.001, 0.001)
        self.status_bar.showMessage("Amnesic Mod | JS Spoofer & WebGL Kapalı & DNS Sızıntısı Korumalı |")

    def configure_profile(self):
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)
        self.profile.setHttpCacheMaximumSize(0)
        self.profile.setSpellCheckEnabled(False)
        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies
        )
        self.profile.setHttpUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")

        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.LocalStorageEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.AutoLoadImages, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.ReadingFromCanvasEnabled, False)

    def create_title_bar(self):
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(30)
        layout = QHBoxLayout(title_bar)
        layout.setContentsMargins(8, 0, 0, 0)
        layout.setSpacing(0)

        title_label = QLabel("GalipiniumRE Alfix")
        title_label.setObjectName("titleLabel")
        layout.addWidget(title_label)
        layout.addStretch(1)

        self.minimize_button = QPushButton("—")
        self.minimize_button.setObjectName("windowButton")
        self.minimize_button.setFixedSize(35, 30)
        self.minimize_button.clicked.connect(self.showMinimized)
        layout.addWidget(self.minimize_button)

        self.maximize_button = QPushButton("☐")
        self.maximize_button.setObjectName("windowButton")
        self.maximize_button.setFixedSize(35, 30)
        self.maximize_button.clicked.connect(self.toggle_maximize)
        layout.addWidget(self.maximize_button)

        self.close_button = QPushButton("✕")
        self.close_button.setObjectName("closeButton")
        self.close_button.setFixedSize(35, 30)
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        return title_bar

    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(14, 14))
        toolbar.setFixedHeight(38)
        toolbar.setObjectName("mainToolbar")

        self.back_action = QAction(self)
        self.back_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowBack))
        self.back_action.triggered.connect(lambda: self.current_browser().back())
        toolbar.addAction(self.back_action)

        self.forward_action = QAction(self)
        self.forward_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ArrowForward))
        self.forward_action.triggered.connect(lambda: self.current_browser().forward())
        toolbar.addAction(self.forward_action)

        self.reload_action = QAction(self)
        self.reload_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_BrowserReload))
        self.reload_action.triggered.connect(lambda: self.current_browser().reload())
        toolbar.addAction(self.reload_action)

        self.home_action = QAction(self)
        self.home_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_DirHomeIcon))
        self.home_action.triggered.connect(self.go_home)
        toolbar.addAction(self.home_action)

        toolbar.addSeparator()

        self.url_bar = QLineEdit()
        self.url_bar.setObjectName("urlBar")
        self.url_bar.setClearButtonEnabled(True)
        toolbar.addWidget(self.url_bar)

        self.new_tab_action = QAction(self)
        self.new_tab_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon))
        self.new_tab_action.triggered.connect(lambda: self.add_new_tab())
        toolbar.addAction(self.new_tab_action)

        self.settings_action = QAction(self)
        self.settings_action.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView))
        self.settings_action.triggered.connect(self.show_settings)
        toolbar.addAction(self.settings_action)

        return toolbar

    def current_browser(self) -> QWebEngineView:
        return self.tabs.currentWidget()

    def add_new_tab(self, qurl=None, label="Güvenli Sekme"):
        browser = QWebEngineView()
        browser.setPage(CustomWebEnginePage(self.profile, browser))
        if qurl is None:
            self.set_home_page(browser)
        else:
            browser.setUrl(qurl)

        browser.page().titleChanged.connect(lambda title, b=browser: self.update_tab_title(b, title))
        browser.page().urlChanged.connect(lambda url, b=browser: self.update_url_bar(b, url))
        
        index = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(index)
        self.url_bar.setText(browser.url().toString())
        return browser

    def set_home_page(self, browser):
        html = """
        <!DOCTYPE html>
        <html>
        <head><meta charset="UTF-8"><style>
            body { background: #050505; color: #00ff66; font-family: monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .box { text-align: center; }
            h1 { font-size: 28px; text-shadow: 0 0 10px rgba(0,255,102,0.4); }
            input { background: #111; border: 1px solid #333; color: #00ff66; padding: 10px; width: 400px; border-radius: 4px; outline: none; }
        </style></head>
        <body>
            <div class="box">
                <h1>Galipinium<span>RE</span></h1>
                <p>DNS Sızıntı Kalkanı & Sanal JS Emülasyon Katmanı Aktif</p>
                <input type="text" placeholder="Güvenli arama yap..." autofocus onkeydown="if(event.key==='Enter'){window.location.href='https://html.duckduckgo.com/html/?q='+encodeURIComponent(this.value);}">
            </div>
        </body>
        </html>
        """
        browser.setHtml(html, QUrl("https://galipinium.amnesic/"))

    def close_tab(self, index):
        if self.tabs.count() == 1:
            self.add_new_tab()
            self.tabs.removeTab(0)
        else:
            self.tabs.removeTab(index)

    def tab_changed(self, index):
        if index >= 0:
            browser = self.tabs.widget(index)
            if browser:
                self.url_bar.setText(browser.url().toString())

    def update_tab_title(self, browser, title):
        index = self.tabs.indexOf(browser)
        if index >= 0:
            self.tabs.setTabText(index, title[:14] + "..." if len(title) > 14 else title)

    def update_url_bar(self, browser, url):
        if browser == self.current_browser():
            self.url_bar.setText(url.toString())

    def navigate_to_url(self):
        text = self.url_bar.text().strip()
        if not text: return
        if " " in text or "." not in text:
            url = QUrl(f"{self.search_engine}{text.replace(' ', '+')}")
        else:
            if not text.startswith(("http://", "https://")): text = "https://" + text
            url = QUrl(text)
        self.current_browser().setUrl(url)

    def go_home(self):
        self.set_home_page(self.current_browser())

    def toggle_maximize(self):
        if self.isMaximized(): self.showNormal()
        else: self.showMaximized()

    def handle_download(self, download: QWebEngineDownloadRequest):
        path, _ = QFileDialog.getSaveFileName(self, "Güvenli İndir", download.suggestedFileName())
        if path:
            download.setDownloadFileName(path)
            download.accept()

    def show_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Çekirdek Durumu")
        dialog.setFixedSize(350, 200)
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        form.addRow("DNS Sızıntı Kalkanı:", QLabel("Aktif (Prefetch & Background Kilitli)"))
        form.addRow("JS Emülasyon Katmanı:", QLabel("Aktif (Virtual Spoof Emulation)"))
        form.addRow("WebRTC Politika:", QLabel("Non-Proxied UDP Engellendi"))
        layout.addLayout(form)
        btn = QPushButton("Kapat")
        btn.clicked.connect(dialog.accept)
        layout.addWidget(btn)
        dialog.exec()

    def apply_stylesheet(self):
        self.setStyleSheet("""
            QMainWindow { background-color: #080808; }
            #titleBar { background-color: #0d0d0d; border-bottom: 1px solid #1a1a1a; }
            #titleLabel { color: #00ff66; font-weight: bold; font-size: 11px; font-family: monospace; }
            #windowButton, #closeButton { background-color: transparent; color: #666; border: none; }
            #closeButton:hover { background-color: #cc0000; color: #fff; }
            #mainToolbar { background-color: #0d0d0d; border-bottom: 1px solid #1a1a1a; }
            #urlBar { background-color: #030303; border: 1px solid #222; border-radius: 3px; color: #00ff66; font-family: monospace; padding: 3px; }
            QStatusBar { background: #0d0d0d; color: #666; font-family: monospace; }
        """)


if __name__ == "__main__":
   
    sys.argv.append("--use-angle=swiftshader")
    sys.argv.append("--disable-gpu")
    sys.argv.append("--disable-gpu-shader-disk-cache")
    sys.argv.append("--enable-unsafe-swiftshader")
    
    sys.argv.append("--force-webrtc-ip-handling-policy=disable_non_proxied_udp")
    sys.argv.append("--disable-dns-prefetch")             
    sys.argv.append("--disable-domain-reliability")    
    sys.argv.append("--disable-background-networking")   
    sys.argv.append("--disable-sync")                    
    sys.argv.append("--disable-features=NetworkServiceInProcess")
    
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())
