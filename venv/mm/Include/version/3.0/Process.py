from multiprocessing import Manager,Pool
from Include.com.project.DBcon.DBcon import DBCon
from Include.com.test.ZhiHuiZhiJiao import zhihui
from Include.com.project.moocCourse import mooc
import time
#
#刷课的后台
#
class PoolProcess():
    def __init__(self):
        self.CourseList=[]
        self.CourseState1=[]
        self.ExceptionCourse=[]
    #初始化
    def initThis(self):
        db=DBCon()
        data=db.queryAllFinish3()
        for i in data:
            db.modifyCisFinish('0',i[0],i[1],i[4])
            print('初始化完成')
        db.docloseDb()
    #找完成状态为1的课程
    def findStuat1and3(self):
        db=DBCon()
        data1 = db.queryAllFinish1()
        data2 = db.queryAllFinish3()
        if data1 != ():
            for i in data1:
                if i not in self.CourseState1:
                    self.CourseState1.append(i)
        if data2 != ():
            for i in data2:
                if i not in self.ExceptionCourse:
                    self.ExceptionCourse.append(i)
        db.docloseDb()

    #找到未处理的课程信息将其添加到courseList列表中
    def queryUnfinishAllCourseInfo(self):
        #数据库消息
        db = DBCon()
        data = db.queryAllUnFinishCourse()
        db.docloseDb()
        self.CourseList=[]

        for i in data:
            cdic = {}
            cdic['qqid'] = i[0]
            cdic['userCount'] = i[1]
            cdic['pwd'] = i[2]
            cdic['type'] = i[3]
            cdic['Cname'] = i[4]
            if cdic not in self.CourseList:
                self.CourseList.append(cdic)

    #刷课方法
    def doflash(self,Udic):
        type = Udic['type']#课程的种类
        user=Udic['userCount']
        pwd=Udic['pwd']
        cname=Udic['Cname']
        qqid=Udic['qqid']
        if type == '职教云':
           try:
            #职教云调用
            z = zhihui()
            z.login(user,pwd)
            list=z.getLearnningCourseList()
            z.doFlashBody(list[str(cname)])

            #数据库操作
            db=DBCon()
            db.modifyCisFinish('1',qqid,Udic['userCount'],Udic['Cname'])#上传数据库完成状态1
            db.modifySendMsg('待处理',qqid,Udic['userCount'],Udic['Cname'])#修该数据库的消息处理状态
            db.docloseDb()
            return 1
           except:
               print('zhijiao出错啦')
               db = DBCon()
               db.modifyCisFinish('3',qq, user, cname)  # 上传数据库完成状态1
               db.docloseDb()

        elif type == 'mooc':
            try:
                m=mooc()
                m.login(user,pwd)
                DIC=m.getTotalOneDict()
                m.doFlushCourseBody(DIC[str(cname)])

                #数据库操作
                db = DBCon()
                db.modifyCisFinish('1', qqid, user, cname)  # 上传数据库完成状态1
                db.modifySendMsg('待处理', qqid, user, cname)  # 修该数据库的消息处理状态
                db.docloseDb()
            except:
                print('mooc出错啦')
                db = DBCon()
                db.modifyCisFinish('3', qq, user, cname)  # 上传数据库完成状态1
                db.docloseDb()
        else:
            pass


if __name__ == '__main__':
    P=Pool(10)
    Q=Manager().Queue()
    Obj=PoolProcess()
    Obj.initThis()
    isRungingList = []
    TaskList = []
    tempList=[]
    tempList3=[]
    while True:
        Obj.queryUnfinishAllCourseInfo()#找到未处理的课程
        List=Obj.CourseList#将找的课程添加到list中

        # 遍历list将未刷完的课添加到列队中
        if List!=[]:
            for i in List:
                if i not in TaskList:
                    TaskList.append(i)
                    Q.put(i)

        # 处理列队中的消息
        if Q.qsize()>0:
            while Q.qsize():
                i=Q.get()
                print('一个任务：',i)
                #如果是职教云
                if i['userCount'] not in isRungingList and i['type']=='职教云':#pop掉所有同一个职教云账号
                    isRungingList.append(i['userCount'])
                    P.apply_async(Obj.doflash,(i,))
                elif i['type']=='职教云':
                    if i in TaskList:
                        for index,val in enumerate(TaskList):
                            if val==i:
                                TaskList.pop(index)
                #如果是其他平台    `
                elif i['type']!='职教云':
                    P.apply_async(Obj.doflash, (i, ))


        time.sleep(10)

        #找到状态1的课程#课程一共有4个状态码分别为0，1，2，3，0代表还没经过处理的，1代表刷课结束，但还在列表中，
        #2代表完成并已经移除列表，3代表刷课中断网或出错被终止的课程
        Obj.findStuat1and3()

        #遍历状态1数组
        if Obj.CourseState1 != []:
            #将状态1的课转化成存字典对象的数组（并去重）
            for i in Obj.CourseState1:
                cdic = {}
                cdic['qqid'] = i[0]
                cdic['userCount'] = i[1]
                cdic['pwd'] = i[2]
                cdic['type'] = i[3]
                cdic['Cname'] = i[4]
                if cdic not in tempList:
                    tempList.append(cdic)
            Obj.CourseState1 = []
            for i,value in enumerate(tempList):

                for j,value1 in enumerate(TaskList):

                    if value==value1:
                        db=DBCon()
                        db.modifyCisFinish('2',value['qqid'],value['userCount'],value['Cname'])
                        db.docloseDb()

                        obj=tempList.pop(i)
                        TaskList.pop(j)

                        if obj['userCount'] in isRungingList:
                            for i,value2 in enumerate(isRungingList):
                                if value2==obj['userCount']:
                                    d=isRungingList.pop(i)


        #遍历状态3数组（刷过程中）
        if Obj.ExceptionCourse != []:
            #将状态3的课转化成存字典对象的数组（并去重）
            for i in Obj.ExceptionCourse:
                cdic = {}
                cdic['qqid'] = i[0]
                cdic['userCount'] = i[1]
                cdic['pwd'] = i[2]
                cdic['type'] = i[3]
                cdic['Cname'] = i[4]
                if cdic not in tempList3:
                    tempList3.append(cdic)
            Obj.ExceptionCourse=[]
            for i,value in enumerate(tempList3):

                for j,value1 in enumerate(TaskList):

                    if value==value1:

                        db=DBCon()
                        db.modifyCisFinish('0',value['qqid'],value['userCount'],value['Cname'])
                        db.docloseDb()
                        obj=tempList3.pop(i)
                        TaskList.pop(j)

                        if obj['userCount'] in isRungingList:
                            for i,value2 in enumerate(isRungingList):
                                if value2==obj['userCount']:
                                    d=isRungingList.pop(i)




