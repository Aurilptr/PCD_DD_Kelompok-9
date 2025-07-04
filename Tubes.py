import sys
import os
from PyQt5 import QtWidgets, QtGui, uic
import cv2
import numpy as np

class DeteksiLubang(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("deteksi.ui", self)

        self.image_path = None

        self.btnLoad.clicked.connect(self.load_image)
        self.btnDetect.clicked.connect(self.detect_pothole)

        # Sesuaikan nama folder dataset sesuai dengan struktur kamu
        self.dataset_berlubang = "./dataset/positif"
        self.dataset_mulus = "./dataset/negatif"

    def load_image(self):
        fname, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', './test', "Image files (*.jpg *.png *.jpeg)")
        if fname:
            self.image_path = fname
            pixmap = QtGui.QPixmap(fname)
            self.labelGambar.setPixmap(pixmap.scaled(self.labelGambar.width(), self.labelGambar.height()))
            self.labelStatus.setText("Gambar berhasil dimuat.")

    def compare_histogram(self, img1, img2):
        hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
        cv2.normalize(hist1, hist1)
        cv2.normalize(hist2, hist2)
        similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        return similarity

    def is_berlubang(self, img_gray):
        similarities_berlubang = []
        similarities_mulus = []

        for filename in os.listdir(self.dataset_berlubang):
            path = os.path.join(self.dataset_berlubang, filename)
            ref_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            ref_img = cv2.resize(ref_img, (img_gray.shape[1], img_gray.shape[0]))
            sim = self.compare_histogram(img_gray, ref_img)
            similarities_berlubang.append(sim)

        for filename in os.listdir(self.dataset_mulus):
            path = os.path.join(self.dataset_mulus, filename)
            ref_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            ref_img = cv2.resize(ref_img, (img_gray.shape[1], img_gray.shape[0]))
            sim = self.compare_histogram(img_gray, ref_img)
            similarities_mulus.append(sim)

        max_sim_berlubang = max(similarities_berlubang) if similarities_berlubang else 0
        max_sim_mulus = max(similarities_mulus) if similarities_mulus else 0

        return max_sim_berlubang > max_sim_mulus

    def detect_pothole(self):
        if not self.image_path:
            self.labelStatus.setText("Harap load gambar terlebih dahulu.")
            return

        img = cv2.imread(self.image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Tampilkan hasil Canny ke labelGambar2
        try:
            canny = cv2.Canny(gray, 100, 200)
            canny_rgb = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)  # konversi ke RGB agar QImage bisa baca
            height, width, channel = canny_rgb.shape
            bytes_per_line = channel * width
            qImg = QtGui.QImage(canny_rgb.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
            pixmapCanny = QtGui.QPixmap.fromImage(qImg)

            if hasattr(self, "labelGambar2"):
                self.labelGambar2.setPixmap(pixmapCanny.scaled(self.labelGambar2.width(), self.labelGambar2.height()))
        except Exception as e:
            self.labelStatus.setText(f"Error saat menampilkan Canny: {e}")
            return

        if not self.is_berlubang(gray):
            self.labelStatus.setText("Gambar mirip jalan mulus, tidak ada lubang terdeteksi.")
            pixmap = QtGui.QPixmap(self.image_path)
            self.labelGambar.setPixmap(pixmap.scaled(self.labelGambar.width(), self.labelGambar.height()))
            return

        # Jika mirip berlubang, lanjut proses deteksi contour
        blur = cv2.GaussianBlur(gray, (7, 7), 0)
        _, thresh = cv2.threshold(blur, 100, 255, cv2.THRESH_BINARY_INV)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        count = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.putText(img, "Lubang", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                count += 1

        result_path = "result.jpg"
        cv2.imwrite(result_path, img)
        pixmap = QtGui.QPixmap(result_path)
        self.labelGambar.setPixmap(pixmap.scaled(self.labelGambar.width(), self.labelGambar.height()))

        if count == 0:
            self.labelStatus.setText("Tidak ditemukan lubang.")
        else:
            self.labelStatus.setText(f"Ditemukan {count} lubang.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = DeteksiLubang()
    window.show()
    sys.exit(app.exec_())
