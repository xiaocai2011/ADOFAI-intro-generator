print('Welcome to \033[1;35mADOFAI INTRO GENERATOR\033[0m')
print('Made by \033[1;7m MNCAT Studio \033[0m\n')
print('\033[31m注：标签、谱子名字、分隔符必填，其它不想填可以不填直接回车！\033[0m\n')

tag = input('你要给这期视频打上什么标签 > ')
name = input('谱子名字（想改字体？\033[35mhttps://igfonts.io/\033[0m） > ')
judgmennt = input('判定 > ')

line = input('简介分隔符 > ')

text = input('有什么需要说的吗 > ')

artist = input('曲师 > ')
artist_ = input('谱师 > ')
xacc = input('你的X-Acc（不要输入百分号） > ')
difficulty = input('难度 > ')
PP = input('PP值（如果有算的话） > ')

keyboard = input('你的键盘 > ')
link = input('谱面下载链接 > ')

def generate_title(**args):
    result = f'【ADOFAI / {args['tag']}】 {args['name']} '
    if len(args) == 3:
        result += args['judgment']

    return result

def generate_intro(**args):
    result = ''
    if args['text']:
        result += args['text'] + '\n\n' + args['line'] + '\n\n'
    if args['artist']:
        result += '曲师：' + args['artist'] + '\n'
    if args['artist_']:
        result += '谱师：' + args['artist_'] + '\n'
    if args['xacc']:
        result += 'X-Acc：' + args['xacc'] + '%\n'
    if args['difficulty']:
        result += '评级：' + args['difficulty'] + '\n'
    if args['PP']:
        result += 'PP值：' + args['PP'] + '\n\n' + args['line'] + '\n\n'
    if args['keyboard']:
        result += '键盘：' + args['keyboard'] + '\n'
    if args['link']:
        result += '下载链接：' + args['link']

    return result if result != '' else '什么都没有'

last = f'''
标题：{generate_title(tag=tag, name=name, judgment=judgmennt)}

简介：
{generate_intro(line=line, text=text, artist=artist, artist_=artist_, xacc=xacc, difficulty=difficulty, PP=PP, keyboard=keyboard, link=link)}
'''

with open('result.txt', 'w') as f:
    f.write(last)
    f.close()

print('\n生成完毕，结果请查看result.txt')
input('按任意键退出...')