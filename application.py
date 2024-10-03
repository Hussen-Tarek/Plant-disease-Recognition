import sys
import cv2
import numpy as np
from keras.models import load_model
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout)
from PyQt5.QtGui import QPixmap, QFont, QIcon
import PyQt5.QtCore as QtCore


class Window2(QWidget):
    def __init__(self, parent=None):
        super(Window2, self).__init__(parent, QtCore.Qt.Window) # <---
        self.resize(800,600)
        #self.setWindowTitle("Info")
        self.setWindowIcon(QIcon('logo.png'))
        self.layout = QVBoxLayout()
        self.labl = QLabel(self)
        self.labl.setFont(QFont('Arial', 12))
        self.labl.setWordWrap(True)
        #self.labl.move(270,300)
        
        self.setLayout(self.layout)

class PlantVillage(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(600,500)
        self.setWindowTitle("PlantVillage Disease Classification")
        self.setWindowIcon(QIcon('logo.png'))
        self.button1 = QPushButton("Upload image")
        self.button1.clicked.connect(self.get_image_file)
        self.button2 = QPushButton('Classify image')
        self.button2.clicked.connect(self.analysis_image)
        self.button3 = QPushButton('Disease causes')
        self.button3.clicked.connect(lambda: self.cause_window(self.analysis_image()))
        self.button4 = QPushButton('Treatment methods')
        self.button4.clicked.connect(lambda: self.treatment_window(self.analysis_image()))

        self.labl = QLabel(self)
        self.labl.setFont(QFont('Arial', 13))
        self.labl.move(270,300)
        self.labelImage = QLabel()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.labelImage)
        self.setLayout(self.layout)

    def get_image_file(self):
        self.labl.setText(" ")
        self.file_name, _ = QFileDialog.getOpenFileName(self, 'Open Image File', r"<Default dir>", "Image files (*.jpg *.jpeg *.gif)")
        self.labelImage.setPixmap(QPixmap(self.file_name))
        #self.button1.deleteLater()
        self.button1.setText("Upload new image")
        self.layout.addWidget(self.button2)
        self.setLayout(self.layout)

    def cause_window(self,class_decoding):
        self.newindow = Window2(self)
        self.newindow.setWindowTitle("Disease Causes")
        print (class_decoding)
        if (class_decoding == 1) or (class_decoding == 4):
            self.data = "The plant is healthy"
        else:
            with open ("disease_causes/"+str(class_decoding)+".txt", "r") as myfile:
                self.data = str(myfile.read().splitlines())
        print (self.data)
        self.newindow.labl.setText(self.data)
        self.newindow.labl.adjustSize()
        self.newindow.show()

    def treatment_window(self,class_decoding):
        self.newindow = Window2(self)
        self.newindow.setWindowTitle("Disease Treatment")
        print (class_decoding)
        if (class_decoding == 1) or (class_decoding == 4):
            self.data = "The plant is healthy"
        else:
            with open ("disease_treatment/"+str(class_decoding)+".txt", "r") as myfile:
                self.data = str(myfile.read().splitlines())
        self.newindow.labl.setText(self.data)
        self.newindow.labl.adjustSize()
        self.newindow.show()

    def analysis_image(self):
        class_decode = {0:"Pepperbell_Bacterial_spot",1:"Pepperbell_healthy",2:"Potato_Earlyblight",
                3:"PotatoLate_blight",4:"Potato_healthy",5:"Tomato_Bacterial_spot", 
                6:"Tomato_Early_blight", 7:"Tomato_Late_blight", 8:"Tomato_Leaf_Mold", 9:"Tomato_Septoria_leaf_spot",10:"Tomato_Spider_mites_Two_spotted_spider_mite",
                11:"TomatoTarget_Spot",12:"TomatoTomato_YellowLeafCurl_Virus",13:"TomatoTomato_mosaic_virus",14:"Tomato_healthy"}
        img = cv2.imread(self.file_name)#read the image
        img = cv2.resize(img,(128,128))#resize
        img = img/.255 #normalization
        img = np.reshape(img,[1,128,128,3])#convert it to tensor
        model = load_model('model_v1.h5')
        test_pred = model.predict(img)
        print(test_pred,"output")
        print(np.argmax(test_pred,axis=1)[0],"output")
        test_class = np.argmax(test_pred,axis=1)[0]
        print(class_decode.get(test_class))

        
        
        #img = cv2.imread()#read the image
        # img = cv2.resize(img,(256,256))#resize
        #img = img/.255 #normalization
        # img = np.reshape(img,[1,256,256,3])#convert it to tensor
        #class_output = model.predict_classes(img)
        self.labl.setText(class_decode.get(test_class)) #the decoded class (disease or healthy)
        self.labl.adjustSize()
        self.layout.addWidget(self.button3)
        self.layout.addWidget(self.button4)
        self.setLayout(self.layout)
        return test_class


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = PlantVillage()
    demo.show()
    sys.exit(app.exec_())
