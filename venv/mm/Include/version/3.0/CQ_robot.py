from cqhttp import CQHttp
import pprint
from Include.com.project.DBcon.DBcon import DBCon
import re
from Include.com.test.ZhiHuiZhiJiao import zhihui
from multiprocessing import Manager,Pool
import time
import threading
bot = CQHttp(api_root='http://127.0.0.1:5700')
list=[]
#=========================一些消息常量============================================
Menu="[CQ:face,id=54][CQ:face,id=54][CQ:face,id=54][CQ:face,id=54]菜单[CQ:face,id=54][CQ:face,id=54][CQ:face,id=54][CQ:face,id=54]\r\n"\
                "≡≡≡≡≡≡≡≡≡≡≡\r\n"\
                "[CQ:face,id=66]查余额[CQ:face,id=66]\r\n"\
                "☆☆☆☆☆☆☆☆☆☆☆\r\n"\
                "[CQ:face,id=66]查状态[CQ:face,id=66]\r\n"\
                "☆☆☆☆☆☆☆☆☆☆☆\r\n"\
                "[CQ:face,id=66]充    值[CQ:face,id=66]\r\n"\
                "☆☆☆☆☆☆☆☆☆☆☆\r\n"\
                "[CQ:face,id=66]刷    课[CQ:face,id=66]\r\n"\
                "☆☆☆☆☆☆☆☆☆☆☆\r\n"\
                "[CQ:face,id=66]表   单1[CQ:face,id=66]\r\n"\
                "☆☆☆☆☆☆☆☆☆☆☆\r\n"\
                "[CQ:face,id=66]表   单2[CQ:face,id=66]\r\n"\
                "☆☆☆☆☆☆☆☆☆☆☆\r\n"\
                "[CQ:face,id=66]使用教程[CQ:face,id=66]\r\n"\
                "☆☆☆☆☆☆☆☆☆☆☆\r\n"\
                "[CQ:face,id=66]关于我们[CQ:face,id=66]\r\n"\
                "☆☆☆☆☆☆☆☆☆☆☆\r\n"\
                "[CQ:face,id=66]加入我们[CQ:face,id=66]\r\n"\
                "≡≡≡≡≡≡≡≡≡≡≡\r\n"
form2='[CQ:face,id=54][CQ:face,id=54][CQ:face,id=54][CQ:face,id=54]表单②[CQ:face,id=54][CQ:face,id=54][CQ:face,id=54][CQ:face,id=54]\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '  ℡点击长按复制此表单\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '[CQ:face,id=66]账号{}[CQ:face,id=66]\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '☆☆☆☆☆☆☆☆☆☆☆\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '[CQ:face,id=66]平台{}[CQ:face,id=66]\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '☆☆☆☆☆☆☆☆☆☆☆\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '[CQ:face,id=66]课程名序号{}[CQ:face,id=66]\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '☆☆☆☆☆☆☆☆☆☆☆\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                'tips：请将相关消息填入“{ }”\r\n'\
                '中，并保证账号，课程名序号，\r\n'\
                '平台正确，其余信息不变！'
form1='[CQ:face,id=54][CQ:face,id=54][CQ:face,id=54][CQ:face,id=54]表单①[CQ:face,id=54][CQ:face,id=54][CQ:face,id=54][CQ:face,id=54]\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '℡点击长按复制此表单\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '[CQ:face,id=66]账号{}[CQ:face,id=66]\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '☆☆☆☆☆☆☆☆☆☆☆\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '[CQ:face,id=66]密码{}[CQ:face,id=66]\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '☆☆☆☆☆☆☆☆☆☆☆\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '[CQ:face,id=66]平台{}[CQ:face,id=66]\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '☆☆☆☆☆☆☆☆☆☆☆\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                'tips:请将账号信息填入“{ }”\r\n'\
                '中，保持其余信息完整，平\r\n'\
                '台名在“职教云,Mooc”选择\r\n'\
                '!\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡'
demo='[CQ:face,id=54][CQ:face,id=54][CQ:face,id=54][CQ:face,id=54]使用教程[CQ:face,id=54][CQ:face,id=54][CQ:face,id=54][CQ:face,id=54]\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '  ℡网课小助手3.0\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '[CQ:face,id=66]①发送：刷课\r\n'\
                '[CQ:face,id=66]②填写表单1\r\n'\
                '[CQ:face,id=66]③发送表单1\r\n'\
                '[CQ:face,id=66]④查看返回的课程名所对应的序号\r\n'\
                '[CQ:face,id=66]⑤填写表单2\r\n'\
                '[CQ:face,id=66]⑥发送表单2\r\n'\
                '[CQ:face,id=66]⑦查看提交结果\r\n'\
                '[CQ:face,id=66]⑧等待服务器处理(1-2天)\r\n'\
                '[CQ:face,id=66]⑨完成\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '☆☆☆持续更新中☆☆☆\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡'
tips='[CQ:face,id=54][CQ:face,id=54][CQ:face,id=54][CQ:face,id=54]用户须知[CQ:face,id=54][CQ:face,id=54][CQ:face,id=54][CQ:face,id=54]\r\n'\
            '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
            '  ℡在线客服:369984438\r\n'\
            '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
            '[CQ:face,id=66]本刷课平台支持智慧职教(职教云)，职教云mooc,后期会适配其他平台，尽请期待…\r\n'\
            '[CQ:face,id=66]小助手工作时间:9:00-22:00，客服在线时间:9:00~22:00,还请文明沟通不要骂骂咧咧！\r\n'\
            '[CQ:face,id=66]订单出现漏刷或超时请联系客服处理。\r\n'\
            '[CQ:face,id=66]提交一门课程一般是24小时左右，具体看课件的多少，刷课期间，不要修改密码，可以上号，但是不能查看课件，否则会造成有些课件漏刷！后果自负。\r\n'\
            '[CQ:face,id=66]课程的价格，职教云8￥/一门 '\
            '(包评论，笔记，纠错，问答)，mooc(慕课学院)7￥/一门(包做题正确率99.9%)。\r\n'\
            '[CQ:face,id=66]活动:充值50到账60，充值100到账120，充值请联系QQ:369984438。\r\n'\
            '[CQ:face,id=66]刷课中遇到bug可以及时向客服反馈。\r\n'\
            '[CQ:face,id=66]更新时间:2019.9\r\n'\
            '[CQ:face,id=66]版本号:3.0\r\n'\
            '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
            '☆☆☆持续更新中☆☆☆\r\n'\
            '≡≡≡≡≡≡≡≡≡≡≡'
about='[CQ:face,id=54][CQ:face,id=54][CQ:face,id=54][CQ:face,id=54]关于我们[CQ:face,id=54][CQ:face,id=54][CQ:face,id=54][CQ:face,id=54]\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '  ℡在线客服:369984438\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '[CQ:face,id=66]网[CQ:face,id=66]课[CQ:face,id=66]小[CQ:face,id=66]助[CQ:face,id=66]手\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡\r\n'\
                '更新时间:2019.9\r\n'\
                '版本号:3.0\r\n'\
                '☆☆☆持续更新中☆☆☆\r\n'\
                '≡≡≡≡≡≡≡≡≡≡≡'
#===============================================================================
#每隔60s刷新一次是否有要通知的消息（用线程实现后台运行）
def reflushMesg():
    while True:
        time.sleep(60)
        # ----------读取数据库中已完成且需要通知用户
        db = DBCon()
        data = db.queryAllSendMsg()
        if data != ():
            print(data)
            for i in data:
                qqid = i[0]
                print(qqid)
                try:
                    myctx = {
                        'font': 41831136,
                        'message': 'Dl',
                        'message_id': 5554,
                        'message_type': 'private',
                        'post_type': 'message',
                        'raw_message': 'Dl',
                        'self_id': 2295891738,
                        'sender': {'age': 19, 'nickname': 'Y', 'sex': 'male', 'user_id': qqid},
                        'sub_type': 'friend',
                        'time': 1556940667,
                        'user_id': qqid}

                    bot.send(myctx, '课程《' + i[1] + '》已完成!')
                    db.modifySendMsg('已处理', str(i[0]), str(i[2]), str(i[1]))
                    print('通知成功！')
                except:
                    db.modifySendMsg('已失去好友关系', str(i[0]), str(i[2]), str(i[1]))
                    print('失败！')
        db.docloseDb()
t=threading.Thread(target=reflushMesg)
t.start()
#===============================================================================
@bot.on_message('private')
def handle_msg(ctx):
    global list
    pprint.pprint(ctx)#总消息
    userid=ctx['user_id']#用户id
    message=ctx['raw_message']#用户发送的消息

#----------请求数据库，进行身份验证，若未绑定提示绑定
    db=DBCon()
    state=db.queryUser(userid)#如数据库中找不到该用户的id返回None
    db.docloseDb()
    if(state!=None):
        # ----------处理用户请求，获取的用户信息储存到数据库
        # ===============================================================================
        if re.search('\[CQ:face,id=54\]表单①',message)!=None:
            # print(re.findall('平台\{.*\}|账号\{.*\}|密码\{.*\}',message))
            user=re.search('账号\{(.*)\}',message).group()[3:-1].strip()
            pwd=re.search('密码\{.*\}',message).group()[3:-1].strip()
            type=re.search('平台\{.*\}',message).group()[3:-1].strip()#平台app
            print(user,pwd,type)

            # 判断平台
            if type=='职教云':
                z = zhihui()
                #判断登陆结果
                if z.login(user, pwd)==1:

                    #将账号密码信息存入数据库
                    db=DBCon()
                    db.addUserInfo(userid,user,pwd,type)
                    db.docloseDb()

                    #返回课程名给用户
                    bot.send(ctx,"正在读取课程中，请稍后...")

                    courseList=''#返回给用户的所有课程及索引的文本对象
                    for i in z.getLearnningCourseList():
                        #Db操作
                        db=DBCon()
                        #判断此课程名是否已经在数据库中了，如果没有则添加进数据库
                        if db.queryCourseIndex(i)==None:
                            db.addCname(i)
                            print('添加',i)
                        #通过课程名找到此课程名的索引
                        index=db.queryCourseIndex(i)
                        db.docloseDb()#关闭数据库连接

                        courseList=courseList+'👉'+str(index[0])+'👈:'+str(i)+'\n\n'#将课程名拼装成字符串

                    bot.send(ctx,courseList)
                    bot.send(ctx,"请提交表单㈡")
                    bot.send(ctx,form2)

                else:
                    bot.send(ctx,'账号或密码错误！')

            elif type=='mooc':
                pass
            else:
                bot.send(ctx,'您输入的平台名有问题，请规范填写!')
        # ----------将用户提交的课程信息提交到数据库
        if re.search('\[CQ:face,id=54\]表单②\[CQ:face,id=54\]',message)!=None:
            # 提取表单消息中
            CnameIndex=re.search('课程名序号\{.*\}',message).group()[6:-1].strip()
            type = re.search('平台\{.*\}', message).group()[3:-1].strip()
            Usercount = re.search('账号\{.*\}', message).group()[3:-1].strip()


            #验证信息是否合法
            db = DBCon()
            Cname=db.queryCnamebyIndex(CnameIndex)[0]
            data = db.queryUserId(userid, type)
            pwd=db.queryUserPwd(userid,type,Usercount)
            money=db.queryMoney(userid)
            db.docloseDb()
            if type not in ['mooc','职教云']:
                bot.send(ctx,"平台名不合法")
            elif(str(Usercount),) not in data:
                bot.send(ctx,"账号不合法")
            elif int(money[0])>0:
                if type=="职教云" and int(money[0])>8:
                    z=zhihui()
                    z.login(Usercount,pwd[0][0])
                    data=z.getLearnningCourseList()

                    if Cname not in data:
                        bot.send(ctx, "课程名不合法")
                    else:
                        try:
                            db=DBCon()
                            code=db.addCourse(userid,Cname,type,0,Usercount)
                            #判断是否成功
                            if code!=0:
                                bot.send(ctx,'提交成功！')
                                money = db.queryMoney(userid)
                                newmoney = int(str(money[0])) - 8#扣取相关费用
                                db.modifyMoney(userid, newmoney)
                                db.docloseDb()
                            else:
                                bot.send(ctx,'提交失败，请联系管理！')
                                db.docloseDb()
                        except:
                            db.rollBack()
                            bot.send(ctx,'提交失败，请联系管理！')
                elif type=="mooc" and int(money[0])>7:
                    pass
                else:
                    bot.send(ctx,'余额不足！请充值！')
        # ===============================================================================


        # ----------处理一些菜单用户命令---------
        # ===============================================================================
        #1.菜单
        if re.search('菜单',message)!=None:
            bot.send(ctx,Menu)
        elif re.search('查余额',message)!=None:
            db=DBCon()
            data=db.queryMoney(userid)
            db.docloseDb()
            money=str('当前账户可用余额为：'+data[0])+"￥"
            bot.send(ctx,money)
        elif re.search('查状态', message) != None:
            pass
        elif re.search('充值', message) != None:
            charge='请联系：QQ369984438'
            bot.send(ctx,charge)
        elif re.search('表单1', message) != None:
            bot.send(ctx,form1)
        elif re.search('表单2', message) != None:
            bot.send(ctx,form2)
        elif re.search('使用教程', message) != None:
            bot.send(ctx,demo)
        elif re.search('关于我们', message) != None:
            bot.send(ctx,about)
        elif re.search('加入我们', message) != None:
            bot.send(ctx,'敬请期待！')
        elif re.search('用户须知', message) != None:
            bot.send(ctx,tips)
        elif re.search('刷课',message) != None:
            bot.send(ctx,'请提交表单㈠')
            bot.send(ctx,form1)
        # ===============================================================================







    else:
        print('登陆失败')
#----------将处理的结果返回给用户
bot.run('127.0.0.1', 8080)