"""
@ FileName: UI
@ Project: ADOFAI_intro_generator
@ Coder: XCXC2011
@ Date: 2025/4/5.
"""

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt


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

        # 固定窗口大小并隐藏最大化按钮
        self.setFixedSize(800, 600)
        self.setWindowFlags(
            Qt.WindowMinimizeButtonHint |
            Qt.WindowCloseButtonHint
        )

        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QGridLayout()
        layout.setSpacing(20)
        self.setMinimumSize(800, 600)
        self.setStyleSheet("background-color: white;")

        central_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        central_widget.setLayout(layout)

        # 标题参数组
        title_group = QtWidgets.QGroupBox("标题参数")
        title_layout = QtWidgets.QFormLayout()

        self.tag_input = QtWidgets.QLineEdit()
        self.tag_input.setPlaceholderText("例如：完美无瑕")
        title_layout.addRow(QtWidgets.QLabel("<b>标签</b>\n"), self.tag_input)

        self.name_input = QtWidgets.QLineEdit()
        self.name_input.setPlaceholderText("例如：Plum-MEGAMIX2")
        title_layout.addRow(QtWidgets.QLabel("<b>谱子名字</b>\n<font color='#FF0000'>* 必填</font>"), self.name_input)

        self.judgment_input = QtWidgets.QLineEdit()
        self.judgment_input.setPlaceholderText("例如：严判")
        title_layout.addRow(QtWidgets.QLabel("<b>判定</b>\n"), self.judgment_input)

        title_group.setLayout(title_layout)
        layout.addWidget(title_group)

        # 简介参数组
        intro_group = QtWidgets.QGroupBox("简介内容")
        intro_layout = QtWidgets.QFormLayout()

        self.line_input = QtWidgets.QLineEdit()
        self.line_input.setPlaceholderText("例如：--------------------")
        intro_layout.addRow(QtWidgets.QLabel("<b>分隔符</b>\n<font color='#FF0000'>* 必填</font>"), self.line_input)

        self.text_input = QtWidgets.QLineEdit()
        self.text_input.setPlaceholderText("写一些你想说的话")
        intro_layout.addRow(QtWidgets.QLabel("<b>文本</b>\n"), self.text_input)

        self.artist_input = QtWidgets.QLineEdit()
        self.artist_input.setPlaceholderText("例如：Plum")
        intro_layout.addRow(QtWidgets.QLabel("<b>曲师</b>\n"), self.artist_input)

        self.suru_input = QtWidgets.QLineEdit()
        self.suru_input.setPlaceholderText("例如：Irin")
        intro_layout.addRow(QtWidgets.QLabel("<b>谱师</b>\n"), self.suru_input)

        self.xacc_input = QtWidgets.QLineEdit()
        self.xacc_input.setPlaceholderText("你的准度")
        intro_layout.addRow(QtWidgets.QLabel("<b>X-Acc</b>\n"), self.xacc_input)

        self.difficulty_input = QtWidgets.QLineEdit()
        self.difficulty_input.setPlaceholderText("谱面评级")
        intro_layout.addRow(QtWidgets.QLabel("<b>难度</b>\n"), self.difficulty_input)

        self.pp_input = QtWidgets.QLineEdit()
        self.pp_input.setPlaceholderText("你的PP分（一般没人去算）")
        intro_layout.addRow(QtWidgets.QLabel("<b>PP值</b>\n"), self.pp_input)

        self.keyboard_input = QtWidgets.QLineEdit()
        intro_layout.addRow(QtWidgets.QLabel("<b>键盘型号</b>\n"), self.keyboard_input)

        self.link_input = QtWidgets.QLineEdit()
        intro_layout.addRow(QtWidgets.QLabel("<b>下载链接</b>\n"), self.link_input)

        intro_group.setLayout(intro_layout)
        layout.addWidget(intro_group)

        # 生成按钮
        generate_button = QtWidgets.QPushButton("生成并保存")
        generate_button.setStyleSheet(
            "border: 2px solid #87CEEB;"
            "background-color: qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #4CAF50,stop:1 #8bc6ff);"
            "color:white; padding:5px; border-radius: 8px;"
        )
        generate_button.clicked.connect(self.generate_intro)
        layout.addWidget(generate_button, alignment=QtCore.Qt.AlignRight)

        self.preview = QtWidgets.QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setPlaceholderText("点击上方按钮查看结果")
        self.preview.setStyleSheet("border:1px solid #D0D0D0; background:#F5F5F5;")
        layout.addWidget(self.preview)

        central_widget.setLayout(layout)
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
        with open("result.txt", "w") as file:
            file.write(output_str)

        QtWidgets.QMessageBox.information(
            self, "成功提示", "已生成并保存到 result.txt！"
        )


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
