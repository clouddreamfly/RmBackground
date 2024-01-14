#!/usr/bin/python3
#-*- coding:utf-8 -*-


import os
import sys
import datetime
import fnmatch
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from rembg import remove
from PIL import Image


    

class RmBackgroundFrame(QWidget):
    
    def __init__(self):
        
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.setWindowTitle("图片移除背景")
        self.resize(860, 520)
        
        self.setAcceptDrops(True)
        
        self.lab_src_img = QLabel(self)
        self.lab_src_img.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lab_src_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.lab_dst_img = QLabel(self)
        self.lab_dst_img.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.lab_dst_img.setAlignment(Qt.AlignmentFlag.AlignCenter)     
        
        
        self.btn_open = QPushButton("打开", self)
        self.btn_remove = QPushButton("移除背景", self)
        self.btn_save = QPushButton("保存", self)
        self.btn_open.setFixedSize(60, 30)
        self.btn_remove.setFixedSize(80, 30)
        self.btn_save.setFixedSize(60, 30)     
        
        group1 = QGroupBox("原图片", self)
        group2 = QGroupBox("结果图", self)
        layout_g1 = QVBoxLayout()
        layout_g2 = QVBoxLayout()
        layout_g1.addWidget(self.lab_src_img, 1)
        layout_g2.addWidget(self.lab_dst_img, 1)
        group1.setLayout(layout_g1)
        group2.setLayout(layout_g2)
    
        layout = QVBoxLayout()
        layout1 = QHBoxLayout()
        layout2 = QHBoxLayout()
   
        layout1.addWidget(group1, 2)
        layout1.addWidget(group2, 2)
        layout2.addWidget(self.btn_open)
        layout2.addWidget(self.btn_remove)
        layout2.addWidget(self.btn_save)
        
        bottom = QWidget(self)
        bottom.setFixedWidth(260)
        bottom.setLayout(layout2)
        
        layout.addLayout(layout1, 1)
        layout.addWidget(bottom, 0, Qt.AlignmentFlag.AlignHCenter)
        
        self.setLayout(layout)
        

        self.btn_open.clicked.connect(self.slotClickedOpen)
        self.btn_remove.clicked.connect(self.slotClickedRemoveBg)
        self.btn_save.clicked.connect(self.slotClickedSave)


    def dragEnterEvent(self, evt):
        
        if evt.mimeData().hasText():
            evt.accept()
        else:
            evt.ignore()
        
    def dropEvent(self, evt):
        
        filepath = evt.mimeData().text()
        path = filepath.replace('file:///', '')
        self.filename = path
        self.dealImage(path, 0)
        
        
    def dealImage(self, path, mode = 0):
              
        if mode == 0:
            self.deal_img = QImage(path)
            src_img = QPixmap.fromImage(self.deal_img).scaled(self.lab_src_img.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.lab_src_img.setPixmap(src_img)
        else:
            pil_image = Image.open(path)
            self.result_img = remove(pil_image)
            self.result_img = self.result_img.toqimage()
            
            dst_img = QPixmap.fromImage(self.result_img).scaled(self.lab_dst_img.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.lab_dst_img.setPixmap(dst_img)        

               
        
    def slotClickedOpen(self, evt):
        
        dlg = QFileDialog(self)
        dlg.setWindowTitle("选择视频文件")
        dlg.setNameFilter("jpg file (*.jpg)\npng file (*.png)\nall file (*.*)")
        ret = dlg.exec()
        if ret == QDialog.DialogCode.Accepted:
            path = dlg.selectedFiles()[0]
            self.filename = path
            self.dealImage(path)
    
    def slotClickedRemoveBg(self, evt):
        
        if hasattr(self, 'deal_img') and self.deal_img: 
            self.dealImage(self.filename, 1)
        else:
            QMessageBox.warning(self, "警告提示", "请先打开图片, 在移除图片背景！")
    
    def slotClickedSave(self, evt):
        
        if hasattr(self, 'result_img') and self.result_img:
            #获取当前时间,转化成字符串
            timenow = datetime.datetime.now()
            timestr = timenow.strftime("%Y-%m-%d-%H-%M-%S")
            
            #保存二维码图片
            if not os.path.exists("imgs"):
                os.makedirs("imgs")
                
            filename = "imgs/imges-" + timestr + '.png'        
            self.result_img.save(filename)

        else:         
            QMessageBox.warning(self, "警告提示", "请先打开图片在保存该图片！")
            


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    frame = RmBackgroundFrame()
    frame.show()
    
    code = app.exec()
    sys.exit(code)