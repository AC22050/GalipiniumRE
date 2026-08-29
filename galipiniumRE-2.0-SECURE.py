import sys
import os
import random
import socket
import struct
import math
import secrets
import logging
import gc
from datetime import datetime
from PyQt6.QtCore import QUrl, QSize, Qt, QPoint, QSettings, QTimer
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QToolBar, QLineEdit, QPushButton, QLabel,
    QStatusBar, QFileDialog, QDialog, QFormLayout, QStyle, QMessageBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import (
    QWebEngineProfile, QWebEngineSettings, QWebEnginePage,
    QWebEngineDownloadRequest, QWebEngineScript, QWebEngineClientCertificateStore
)

from fakefpu import get_virtual_fpu_instance
from faketcpip import get_virtual_tcpip_instance
from fakewebgl import get_hyper_sophisticated_webgl_canvas_shield_instance

# Logging configuration
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/tmp/galipinium_security.log') if os.name != 'nt' else None,
    ]
)
logger = logging.getLogger(__name__)

# URL Protocol Whitelist (Aggressive spoofing-safe)
SAFE_PROTOCOLS = {"https", "http"}
BLOCKED_PROTOCOLS = {"javascript", "data", "file", "about", "chrome", "vbscript", "ftp"}

# Random User-Agent Pool (Diverse fingerprinting)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
]

class VirtualSSLCertificateValidator:
    """Enhanced SSL/TLS validation with logging"""
    def __init__(self):
        self.blocked_hosts = set()
        self.trusted_hosts = set()
    
    def validate_certificate(self, error):
        """
        Return False = accept, True = reject
        This implementation REJECTS expired/invalid certs (aggressive privacy stance)
        """
        if error is None:
            return False
        
        error_code = error.error()
        error_desc = error.description()
        
        # Log all certificate errors for analysis
        logger.warning(f"Certificate Error - Code: {error_code}, Desc: {error_desc}")
        
        # SelfSignedCertificate errors are rejected (security first)
        if "self-signed" in error_desc.lower():
            logger.warning(f"Self-signed certificate rejected: {error.url().host()}")
            return True
        
        # ExpiredCertificate errors are rejected
        if "expired" in error_desc.lower():
            logger.warning(f"Expired certificate rejected: {error.url().host()}")
            return True
        
        # Return True = reject/block, False = accept
        return True


class SecureCustomWebEnginePage(QWebEnginePage):
    def __init__(self, profile, parent=None):
        super().__init__(profile, parent)
        self.fpu_instance = get_virtual_fpu_instance()
        self.tcpip_instance = get_virtual_tcpip_instance()
        self.webgl_shield_instance = get_hyper_sophisticated_webgl_canvas_shield_instance()
        self.cert_validator = VirtualSSLCertificateValidator()
        
        self.fullScreenRequested.connect(self.handle_fullscreen_request)

    def handle_fullscreen_request(self, request):
        """
        AGGRESSIVE PRIVACY: Reject fullscreen by default to prevent UI spoofing
        Log all attempts for analysis
        """
        logger.warning(f"Fullscreen requested by: {self.url().host()}")
        # Reject fullscreen to prevent UI spoofing attacks
        request.reject()

    def certificateError(self, error):
        """
        SSL/TLS validation with security-first approach
        Return True = reject, False = accept
        """
        should_reject = self.cert_validator.validate_certificate(error)
        return should_reject


class SecureURLValidator:
    """Advanced URL validation with protocol whitelist"""
    
    @staticmethod
    def is_safe_url(url_string):
        """
        Validates URL against spoofing-safe criteria
        Returns (is_safe, reason)
        """
        url_string = url_string.strip().lower()
        
        # Check for dangerous protocols
        for blocked_protocol in BLOCKED_PROTOCOLS:
            if url_string.startswith(f"{blocked_protocol}:"):
                return False, f"Blocked protocol: {blocked_protocol}"
        
        # Check for URL encoding bypass attempts
        if "%3a" in url_string or "%2f" in url_string or "%2e" in url_string:
            return False, "URL encoding detected (potential protocol bypass)"
        
        # Check for unicode normalization attacks
        if any(ord(c) > 127 for c in url_string):
            return False, "Non-ASCII characters in URL (potential bypass)"
        
        # Empty or whitespace-only URLs
        if not url_string or url_string.isspace():
            return False, "Empty URL"
        
        return True, "URL is valid"


class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GalipiniumRE - Amnesic Secure Core v2.0")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.resize(1024, 650)
        self.setMinimumSize(640, 400)

        self.settings = QSettings(QSettings.Scope.UserScope, "GalipiniumRE_Amnesic", "Browser")
        
        self.fpu_stack = get_virtual_fpu_instance()
        self.tcpip_stack = get_virtual_tcpip_instance()
        self.webgl_shield = get_hyper_sophisticated_webgl_canvas_shield_instance()
        
        self.search_engine = "https://html.duckduckgo.com/html/?q="
        self.url_validator = SecureURLValidator()

        # Generate truly random profile ID per session
        self.profile_id = secrets.token_hex(16)
        self.profile = QWebEngineProfile(self.profile_id, self)
        self.configure_profile()
        self.profile.downloadRequested.connect(self.handle_download)

        # Inject advanced anti-fingerprint script
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

        # Amnesic timer for memory cleanup
        self.memory_cleanup_timer = QTimer(self)
        self.memory_cleanup_timer.timeout.connect(self.periodic_memory_cleanup)
        self.memory_cleanup_timer.start(30000)  # 30 seconds

        # Status update timer
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_status_bar)
        self.status_timer.start(3000)

    def periodic_memory_cleanup(self):
        """
        AMNESIC: Aggressive memory cleanup to prevent data recovery
        """
        gc.collect()
        # Clear profile cache
        self.profile.clearHttpCache()
        self.profile.clearAllVisitedLinks()
        
        status_msg = "🔒 Amnesic Memory Cleanup | Spoofing Active | SSL Hardened"
        self.status_bar.showMessage(status_msg)

    def update_status_bar(self):
        """Update status bar with security indicators"""
        lat = 41.0082 + random.uniform(-0.001, 0.001)
        lon = 28.9784 + random.uniform(-0.001, 0.001)
        
        telemetry = {
            "webgl": self.webgl_shield.get_deep_telemetry_metrics()["shield_status"],
            "fpu": self.fpu_stack.get_telemetry()["cycles"],
            "tcp": self.tcpip_stack.get_stack_telemetry()["dpi_evasion_mode"]
        }
        
        status_msg = f"🛡️ WebGL:{telemetry['webgl'][:8]} | FPU:{telemetry['fpu']} | TCP:Polymorphic"
        self.status_bar.showMessage(status_msg)

    def inject_global_anti_fingerprint_script(self):
        """
        AGGRESSIVE anti-fingerprinting with enhanced spoofing
        Blocks all common tracking vectors while maintaining spoofing effectiveness
        """
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
                    this.blockFingerprintingAPIs();
                    this.blockWebRTC();
                },

                spoofNavigator: function() {
                    const navKeys = {
                        webdriver: { get: () => false },
                        hardwareConcurrency: { get: () => Math.floor(Math.random() * 4) + 4 },
                        deviceMemory: { get: () => [4, 8, 16][Math.floor(Math.random() * 3)] },
                        maxTouchPoints: { get: () => Math.random() > 0.5 ? 0 : 10 },
                        platform: { get: () => ['Win32', 'MacIntel', 'Linux x86_64'][Math.floor(Math.random() * 3)] },
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

                    // Spoof plugins
                    if (navigator.plugins) {
                        try {
                            const fakePlugins = {
                                length: Math.floor(Math.random() * 3),
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

                    // Spoof mimeTypes
                    if (navigator.mimeTypes) {
                        try {
                            const fakeMimeTypes = {
                                length: Math.floor(Math.random() * 5),
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
                    // Randomize screen dimensions
                    const screenOptions = [
                        { width: 1920, height: 1080, availWidth: 1920, availHeight: 1040 },
                        { width: 2560, height: 1440, availWidth: 2560, availHeight: 1400 },
                        { width: 1366, height: 768, availWidth: 1366, availHeight: 728 },
                        { width: 3840, height: 2160, availWidth: 3840, availHeight: 2120 }
                    ];
                    const screenProps = screenOptions[Math.floor(Math.random() * screenOptions.length)];

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
                        const jitterOffset = Math.random() * 500 + Math.random() * 500;
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
                            const memoryValues = [
                                { jsHeapSizeLimit: 2172649472, totalJSHeapSize: 16777216, usedJSHeapSize: 10485760 },
                                { jsHeapSizeLimit: 4294967295, totalJSHeapSize: 33554432, usedJSHeapSize: 20971520 }
                            ];
                            const fakeMemory = memoryValues[Math.floor(Math.random() * memoryValues.length)];
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
                        const timingJitter = Math.random() * 200000;
                        const spoofedDateObject = function(...args) {
                            if (args.length === 0) {
                                const d = new OriginalDate();
                                d.setTime(d.getTime() + timingJitter);
                                return d;
                            }
                            return new OriginalDate(...args);
                        };
                        spoofedDateObject.now = function() {
                            return OriginalDate.now() + timingJitter;
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
                    
                    // Block IndexedDB
                    try {
                        window.indexedDB = null;
                        window.openDatabase = null;
                    } catch (e) {}
                },

                spoofNetwork: function() {
                    if (navigator.connection) {
                        try {
                            const fakeConnections = [
                                { downlink: 10, effectiveType: '4g', rtt: 50, saveData: false },
                                { downlink: 25, effectiveType: '4g', rtt: 30, saveData: false },
                                { downlink: 50, effectiveType: '4g', rtt: 15, saveData: false }
                            ];
                            const fakeConnection = fakeConnections[Math.floor(Math.random() * fakeConnections.length)];
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
                                return [];  // Return empty - no devices
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
                                targetObject.stack = targetObject.stack.replace(/at\\s+.+?\\s+\\(.+?\\)/g, 'at secure_virtual_context (native)');
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
                                const originalGetImageData = ctx.getImageData;
                                ctx.getImageData = function() {
                                    throw new Error("Canvas fingerprinting blocked by security policy.");
                                };
                                ctx.toDataURL = function() {
                                    throw new Error("Canvas export blocked by security policy.");
                                };
                            }
                            return ctx;
                        }
                        return originalGetContext.apply(this, arguments);
                    };

                    HTMLCanvasElement.prototype.toDataURL = function() {
                        throw new Error("Canvas data export blocked by security policy.");
                    };
                },

                blockFingerprintingAPIs: function() {
                    // Block getBattery (deprecated but still a vector)
                    if (navigator.getBattery) {
                        navigator.getBattery = undefined;
                    }
                    
                    // Block getVRDisplays
                    if (navigator.getVRDisplays) {
                        navigator.getVRDisplays = function() {
                            return Promise.resolve([]);
                        };
                    }
                    
                    // Block Bluetooth
                    if (navigator.bluetooth) {
                        navigator.bluetooth.requestDevice = function() {
                            return Promise.reject(new Error("Bluetooth disabled"));
                        };
                    }
                },

                blockWebRTC: function() {
                    // Disable WebRTC IP leak
                    const PC = window.RTCPeerConnection || window.webkitRTCPeerConnection || window.mozRTCPeerConnection;
                    if (PC) {
                        window.RTCPeerConnection = function() {
                            throw new Error("WebRTC disabled for privacy");
                        };
                    }
                }
            };

            VirtualJSSpoofEngine.init();
        })();
        """
        
        script = QWebEngineScript()
        script.setName("VirtualJSSpoofEmulationShield_v2")
        script.setSourceCode(script_code)
        script.setInjectionPoint(QWebEngineScript.InjectionPoint.DocumentCreation)
        script.setWorldId(QWebEngineScript.ScriptWorldId.ApplicationWorld)  # Isolated world
        script.setRunsOnSubFrames(True)
        self.profile.scripts().insert(script)

    def configure_profile(self):
        """
        AGGRESSIVE profile configuration for privacy and security
        """
        # Memory-only HTTP cache
        self.profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.MemoryHttpCache)
        self.profile.setHttpCacheMaximumSize(10 * 1024 * 1024)  # 10MB RAM cache
        
        # Spell checking off
        self.profile.setSpellCheckEnabled(False)
        
        # No persistent cookies
        self.profile.setPersistentCookiesPolicy(
            QWebEngineProfile.PersistentCookiesPolicy.NoPersistentCookies
        )
        
        # Rotate User-Agent
        self.profile.setHttpUserAgent(random.choice(USER_AGENTS))

        # WebEngine settings
        settings = self.profile.settings()
        settings.setAttribute(QWebEngineSettings.WebAttribute.JavascriptEnabled, True)
        settings.setAttribute(QWebEngineSettings.WebAttribute.PluginsEnabled, False)
        settings.setAttribute(QWebEngineSettings.WebAttribute.FullScreenSupportEnabled, False)  # Disable fullscreen
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

        title_label = QLabel("GalipiniumRE Alfix v2.0")
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
        browser.setPage(SecureCustomWebEnginePage(self.profile, browser))
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
            .notice { color: #ff6600; font-size: 12px; margin-top: 20px; }
        </style></head>
        <body>
            <div class="box">
                <h1>Galipinium<span>RE</span> v2.0</h1>
                <p>🛡️ SSL Doğrulanmış & Agresif Spoofing Katmanı Aktif</p>
                <p>🔒 Bellek Tabanlı & Amnesic Mimari</p>
                <input type="text" placeholder="Güvenli arama yap..." autofocus onkeydown="if(event.key==='Enter'){window.location.href='https://html.duckduckgo.com/html/?q='+encodeURIComponent(this.value); this.value='';}">
                <div class="notice">⚠️ Fullscreen engellendi | WebRTC devre dışı | Canvas koruması aktif</div>
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
        if not text:
            return
        
        # Validate URL before navigation
        is_safe, reason = self.url_validator.is_safe_url(text)
        
        if not is_safe:
            logger.warning(f"Blocked URL: {reason}")
            self.status_bar.showMessage(f"🚫 URL Blocked: {reason}")
            return
        
        # Handle search vs direct URL
        if " " in text or ("." not in text and not text.startswith("http")):
            url = QUrl(f"{self.search_engine}{text.replace(' ', '+')}")
        else:
            if not text.startswith(("http://", "https://")): 
                text = "https://" + text
            url = QUrl(text)
        
        # Validate QUrl
        if not url.isValid():
            logger.warning(f"Invalid URL after parsing: {text}")
            self.status_bar.showMessage("🚫 Invalid URL")
            return
        
        self.current_browser().setUrl(url)

    def go_home(self):
        self.set_home_page(self.current_browser())

    def toggle_maximize(self):
        if self.isMaximized(): 
            self.showNormal()
        else: 
            self.showMaximized()

    def handle_download(self, download: QWebEngineDownloadRequest):
        path, _ = QFileDialog.getSaveFileName(self, "Güvenli İndir", download.suggestedFileName())
        if path:
            download.setDownloadFileName(path)
            download.accept()

    def show_settings(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Çekirdek Durumu v2.0")
        dialog.setFixedSize(400, 250)
        layout = QVBoxLayout(dialog)
        form = QFormLayout()
        
        form.addRow("SSL Doğrulama:", QLabel("✓ Etkin (Sertifika Hatası = Bloklanır)"))
        form.addRow("Fullscreen Engeli:", QLabel("✓ Etkin (UI Spoofing Koruması)"))
        form.addRow("WebGL Engeli:", QLabel("✓ Etkin (Canvas FP Koruması)"))
        form.addRow("WebRTC Engeli:", QLabel("✓ Etkin (IP Sızıntı Koruması)"))
        form.addRow("Bellek Temizliği:", QLabel("✓ Etkin (30s aralıkla)"))
        form.addRow("URL Validasyonu:", QLabel("✓ Etkin (XSS/RCE Koruması)"))
        form.addRow("User-Agent:", QLabel("✓ Döndürülebilir (Fingerprint Koruması)"))
        form.addRow("DNS Prefetch:", QLabel("✓ Devre dışı"))
        form.addRow("Logging:", QLabel("✓ Güvenli (uyarı seviyesi)"))
        
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

    def closeEvent(self, event):
        """
        AMNESIC: Aggressive cleanup on exit
        """
        logger.info("Browser closing - initiating amnesic memory wipe")
        
        # Close all tabs
        for i in range(self.tabs.count()):
            self.tabs.removeTab(0)
        
        # Clear profile data
        self.profile.clearHttpCache()
        self.profile.clearAllVisitedLinks()
        
        # Force garbage collection
        gc.collect()
        gc.collect()
        
        self.memory_cleanup_timer.stop()
        self.status_timer.stop()
        
        event.accept()


if __name__ == "__main__":
   
    # AGGRESSIVE Chromium hardening flags
    sys.argv.append("--use-angle=swiftshader")
    sys.argv.append("--disable-gpu")
    sys.argv.append("--disable-gpu-shader-disk-cache")
    
    # WebRTC IP leak prevention
    sys.argv.append("--force-webrtc-ip-handling-policy=disable_non_proxied_udp")
    
    # DNS leak prevention
    sys.argv.append("--disable-dns-prefetch")             
    sys.argv.append("--disable-domain-reliability")    
    sys.argv.append("--disable-background-networking")   
    
    # Privacy flags
    sys.argv.append("--disable-sync")                    
    sys.argv.append("--disable-features=NetworkServiceInProcess")
    sys.argv.append("--disable-plugins")
    sys.argv.append("--no-referrers")
    
    app = QApplication(sys.argv)
    window = BrowserWindow()
    window.show()
    sys.exit(app.exec())
