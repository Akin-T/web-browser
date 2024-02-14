import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from pymongo import MongoClient
import socket
from threading import Thread

class AnaEkran(QMainWindow):
    def __init__(self):
        super(AnaEkran, self).__init__()

        self.tarayici = QWebEngineView()
        self.tarayici.setUrl(QUrl('http://google.com'))
        self.setCentralWidget(self.tarayici)

        geri_git_buton = QAction('<', self)
        geri_git_buton.setStatusTip('Sayfaya Geri Git')
        geri_git_buton.triggered.connect(self.tarayici.back)

        sayfa_geri_don_buton = QAction('>', self)
        sayfa_geri_don_buton.setStatusTip('Sayfada İleri Git')
        sayfa_geri_don_buton.triggered.connect(self.ana_sayfaya_don)

        tara_buton = QAction('Port Tara', self)
        tara_buton.setStatusTip('Portları Tara')
        tara_buton.triggered.connect(self.port_tara)

        google_git_buton = QAction('Google\'a Git', self)
        google_git_buton.setStatusTip('Google Ana Sayfasına Git')
        google_git_buton.triggered.connect(lambda: self.tarayici.setUrl(QUrl('http://google.com')))

        arac_cubugu = self.addToolBar("Navigation")
        arac_cubugu.addAction(geri_git_buton)
        arac_cubugu.addAction(sayfa_geri_don_buton)
        arac_cubugu.addAction(tara_buton)
        arac_cubugu.addAction(google_git_buton)

        self.showMaximized()

        # DATABASE BAĞLANTISI
        self.mongo_client = MongoClient('mongodb://localhost:27017')
        self.db = self.mongo_client['test']
        self.arama_koleksiyonu = self.db['arama_sorgulari']

    def ana_sayfaya_don(self):
        self.tarayici.setUrl(QUrl('http://google.com'))


    #PORT SCANNER MANUEL BUTONA BASIP TARIYOR.
    def port_tara(self):
        target_host = "localhost"
        target_ports = range(1, 1025)

        for target_port in target_ports:
            tarama_thread = Thread(target=self.taramayi_baslat, args=(target_host, target_port))
            tarama_thread.start()

    def taramayi_baslat(self, target_host, target_port):
        try:
            soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soket.settimeout(1)
            soket.connect((target_host, target_port))
            print(f"[+] {target_port}/tcp açık")
            soket.close()


            self.arama_koleksiyonu.insert_one({'open_port': target_port})
        except (socket.error, socket.timeout):
            pass

if __name__ == "__main__":
    uygulama = QApplication(sys.argv)
    QApplication.setApplicationName("AKININ TARAYICISI")
    pencere = AnaEkran()
    uygulama.exec()
