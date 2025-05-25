"""
@ FileName: main
@ Project: ADOFAI_intro_generator
@ Coder: XCXC2011
@ Date: 2025/4/5.
"""

import sys
import json
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
import win32gui
import win32con
from adobase.level import ADOFAILevel

if sys.argv[-1] != 'debug':
    # 获取当前控制台窗口的句柄
    console_window = win32gui.GetForegroundWindow()

    # 隐藏控制台窗口
    win32gui.ShowWindow(console_window, win32con.SW_HIDE)


def generate_title(**kwargs):
    tag = kwargs.get('tag')
    name = kwargs.get('name', '')
    judgment_val = kwargs.get('judgment')

    result = f"【ADOFAI / {tag}】 {name}"
    if judgment_val:
        result += " " + judgment_val
    return result


def generate_intro(**kwargs):
    text = kwargs.get('text', '')
    line = kwargs.get('line', '')
    artist = kwargs.get('artist')
    artist_ = kwargs.get('artist_')
    xacc = kwargs.get('xacc')
    difficulty = kwargs.get('difficulty')
    pp_val = kwargs.get('PP')
    keyboard = kwargs.get('keyboard')
    link = kwargs.get('link')

    result = ''

    if text:
        result += f"{text}\n\n{line}\n\n"
    if artist:
        result += "曲师：" + artist + "\n"
    if artist_:
        result += "谱师：" + artist_ + "\n"
    if xacc:
        result += 'X-Acc：' + str(xacc) + '%\n'
    if difficulty:
        result += '评级：' + difficulty + '\n'
    if pp_val:
        result += f"PP值：{pp_val}\n\n{line}\n\n"
    if keyboard | link:
        result += f'\n{line}\n\n'
    if keyboard:
        result += "键盘：" + keyboard + "\n"
    if link:
        result += "下载链接：" + link

    return result.strip() or '什么都没有'


class IntroGenerator(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("ADOFAI Intro Generator")
        self.setWindowIcon(QtGui.QIcon('./assets/images/icon.png'))

        self.font = QtGui.QFont(QtGui.QFontDatabase.applicationFontFamilies(
            QtGui.QFontDatabase.addApplicationFont('./assets/ttf/FZMWFont.ttf'))[0], 12)
        self.setFont(self.font)

        # 固定窗口大小并隐藏最大化按钮
        self.setFixedSize(800, 600)
        self.setWindowFlags(
            Qt.WindowMinimizeButtonHint |
            Qt.WindowCloseButtonHint
        )

        central_widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(20)
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: white;")

        central_widget = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(self.layout)

        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle('选择谱面文件')
        dialog.setNameFilter('*.adofai')
        filePath, fileType = dialog.getOpenFileName()
        level = ADOFAILevel.load(filePath)

        settings = level.data.get('settings', {})
        name = settings.get('song')
        artist = settings.get('artist')
        suru = settings.get('author')

        # 标题参数组
        title_group = QtWidgets.QGroupBox("标题参数")
        title_group.setFont(self.font)
        title_layout = QtWidgets.QFormLayout()

        try:
            with open('confing.json', 'r', encoding='utf-8') as f:
                data = f.read()
                self.line = json.loads(data)['line']
                self.keyboard = json.loads(data)['keyboard']
        except:
            self.line = ''
            self.keyboard = ''

        self.tag_input = QtWidgets.QLineEdit()
        self.tag_input.setFont(self.font)
        self.tag_input.setPlaceholderText("例如：完美无瑕")
        self.tag_label = QtWidgets.QLabel("<p>标签<font color='#FF0000'> * 必填</font></p>\n")
        self.tag_label.setFont(self.font)
        title_layout.addRow(self.tag_label, self.tag_input)

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setFont(self.font)
        self.name_input.setPlaceholderText("例如：Plum-MEGAMIX2")
        self.name_input.setText(name)
        self.name_label = QtWidgets.QLabel("<p>谱子名字<font color='#FF0000'> * 必填</font></p>\n")
        self.name_label.setFont(self.font)
        title_layout.addRow(self.name_label, self.name_input)

        self.judgment_input = QtWidgets.QLineEdit()
        self.judgment_input.setFont(self.font)
        self.judgment_input.setPlaceholderText("例如：严判")
        self.judgment_label = QtWidgets.QLabel("<p>判定</p>\n")
        self.judgment_label.setFont(self.font)
        title_layout.addRow(self.judgment_label, self.judgment_input)

        title_group.setLayout(title_layout)
        self.layout.addWidget(title_group)

        # 简介参数组
        intro_group = QtWidgets.QGroupBox("简介内容")
        intro_group.setFont(self.font)
        intro_layout = QtWidgets.QFormLayout()

        self.line_input = QtWidgets.QLineEdit()
        self.line_input.setFont(self.font)
        self.line_input.setPlaceholderText("例如：--------------------")
        self.line_input.setText(self.line)
        self.line_label = QtWidgets.QLabel("<p>分隔符<font color='#FF0000'> * 必填</font></p>\n")
        self.line_label.setFont(self.font)
        intro_layout.addRow(self.line_label, self.line_input)

        self.text_input = QtWidgets.QLineEdit()
        self.text_input.setFont(self.font)
        self.text_input.setPlaceholderText("写一些你想说的话")
        self.text_label = QtWidgets.QLabel("<p>文本</p>\n")
        self.text_label.setFont(self.font)
        intro_layout.addRow(self.text_label, self.text_input)

        self.artist_input = QtWidgets.QLineEdit()
        self.artist_input.setFont(self.font)
        self.artist_input.setPlaceholderText("例如：Plum")
        self.artist_input.setText(artist)
        self.artist_label = QtWidgets.QLabel("<p>曲师</p>\n")
        self.artist_label.setFont(self.font)
        intro_layout.addRow(self.artist_label, self.artist_input)

        self.suru_input = QtWidgets.QLineEdit()
        self.suru_input.setFont(self.font)
        self.suru_input.setPlaceholderText("例如：Irin")
        self.suru_input.setText(suru)
        self.suru_label = QtWidgets.QLabel("<p>谱师</p>\n")
        self.suru_label.setFont(self.font)
        intro_layout.addRow(self.suru_label, self.suru_input)

        self.xacc_input = QtWidgets.QLineEdit()
        self.xacc_input.setFont(self.font)
        self.xacc_input.setPlaceholderText("你的准度")
        self.xacc_label = QtWidgets.QLabel("<p>X-Acc</p>\n")
        self.xacc_label.setFont(self.font)
        intro_layout.addRow(self.xacc_label, self.xacc_input)

        self.difficulty_input = QtWidgets.QLineEdit()
        self.difficulty_input.setFont(self.font)
        self.difficulty_input.setPlaceholderText("谱面评级")
        self.difficulty_label = QtWidgets.QLabel("<p>难度</p>\n")
        self.difficulty_label.setFont(self.font)
        intro_layout.addRow(self.difficulty_label, self.difficulty_input)

        self.pp_input = QtWidgets.QLineEdit()
        self.pp_input.setFont(self.font)
        self.pp_input.setPlaceholderText("你的PP分（一般没人去算）")
        self.pp_label = QtWidgets.QLabel("<p>PP值</p>\n")
        self.pp_label.setFont(self.font)
        intro_layout.addRow(self.pp_label, self.pp_input)

        self.keyboard_input = QtWidgets.QLineEdit()
        self.keyboard_input.setFont(self.font)
        self.keyboard_input.setText(self.keyboard)
        self.keyboard_label = QtWidgets.QLabel("<p>键盘型号</p>\n")
        self.keyboard_label.setFont(self.font)
        intro_layout.addRow(self.keyboard_label, self.keyboard_input)

        self.link_input = QtWidgets.QLineEdit()
        self.link_input.setFont(self.font)
        self.link_label = QtWidgets.QLabel("<p>下载链接</p>\n")
        self.link_label.setFont(self.font)
        intro_layout.addRow(self.link_label, self.link_input)

        intro_group.setLayout(intro_layout)
        self.layout.addWidget(intro_group)

        # 生成按钮
        generate_button = QtWidgets.QPushButton("生成并保存")
        generate_button.setFont(self.font)
        generate_button.setStyleSheet(
            "border: 2px solid #87CEEB;"
            "background-color: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #4CAF50,stop:1 #8bc6ff);"
            "color:white; padding:5px; border-radius: 8px;"
        )
        generate_button.clicked.connect(self.generate_intro)
        self.layout.addWidget(generate_button, alignment=QtCore.Qt.AlignRight)

        self.preview = QtWidgets.QTextEdit()
        self.preview.setFont(self.font)
        self.preview.setReadOnly(True)
        self.preview.setPlaceholderText("点击上方按钮查看结果")
        self.preview.setStyleSheet("border:1px solid #D0D0D0; background:#F5F5F5;")
        self.layout.addWidget(self.preview)

        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)
        self.show()

    def generate_intro(self):
        tag = self.tag_input.text().strip()
        name = self.name_input.text().strip()
        line = self.line_input.text().strip()

        if not (tag and name and line):
            QtWidgets.QMessageBox.critical(
                self, "输入错误", "必填字段未填写！"
            )
            return

        title_part = generate_title(
            tag=tag,
            name=name,
            judgment=self.judgment_input.text()
        )

        intro_content = generate_intro(
            text=self.text_input.text(),
            line=line,
            artist=self.artist_input.text(),
            artist_=self.suru_input.text(),
            xacc=self.xacc_input.text(),
            difficulty=self.difficulty_input.text(),
            PP=self.pp_input.text(),
            keyboard=self.keyboard_input.text(),
            link=self.link_input.text()
        )

        output_str = f"标题：\n{title_part}\n\n简介：\n{intro_content}"

        self.preview.setText(output_str)

        with open('confing.json', 'w') as f:
            conf = {
                'line': self.line_input.text(),
                'keyboard': self.keyboard_input.text()
            }
            f.write(json.dumps(conf))
            f.close()

        with open("result.txt", "w") as file:
            file.write(output_str)

        QtWidgets.QMessageBox.information(
            self, "成功提示", "已生成并保存到 result.txt！"
        )

    '''
    def saveChange(self):
        with open('confing.json', 'w') as f:
            conf = {
                'line': self.line_input.text()
            }
            f.write(json.dumps(conf))
            f.close()
    '''

def main():
    app = QtWidgets.QApplication(sys.argv)

    style_sheet = """
        QGroupBox {
            border-radius: 15px;
            background-color: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #F8F8FF, stop:1 #FFFFFF);
            padding:20px;
            border: 1px solid #D3D3D3; 
        }

        QGroupBox::title {
            background:white;
            margin-left:5px;
            padding:4px;
        }

        QLineEdit {
            min-width: 240px;
            max-height: 30px;
            border: 1px solid #D3D3D3;
            border-radius: 5px;
            padding-left: 5px;
        }

        QLineEdit:focus {border-color:#87CEEB;} 

        QPushButton {
            font-weight: bold;
            color: white;
            background-color: qlineargradient(
                x1:0,y1:0,x2:0,y2:1,
                stop:0 #4CAF50,
                stop:1 #8bc6ff
            );
            border-radius: 10px;
        }

        QPushButton:hover {
            background-color: #3d99f6;
        }
    """

    app.setStyleSheet(style_sheet)

    window = IntroGenerator()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()