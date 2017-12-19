import itchat
import requests
# import matplotlib.pyplot as plt

def friends_analysis():
    friends = itchat.get_friends(update=True)[0:]
    male = female = other = 0
    NickName = friends[0]['NickName']
    for i in friends[1:]:
        sex = i["Sex"]
        if sex == 1:
            male += 1
        elif sex == 2:
            female += 1
        else:
            other += 1

    total = len(friends[1:])

    print("%s，你共有好友%d人" %( NickName,total))
    print("其中男性好友%d人，占总人数的%.2f%%" % (male, (float(male) / total * 100)))
    print("其中女性好友%d人，占总人数的%.2f%%" % (female, (float(female) / total * 100)))
    print("其中未填性别%d人，占总人数的%.2f%%" % (other, (float(other) / total * 100)))


    # plt.figure('微信好友性别分布')
    # labels = '男', '女', '其他'
    # sizes = male,female,other
    # colors = 'lightgreen', 'gold', 'lightskyblue'
    # explode = 0, 0, 0
    # plt.title("%s的微信好友性别分布如下"%NickName)
    # plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=False, startangle=50)
    # plt.axis('equal')
    # plt.show()


def post_to_robot(msg):
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': '529058217bcb421cb01b607e7e388e18',
        'info': msg,
        'userid': '微信机器人V1.0',
    }
    # 发送post请求
    r = requests.post(apiUrl, data=data).json()


    return r


def wechat_robot():
    @itchat.msg_register(itchat.content.TEXT)
    def text_reply(msg):
        if msg['ToUserName'] == itchat.get_friends()[0]['UserName']:
            name = (msg['User']['RemarkName'] if msg['User']['RemarkName'] else msg['User']['NickName'])
            print("%s:%s" % (name, msg['Text']))
            reply = post_to_robot(msg['Text'])
            reply_s = reply['text'] if reply['code']==100000 else reply['text'] + reply['url']
            print("自动回复:%s" % reply_s)
            return reply_s
        else:
            print('你发送了消息:%s' % msg['Text'])

    @itchat.msg_register(itchat.content.PICTURE)
    def picture_reply(msg):
        msg.download('img/'+msg.fileName)
        typeSymbol = {
            'PICTURE' : 'img'}.get(msg.type, 'img')
        return '@%s@%s' % (typeSymbol,'img/'+msg.fileName)

    # itchat.auto_login(hotReload=True)
    itchat.run()


if __name__ == '__main__':
    itchat.auto_login()
    while(True):
        print("--------------------------------------------------")
        print("1.查看好友性别分布")
        print('2.开启微信机器人')
        print("--------------------------------------------------")
        select = input('请按提示输入:')
        if(select == '1'):
            friends_analysis()
        elif(select == '2'):
            wechat_robot()
        else:
            print("输入不符合要求！")
