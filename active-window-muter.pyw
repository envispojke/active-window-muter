import sys
import ctypes
import comtypes
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer, QRect
from PySide6.QtGui import QFont, QPainter, QColor, QPen, QBrush

# ==========================================
#              CONFIGURATION
# ==========================================
ACTIVATION_DELAY_MS = 0          # Delay before grabbing the window (ms). Only useful for manual activation. 
DISPLAY_TIME_MS = 1500           # How long the UI stays on screen (milliseconds)

WINDOW_POSITION = "bottom-left"  # Options: 'top-left', 'top-right', 'bottom-left', 'bottom-right'
EDGE_MARGIN = 20                 # Distance from the edge of the screen (px)
WINDOW_WIDTH = 180               # Popup width (px)
WINDOW_HEIGHT = 48               # Popup height (px)
BG_COLOR = (30, 30, 30, 180)     # Background color in RGBA (0-255; red, green, blue, opacity)
BORDER_RADIUS = 8                # Corner radius for the popup (px)

FONT_FAMILY = "Consolas"         # Font style
BASE_FONT_SIZE = 12              # Base font size (pt)
USE_COLORED_TEXT = True          # True = Red/Green/Yellow text, False = White text
# ==========================================

def toggle_active_window_mute():
    comtypes.CoInitialize()
    user32 = ctypes.windll.user32
    hwnd = user32.GetForegroundWindow()
    
    if not hwnd:
        comtypes.CoUninitialize()
        return None

    pid = ctypes.c_ulong()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    
    sessions = AudioUtilities.GetAllSessions()
    new_state = None
    
    for session in sessions:
        if session.Process and session.Process.pid == pid.value:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            new_state = 0 if volume.GetMute() else 1
            volume.SetMute(new_state, None)
            break
            
    comtypes.CoUninitialize()
    return True if new_state == 1 else False if new_state == 0 else None


class NotificationBanner(QWidget):
    def __init__(self, mute_state):
        super().__init__()
        
        # Display text and font color
        if mute_state is True:
            self.msg, color = "🔇 Muted", "#ff6b6b"
            actual_font_size = BASE_FONT_SIZE
        elif mute_state is False:
            self.msg, color = "🔊 Unmuted", "#4dff88"
            actual_font_size = BASE_FONT_SIZE
        else:
            self.msg, color = "⚠️ No Audio Session", "#feca57"
            # Make text 2 points smaller to ensure it fits the box
            actual_font_size = max(1, BASE_FONT_SIZE - 2) 

        # Apply color toggle
        self.text_color = color if USE_COLORED_TEXT else "#ffffff"

        # Window Setup
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # Layout and Label
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        
        self.label = QLabel(self.msg, alignment=Qt.AlignmentFlag.AlignCenter)
        self.label.setFont(QFont(FONT_FAMILY, actual_font_size, QFont.Weight.Bold))
        self.label.setStyleSheet(f"color: {self.text_color}; background: transparent; border: none;")
        layout.addWidget(self.label)

        # Position Window based on configuration
        screen = QApplication.primaryScreen().availableGeometry()
        if WINDOW_POSITION == "top-left":
            self.move(screen.left() + EDGE_MARGIN, screen.top() + EDGE_MARGIN)
        elif WINDOW_POSITION == "top-right":
            self.move(screen.right() - self.width() - EDGE_MARGIN, screen.top() + EDGE_MARGIN)
        elif WINDOW_POSITION == "bottom-right":
            self.move(screen.right() - self.width() - EDGE_MARGIN, screen.bottom() - self.height() - EDGE_MARGIN)
        else: # Defaults to bottom-left
            self.move(screen.left() + EDGE_MARGIN, screen.bottom() - self.height() - EDGE_MARGIN)
        
        # Close after X ms
        app = QApplication.instance()
        if app is not None:
            QTimer.singleShot(DISPLAY_TIME_MS, app.quit)
        else:
            QTimer.singleShot(DISPLAY_TIME_MS, self.close)

    def paintEvent(self, event):
        """Manually paint the background"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background color (rgba)
        painter.setBrush(QBrush(QColor(*BG_COLOR)))
        painter.setPen(Qt.PenStyle.NoPen) 
        
        # Draw the rectangle with configured radius
        rect = self.rect().adjusted(0, 0, -1, -1)
        painter.drawRoundedRect(rect, BORDER_RADIUS, BORDER_RADIUS)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mute_state = toggle_active_window_mute()
    banner = NotificationBanner(mute_state)
    banner.show()
    sys.exit(app.exec())