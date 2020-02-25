import urllib.request
import urllib.parse
import json
import http.cookiejar
import time
from selenium import webdriver
from Include.com.day7.Tensorflow import *
class zhihui():
    
    name = ''  # '183618'      #'183680'
    pwo = ''  # 'C19990818'      #'wjh8023.'
    opener=''
    #函数
    #使用selenium处理需要更新的资源
    def update(self,courseOpenId,openClassId,cellId,flag,moduleId,type,user,pwt):
        #创建对象
        # driver = webdriver.Firefox()
        driver = webdriver.PhantomJS(executable_path=r'G:\Downloads\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        # 登陆
        driver.get('https://zjy2.icve.com.cn/portal/login.html')
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[1]/div/input').send_keys(user)#账号
        driver.find_element_by_xpath('/html/body/div[2]/div/div/div[1]/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[2]/div/input').send_keys(pwt)#密码
        driver.find_element_by_xpath('//*[@id="btnLogin"]').click()#登陆
        time.sleep(1)
        url='https://zjy2.icve.com.cn/common/directory/directory.html?courseOpenId='+str(courseOpenId)+'&openClassId='+str(openClassId)+'&cellId='+str(cellId)+'&flag='+str(flag)+'&moduleId='+str(moduleId)
        driver.get(url)#目录界面
        time.sleep(1)
        if type=='视频':
            #如果是视频
            time.sleep(2)
            try:
                driver.find_element_by_xpath("/html/body/div/div[3]/div/div/div[1]/div/div/div[7]/div[1]/div").click()
            except:
                print('出错')
            time.sleep(2)
        driver.close()
        return 0
    #1.登陆函数，使用户登陆平台并保持登陆状态
    def login(self,username, password):
        # 登陆账号保持登陆状态
        self.name=username
        self.pwo=password
        list=[]
        global opener
        date = {}
        date["userName"] = username
        date["userPwd"] = password
        # 登陆地址
        url = 'https://zjy2.icve.com.cn/common/login/login'
        # 发起请求
        req = urllib.request.Request(url=url, data=urllib.parse.urlencode(date).encode("utf-8"), headers=header)
        # 构造cookie
        cookie = http.cookiejar.CookieJar()
        # 由cookie构造opener
        opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))
        # 发送登录请求，此后这个opener就携带了cookie，以证明自己登录过
        resp = opener.open(req)
        Json = json.loads(resp.read().decode('utf-8'))
        print(Json)
        if Json['code']==1:
            print("登陆成功！")
            dict={}
            dict['code']=1
            dict['userId']=Json['userId']
            dict['userName'] = Json['userName']
            dict['displayName']=Json['displayName']
            return 1
        elif Json['code']==-2:
            print("密码错误！")
            return -2
        elif Json['code'] == -1:
            print("用户不存在！")
            return -1
        else:
            print('未知错误')
            return 0
    #3.获得courseOpenId
    def getLearnningCourseList(self):
        # 说明：此方法负责获取courseOpenId，openClassId，courseName返回一个内置字典的数组
        #创建列表
        Coures={}
        # 获取课程科目
        url = 'https://zjy2.icve.com.cn/student/learning/getLearnningCourseList'
        req = urllib.request.Request(url=url, headers=header)
        req = opener.open(req)
        info = json.loads(req.read().decode("utf-8"))

        courseList=info['courseList']
        for i in courseList:
            list={}
            list['courseName']=i['courseName']
            list['courseOpenId']=i['courseOpenId']
            list['openClassId'] = i['openClassId']
            list['process'] = i['process']
            list['totalScore'] = i['totalScore']
            list['assistTeacherName'] = i['assistTeacherName']
            Coures[i['courseName']]=list
        return Coures
    def getProcessList(self,courseOpId,openClassId):
        list = []  # 储存moduleId
        url = 'https://zjy2.icve.com.cn/study/process/getProcessList'
        date1 = {}
        date1['courseOpenId'] = courseOpId
        date1['openClassId']=openClassId
        req = urllib.request.Request(url=url, headers=header, data=urllib.parse.urlencode(date1).encode('utf-8'))
        req = opener.open(req)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.read().decode("utf-8"))
        # print(info)
        # print(info['progress']['moduleList'])
        moduleList=info['progress']['moduleList']
        for i in moduleList:
            list1={}
            list1['moduleId']=i['id']
            list1['name'] =i['name']
            list1['percent']=i['percent']
            list.append(list1)
        return list
    def getTopicByModuleId(self,courseOpId,moduleId):
        list = []  # 储存moduleId
        url = 'https://zjy2.icve.com.cn/study/process/getTopicByModuleId'
        date1 = {}
        date1['courseOpenId'] = courseOpId
        date1['moduleId']=moduleId
        req = urllib.request.Request(url=url, headers=header, data=urllib.parse.urlencode(date1).encode('utf-8'))
        req = opener.open(req)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.read().decode("utf-8"))
        # print(info)
        # print(info['topicList'])
        topicList=info['topicList']
        for i in topicList:
            # print(i)
            list1={}
            list1['topicId']=i['id']#topicid
            list1['name']=i['name']#
            list.append(list1)
        return list
    def getCellByTopicId(self,courseOpId,openClassId,topicId):
        list = []  # 储存moduleId
        url = 'https://zjy2.icve.com.cn/study/process/getCellByTopicId'
        date1 = {}
        date1['courseOpenId'] = courseOpId
        date1['openClassId']=openClassId
        date1['topicId']=topicId
        req = urllib.request.Request(url=url, headers=header, data=urllib.parse.urlencode(date1).encode('utf-8'))
        req = opener.open(req)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.read().decode("utf-8"))
        # print(info['cellList'])
        cellList=info['cellList']
        for i in cellList:
            if i['categoryName']=='子节点':
                # print('-----------字节点----------------')
                # print(i['childNodeList'])
                for i1 in i['childNodeList']:#遍历子节点中的课件
                    list1={}
                    list1['Id']=i1['Id']#cellk课件id
                    list1['cellName']=i1['cellName']#课件名
                    list1['categoryName']=i1['categoryName']#课件类型
                    list1['stuCellFourPercent'] = i1['stuCellFourPercent']#课件百分比
                    list.append(list1)
            else:
                # print("------------非子节点--------------")
                list2 = {}
                list2['Id'] = i['Id']
                list2['cellName'] = i['cellName']
                list2['categoryName'] = i['categoryName']
                list2['stuCellFourPercent'] = i['stuCellPercent']
                list.append(list2)
                # print('list:',list)
        return list
    #查看当前cell课件的信息
    def continueStudy(self,courseOpenId,openClassId,cellId,cellName,moduleId):
        url='https://zjy2.icve.com.cn/common/Directory/changeStuStudyProcessCellData'
        date1 = {}
        date1['courseOpenId'] = courseOpenId
        date1['openClassId'] = openClassId
        date1['moduleId'] = moduleId
        date1['cellId'] = cellId
        date1['cellName'] = cellName
        req = urllib.request.Request(url=url, headers=header, data=urllib.parse.urlencode(date1).encode('utf-8'))
        req = opener.open(req)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.read().decode("utf-8"))
    def viewDirectory(self,courseOpenId,openClassId,cellId,flag,moduleId):
        list = []  # 储存moduleId
        url = 'https://zjy2.icve.com.cn/common/Directory/viewDirectory'
        date1 = {}
        date1['courseOpenId']=courseOpenId
        date1['openClassId'] =openClassId
        date1['cellId'] =cellId
        date1['flag'] =flag
        date1['moduleId'] =moduleId

        req = urllib.request.Request(url=url, headers=header, data=urllib.parse.urlencode(date1).encode('utf-8'))
        req = opener.open(req)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.read().decode("utf-8"))
        # print("+++++++",info)
        list1={}
        # time.sleep(5)
        if info['code']==1:
            list1['audioVideoLong']=info['audioVideoLong']#这是课件的时间
            list1['cellName'] = info['cellName']#课件名
            list1['cellLogId'] = info['cellLogId']#logid
            list1['cellPercent'] = info['cellPercent']#当前课件完成百分比
            list1['guIdToken'] = info['guIdToken']#
            list1['isNeedUpdate'] = info['isNeedUpdate']#是否需要更新
            list1['categoryName'] = info['categoryName']#课件类型
            list.append(list1)
            # print('=====',list)
            return list  # 返回一个数组
        elif info['code']==-100:
            currCourseOpenId = info['currCourseOpenId']
            currOpenClassId = info['currOpenClassId']
            currModuleId = info['currModuleId']
            curCellId = info['curCellId']
            currCellName = info['currCellName']
            lastPercent = info['lastPercent']
            # print(currCellName)
            self.continueStudy(currCourseOpenId,currOpenClassId,curCellId,currCellName,currModuleId)
            return self.viewDirectory(currCourseOpenId,currOpenClassId,curCellId,flag,currModuleId)
    #上传进度
    def stuProcessCellLog(self,courseOpenId,openClassId,cellId,cellLogId,token,studyNewlyTime):
        list = []  # 储存moduleId
        url = 'https://zjy2.icve.com.cn/common/Directory/stuProcessCellLog'
        date1 = {
                    'picNum':'9999',#ppt的进度
                    # 'studyNewlyTime': '9856.98',#视频进度
                    'studyNewlyPicNum': '9999'
        }
        date1['studyNewlyTime']=studyNewlyTime
        date1['courseOpenId']=courseOpenId
        date1['openClassId']=openClassId
        date1['cellId']=cellId
        date1['cellLogId']=cellLogId
        date1['token']=token

        req = urllib.request.Request(url=url, headers=header, data=urllib.parse.urlencode(date1).encode('utf-8'))
        req = opener.open(req)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.read().decode("utf-8"))
        print(info)#服务器返回提交是否成功代码
        return info['code']
    #
    def zjyUserOnlineTimeRedis(self,userId,userName,userDisplayName):
        list = []  # 储存moduleId
        url = 'https://dm.icve.com.cn/ZjyLogsManage/zjyUserOnlineTimeRedis'
        date1 = {}
        date1['userId'] = userId
        date1['userName']=userName
        date1['userDisplayName'] =userDisplayName
        req = urllib.request.Request(url=url, headers=header, data=urllib.parse.urlencode(date1).encode('utf-8'))
        req = opener.open(req)
        # 将读到的信息转换成json对象并写入到一个文件中
        info = json.loads(req.read().decode("utf-8"))
        # print(info)
    #计算课件量
    def CountPage(self,cName):
        count = 0
        # print('=============换课啦,得courseOpenId，openClassId====================')
        p = self.getProcessList(cName['courseOpenId'], cName['openClassId'])
        for i1 in p:
            # print('-------------------换模块啦，得Topic-----------------------------')
            m = self.getTopicByModuleId(cName['courseOpenId'], i1['moduleId'])
            # print(m)
            for i2 in m:
                # print("-----------------------换Topic,获取cellID-----------------------------")
                c = self.getCellByTopicId(cName['courseOpenId'], cName['openClassId'], i2['topicId'])

                for i3 in c:
                    # print('-----------------进入viewDirectory模式-----------------------------')
                    v = self.viewDirectory(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's', i1['moduleId'])
                    # print(v)
                    for i4 in v:
                        count=count+1
        return count
    #第一遍加载资源
    def LoadingCourse(self,cName):
        count = 0
        # print('=============换课啦,得courseOpenId，openClassId====================')
        p = self.getProcessList(cName['courseOpenId'], cName['openClassId'])
        for i1 in p:
            # print('-------------------换模块啦，得Topic-----------------------------')
            m = self.getTopicByModuleId(cName['courseOpenId'], i1['moduleId'])
            # print(m)
            for i2 in m:
                # print("-----------------------换Topic,获取cellID-----------------------------")
                c = self.getCellByTopicId(cName['courseOpenId'], cName['openClassId'], i2['topicId'])

                for i3 in c:
                    # print('-----------------进入viewDirectory模式-----------------------------')
                    v = self.viewDirectory(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's', i1['moduleId'])
                    # print(v)
                    for i4 in v:
                        count=count+1#计算总课件个数
                        # print(i4['cellPercent'])

                        if i4['cellPercent'] == 100:
                            self.stuProcessCellLog(cName['courseOpenId'], cName['openClassId'], i3['Id'],
                                                   i4['cellLogId'],
                                                   i4['guIdToken'])
                        else:
                            print('加载中>>>>')
                            self.stuProcessCellLog(cName['courseOpenId'], cName['openClassId'], i3['Id'], i4['cellLogId'],
                                              i4['guIdToken'])
                            v = self.viewDirectory(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's', i1['moduleId'])
                            #如果需要更新
                            if v[0]['isNeedUpdate']==1:
                                try:
                                    self.update(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's', i1['moduleId'], i4['categoryName'], self.name, self.pwo)
                                except:
                                    print(v)
                            print("加载完毕~")
        return count
    #开始刷课
    #基本思路
    #进入目录--》选择课件--》上传进度（若失败则停留11s,在重新上传）--》判断进度是否为100%--》进入下一个课件--》循环
    def doFlashBody(self,cName):
        isFinish=False
        while True:
            if isFinish:
                break
            isFinish = True
            # print('=============换课啦,得courseOpenId，openClassId====================')
            p = self.getProcessList(cName['courseOpenId'], cName['openClassId'])#获取进度
            for i1 in p:#遍历所有的课程名（courseopenid）
                if i1['percent']!=100:
                    # print('-------------------换模块啦，得Topic-----------------------------')
                    m = self.getTopicByModuleId(cName['courseOpenId'], i1['moduleId'])
                    # print(m)
                    for i2 in m:#遍历所有的ModuleId
                        # print("-----------------------换Topic,获取cellID-----------------------------")
                        c = self.getCellByTopicId(cName['courseOpenId'], cName['openClassId'], i2['topicId'])

                        for i3 in c:#遍历所有的topicid
                            # print('-----------------进入viewDirectory模式-----------------------------')
                            v = self.viewDirectory(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's', i1['moduleId'])
                            # print(v)
                            for i4 in v:#遍历所有的课程目录
                                # print('我是v:',v)
                                # print(i4['cellPercent'])
                                if i4['cellPercent'] == 100:#如果进度100%则跳过
                                    pass
                                else:#如果进度未满，则上传进度（10s一次）
                                    # print('--测试开始--')
                                    # print('提交')

                                    res=self.stuProcessCellLog(cName['courseOpenId'], cName['openClassId'], i3['Id'], i4['cellLogId'],
                                                      i4['guIdToken'],i4['audioVideoLong'])
                                    print(res)
                                    time.sleep(11)
                                    # print('---到此结束----')


                                    v = self.viewDirectory(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's', i1['moduleId'])
                                    #如果需要更新
                                    if v[0]['isNeedUpdate']==1:
                                        try:
                                            self.update(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's', i1['moduleId'], i4['categoryName'], self.name, self.pwo)
                                        except:
                                            print(v)
                                    num=v[0]['cellPercent']#获取进度
                                    print("刷完之后：", num)

                                    guIdToken=v[0]['guIdToken']
                                    # print('新的logcid:',guIdToken)
                                    if num!=100:#如果单个课件没有刷满
                                        while True:#循环
                                            time.sleep(11)
                                            code=self.stuProcessCellLog(cName['courseOpenId'], cName['openClassId'], i3['Id'],
                                                                   i4['cellLogId'],
                                                                   guIdToken,i4['audioVideoLong'])  # 提交一次
                                            flash = self.viewDirectory(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's',
                                                              i1['moduleId'])#查看一下情况
                                            if flash[0]['isNeedUpdate'] == 1:
                                                self.update(cName['courseOpenId'], cName['openClassId'], i3['Id'], 's', i1['moduleId'],
                                                       i4['categoryName'], self.name, self.pwo)#更新资源
                                            num=flash[0]['cellPercent']#课程进度
                                            guIdToken=flash[0]['guIdToken']
                                            if code!=1:
                                                isFinish=False
                                            if num==100 or code!=1:
                                                break
                                            print('循环:', num)
                else:
                    print("已完成！")
    def loopFlash(self,list):
        while True:
            if self.checkIsFinish(list)==True:
                break;
            courseList=self.getLearnningCourseList()
            for i in list:
                try:
                    self.doFlashBody(courseList[i])
                except:
                    print("异常跳过")
                    pass
            return 'finish'
    def checkIsFinish(self,list):
        Courselist = z.getLearnningCourseList() #获取课程
        for i in list:
            if Courselist[i]['process'] != 100:
                print(Courselist[i]['process'])
                return False
            else:
                print(Courselist[i]['process'])
        return True
header = {
            'Origin': 'https://mooc.icve.com.cn',
            'Referer': 'https://mooc.icve.com.cn/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
}
if __name__ == '__main__':

    z=zhihui()
    # z.login('081218191','sui2001.')
    z.login('lnnzy44','lwlnwsmbawl521.')#登陆
    list=z.getLearnningCourseList()#获取课程
    print(list)
    z.doFlashBody(list['园艺植物栽培四'])
    # '园艺植物栽培四','食用菌盆艺栽培','微生物应用技术','园艺植物病虫害防治','植物组织培养三（生技18）','无土栽培'
    # courseList=['园艺植物栽培四','食用菌盆艺栽培','微生物应用技术','园艺植物病虫害防治','植物组织培养三（生技18）','无土栽培']#课程列表
    # z.loopFlash(courseList)





