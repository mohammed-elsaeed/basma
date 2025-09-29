#https://www.figma.com/proto/cWjiwZcAtOSbPgGzLJWaa4/Bassma?node-id=1-1588&p=f&t=p68Q6CnC7tpdIyrj-1&scaling=scale-down&content-scaling=fixed&page-id=0%3A1&starting-point-node-id=1%3A1588
import sys
import os
import json
import cv2
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QMessageBox,
    QLabel, QListWidget, QDialog, QHBoxLayout, QListWidgetItem, QScrollArea, QFrame
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

DATA_FILE = "reports.json"
SAVE_DIR = "reports_images"

# إنشاء مجلد لحفظ الصور الملتقطة
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

class ReportApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌍 بصمة - للحفاظ على البيئة")
        self.setGeometry(300, 200, 500, 400)
        self.setStyleSheet("background-color: #f0f8f5;")

        layout = QVBoxLayout()

        # شعار
        title = QLabel("🌱 تطبيق بصمة")
        title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2e7d32; margin: 10px;")
        layout.addWidget(title)

        # زر إرسال بلاغ
        self.btn_report = QPushButton("إرسال بلاغ 📷")
        self.btn_report.setStyleSheet("background-color: #4caf50; color: white; padding: 10px; font-size: 16px; border-radius: 10px;")
        self.btn_report.clicked.connect(self.send_report)

        # زر متابعة البلاغات
        self.btn_follow = QPushButton("متابعة البلاغات 📑")
        self.btn_follow.setStyleSheet("background-color: #2196f3; color: white; padding: 10px; font-size: 16px; border-radius: 10px;")
        self.btn_follow.clicked.connect(self.view_reports)

        layout.addWidget(self.btn_report)
        layout.addWidget(self.btn_follow)

        self.setLayout(layout)

    def send_report(self):
        choice = QMessageBox.question(self, "اختيار",
                                      "هل تريد التصوير بالكاميرا (نعم) أم اختيار صورة (لا)؟",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if choice == QMessageBox.StandardButton.Yes:
            self.capture_camera()
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "اختر صورة", "", "Images (*.png *.jpg *.jpeg)")
            if file_path:
                self.save_report(file_path)
                QMessageBox.information(self, "تم", "✅ تم حفظ البلاغ بنجاح")

    def capture_camera(self):
        cap = cv2.VideoCapture(0)  # فتح الكاميرا
        if not cap.isOpened():
            QMessageBox.warning(self, "خطأ", "⚠️ لا يمكن فتح الكاميرا")
            return
        
        ret, frame = cap.read()
        if ret:
            file_name = datetime.now().strftime("%Y%m%d%H%M%S") + ".jpg"
            file_path = os.path.join(SAVE_DIR, file_name)
            cv2.imwrite(file_path, frame)
            self.save_report(file_path)
            QMessageBox.information(self, "تم", "✅ تم التقاط الصورة وحفظ البلاغ")
        cap.release()
        cv2.destroyAllWindows()

    def save_report(self, image_path):
        report = {
            "id": datetime.now().strftime("%Y%m%d%H%M%S"),
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "image": image_path,
            "status": "قيد المراجعة"
        }

        data = []
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

        data.append(report)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def view_reports(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("📑 متابعة البلاغات")
        dialog.setGeometry(350, 250, 600, 500)
        dialog.setStyleSheet("background-color: #ffffff;")

        layout = QVBoxLayout()

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        vbox = QVBoxLayout()

        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                for report in data:
                    frame = QFrame()
                    frame.setFrameShape(QFrame.Shape.StyledPanel)
                    frame.setStyleSheet("background-color: #f9f9f9; border-radius: 8px; margin: 5px; padding: 5px;")

                    hbox = QHBoxLayout()

                    # الصورة
                    pixmap = QPixmap(report['image']).scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio)
                    img_label = QLabel()
                    img_label.setPixmap(pixmap)

                    # التفاصيل
                    text = QLabel(f"بلاغ رقم: {report['id']}\nالتاريخ: {report['date']}\nالحالة: {report['status']}")
                    text.setStyleSheet("font-size: 14px; color: #333;")

                    hbox.addWidget(img_label)
                    hbox.addWidget(text)
                    frame.setLayout(hbox)

                    vbox.addWidget(frame)

        container.setLayout(vbox)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        dialog.setLayout(layout)
        dialog.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportApp()
    window.show()
    sys.exit(app.exec())
