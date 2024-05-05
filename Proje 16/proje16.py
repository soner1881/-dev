import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QComboBox, QDialog
from PyQt5.QtGui import QIcon 

class GirisPenceresi(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
                color: #333333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit, QTextEdit {
                border: 2px solid #4CAF50;
                padding: 5px;
            }
            QLabel {
                font-size: 16px;
            }
        """)
        self.setWindowTitle("Giriş")
        self.setGeometry(200, 200, 300, 150)

        self.kullanici_adi_etiketi = QLabel("Kullanıcı Adı:")
        self.kullanici_adi_girdisi = QLineEdit()
        self.sifre_etiketi = QLabel("Şifre:")
        self.sifre_girdisi = QLineEdit()
        self.sifre_girdisi.setEchoMode(QLineEdit.Password)
        self.giris_butonu = QPushButton("Giriş")
        self.giris_butonu.clicked.connect(self.giris)

        layout = QVBoxLayout()
        layout.addWidget(self.kullanici_adi_etiketi)
        layout.addWidget(self.kullanici_adi_girdisi)
        layout.addWidget(self.sifre_etiketi)
        layout.addWidget(self.sifre_girdisi)
        layout.addWidget(self.giris_butonu)

        self.setLayout(layout)

    def giris(self):
        kullanici_adi = self.kullanici_adi_girdisi.text()
        sifre = self.sifre_girdisi.text()

        if kullanici_adi == "admin" and sifre == "admin":
            self.close()
            self.anasayfa_penceresi = AnaSayfaPenceresi()
            self.anasayfa_penceresi.show()
        else:
            QMessageBox.warning(self, "Giriş Başarısız", "Geçersiz kullanıcı adı veya şifre")

class AnaSayfaPenceresi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Film ve Dizi İzleme Servisi")
        self.setGeometry(200, 200, 500, 300)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
                color: #333333;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QLineEdit, QTextEdit {
                border: 2px solid #4CAF50;
                padding: 5px;
            }
            QLabel {
                font-size: 16px;
            }
        """)

        self.enstrumanlar = {
            "Aslan Kral": {"puan": 10},
            "Arınma Gecesi": {"puan": 10},
            "Labirent": {"puan": 10}
        }

        self.stok_label = QLabel("Filmler:")
        self.stok_combo = QComboBox()
        self.stok_combo.addItems(self.enstrumanlar.keys())
        self.stok_combo.currentIndexChanged.connect(self.stok_miktarini_guncelle)

        self.stok_miktari_label = QLabel("IMDB:")
        self.stok_miktari_goster = QLabel(str(self.enstrumanlar[self.stok_combo.currentText()]["puan"]))

        self.stok_artir_label = QLabel("IMDB Puan Güncelle:")
        self.stok_artir_input = QLineEdit()

        self.stok_guncelle_butonu = QPushButton("Puan Güncelle")
        self.stok_guncelle_butonu.clicked.connect(self.stok_guncelle)

        self.yorumlar_butonu = QPushButton("Yorumları Görüntüle")
        self.yorumlar_butonu.clicked.connect(self.yorumlari_goruntule)

        self.yorum_yap_butonu = QPushButton("Yorum Yap")
        self.yorum_yap_butonu.clicked.connect(self.yorum_yap_dialog)

        self.film_ekle_butonu = QPushButton("Film Ekle")
        self.film_ekle_butonu.clicked.connect(self.film_ekle_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.stok_label)
        layout.addWidget(self.stok_combo)
        layout.addWidget(self.stok_miktari_label)
        layout.addWidget(self.stok_miktari_goster)
        layout.addWidget(self.stok_artir_label)
        layout.addWidget(self.stok_artir_input)
        layout.addWidget(self.stok_guncelle_butonu)
        layout.addWidget(self.yorumlar_butonu)
        layout.addWidget(self.yorum_yap_butonu)
        layout.addWidget(self.film_ekle_butonu)

        self.setLayout(layout)

    def stok_guncelle(self):
        secilen_film = self.stok_combo.currentText()
        yeni_puan = str(self.stok_artir_input.text())
        yeni_puan = min(10, int(yeni_puan))  # En fazla 10 yap
        self.enstrumanlar[secilen_film]["puan"] = yeni_puan
        self.stok_miktari_goster.setText(str(yeni_puan))

    def stok_miktarini_guncelle(self):
        secilen_film = self.stok_combo.currentText()
        mevcut_puan = self.enstrumanlar[secilen_film]["puan"]
        self.stok_miktari_goster.setText(str(mevcut_puan))

    def yorumlari_goruntule(self):
        if not os.path.exists("yorumlar.txt"):
            QMessageBox.information(self, "Yorumlar", "Henüz yorum bulunmamaktadır.")
        else:
            with open("yorumlar.txt", "r") as dosya:
                yorumlar = dosya.read()
                QMessageBox.information(self, "Yorumlar", yorumlar)
      
    def yorum_yap_dialog(self):  
        dialog = YorumYapDialog(self.enstrumanlar, self)
        dialog.exec_()

    def film_ekle_dialog(self):
        dialog = FilmEkleDialog(self.enstrumanlar, self)
        dialog.exec_()

class YorumYapDialog(QDialog):
    def __init__(self, enstrumanlar, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Yorum Yap")
        self.setGeometry(300, 300, 300, 200)
        self.enstrumanlar = enstrumanlar
        self.parent = parent

        self.enstruman_label = QLabel("Film Seç:")
        self.enstruman_combo = QComboBox()
        self.enstruman_combo.addItems(self.enstrumanlar.keys())

        self.isim_label = QLabel("İsim:")
        self.isim_input = QLineEdit()

        self.yorum_label = QLabel("Yorum:")
        self.yorum_input = QLineEdit()

        self.yorum_button = QPushButton("Yorum Yap")
        self.yorum_button.clicked.connect(self.yorum_yap)

        layout = QVBoxLayout()
        layout.addWidget(self.enstruman_label)
        layout.addWidget(self.enstruman_combo)
        layout.addWidget(self.isim_label)
        layout.addWidget(self.isim_input)
        layout.addWidget(self.yorum_label)
        layout.addWidget(self.yorum_input)
        layout.addWidget(self.yorum_button)

        self.setLayout(layout)

    def yorum_yap(self):
        film = self.enstruman_combo.currentText()
        isim = self.isim_input.text()
        yorum = self.yorum_input.text()

        with open("yorumlar.txt", "a") as dosya:
            dosya.write(f"\n{film} - {isim}: {yorum}")

        QMessageBox.information(self, "Yorum Bilgisi", "Yorumunuz başarıyla kaydedildi.")

class FilmEkleDialog(QDialog):
    def __init__(self, enstrumanlar, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Film Ekle")
        self.setGeometry(300, 300, 300, 150)
        self.enstrumanlar = enstrumanlar
        self.parent = parent

        self.enstruman_ad_label = QLabel("Film Adı:")
        self.enstruman_ad_input = QLineEdit()

        self.puan_label = QLabel("IMDB Puanı:")
        self.puan_input = QLineEdit()

        self.ekle_button = QPushButton("Film Ekle")
        self.ekle_button.clicked.connect(self.film_ekle)

        layout = QVBoxLayout()
        layout.addWidget(self.enstruman_ad_label)
        layout.addWidget(self.enstruman_ad_input)
        layout.addWidget(self.puan_label)
        layout.addWidget(self.puan_input)
        layout.addWidget(self.ekle_button)

        self.setLayout(layout)

    def film_ekle(self):
        film_ad = self.enstruman_ad_input.text()
        puan = str(self.puan_input.text())
        puan = min(10, int(puan))  # En fazla 10 yap

        if film_ad in self.enstrumanlar:
            QMessageBox.warning(self, "Film Zaten Var", "Bu film zaten mevcut!")
            return

        self.enstrumanlar[film_ad] = {"puan": puan}
        self.parent.stok_combo.addItem(film_ad)
        QMessageBox.information(self, "Film Eklendi", f"{film_ad} filmi başarıyla eklendi!")
        self.close()

if __name__ == "__main__":
    uygulama = QApplication(sys.argv)
    giris_penceresi = GirisPenceresi()
    giris_penceresi.show()
    sys.exit(uygulama.exec_())
