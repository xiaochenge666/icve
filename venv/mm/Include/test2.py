import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setWindowTitle("打开网页例子")
        #相当于初始化这个加载web的控件
        self.browser = QWebEngineView()
        self.browser.setHtml('''
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <title></title>
            </head>
            <body>
                <img class="img_verifycode change-code change_verifycode"
                 src="https://zjy2.icve.com.cn/common/VerifyCode/index?t=0.7927288017515706"
                  alt="验证码" 
                  title="看不清？点击更换"
                  style="width: 100px; height: 32px;margin-top: 10px;cursor: pointer;">
            </body>
        </html>

        ''')
        self.setCentralWidget(self.browser)
if __name__=='__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())