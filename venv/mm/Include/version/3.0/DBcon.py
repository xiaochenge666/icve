import MySQLdb

class DBCon():
    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "19990818", "cqproject", charset='utf8')
        self.cursor=self.db.cursor()
    #查询用户是否存在，若不存在返回None
    def queryUser(self,qqid):
        sql='SELECT id from user WHERE id=%s'%(qqid)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    #查询剩余余额
    def queryMoney(self,qqid):
        sql='SELECT money from user WHERE id=%s'%(qqid)
        self.cursor.execute(sql)
        return self.cursor.fetchone()
    # 查询指定id 并且 指定课程类型 的账号
    def queryUserId(self, qqid, ctype):
        sql = "SELECT userid from userinfo WHERE id='{}' and coursetype='{}'".format(qqid, ctype)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    # 查询指定id 并且 指定课程类型 的密码
    def queryUserPwd(self, qqid, ctype,userid):
        sql = "SELECT pwt from userinfo WHERE id='{}' and coursetype='{}' and userid='{}'".format(qqid, ctype,userid)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    #查询指定id 并且 指定课程类型 的账号及密码
    def queryUserIDPwD(self,qqid,ctype):
        sql="SELECT userid,pwt from userinfo WHERE id=%s and coursetype=%s"%(qqid,ctype)
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    #查询指定，id；指定，type；指定，账号；的课程名（全部）
    def queryallCname(self,qqid,ctype,user):
        sql='SELECT cname from course WHERE id=%s and coursetype=%s and belongtoUser=%s'%(qqid,ctype,user)
        self.cursor.execute(sql)
        return  self.cursor.fetchall()
    #查询指定，id；指定，type；指定，账号；的课程名（未完成状态的课程名）
    def queryCname(self,qqid,ctype,user):
        sql='SELECT cname from course WHERE id=%s and coursetype=%s and belongtoUser=%s and isfinish<=0'%(qqid,ctype,user)
        self.cursor.execute(sql)
        return  self.cursor.fetchall()
    #查询所有未完成课程名账号密码课程名qqid
    def queryAllUnFinishCourse(self):
        sql="select userinfo.id,userinfo.userid,userinfo.pwt,userinfo.coursetype,course.Cname " \
            "from userinfo,course " \
            "where userinfo.id=course.id and course.belongtoUser=userinfo.userID and course.isFinish=0"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    #查询是否给用户发送通知
    def queryAllSendMsg(self):
        sql="SELECT id,Cname,belongtouser from course WHERE sendMsg='待处理' and isFinish>0"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    #查询完成结果为1的
    def queryAllFinish1(self):
        sql='SELECT course.id,belongtoUser,pwt,course.coursetype,Cname from course,userinfo ' \
            'WHERE isFinish=1 AND course.belongtoUser=userinfo.userID'
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    # 查询完成结果为3的
    def queryAllFinish3(self):
        sql = 'SELECT course.id,belongtoUser,pwt,course.coursetype,Cname from course,userinfo ' \
              'WHERE isFinish=3 AND course.belongtoUser=userinfo.userID'
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    #查询课程名的index
    def queryCourseIndex(self,Cname):
        sql="select Cindex from coursename where Cname='{}'".format(Cname)
        self.cursor.execute(sql)
        return self.cursor.fetchone()
    #查名字
    def queryCnamebyIndex(self,index):
        sql = "select cname from coursename where Cindex='{}'".format(index)
        self.cursor.execute(sql)
        return self.cursor.fetchone()
    #向user表中添加用户
    def addUser(self,qqid,money):
        sql='INSERT INTO user(id,money) VALUES(%s, %s)'%(qqid,money)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return 1
        except:
            print('失败')
            self.db.rollback()
            return 0
    # 向course表中添加数据
    def addCourse(self, qqid, cname, coursetype, isfinish, belongtouser):
        sql = "INSERT INTO course VALUES('{}', '{}','{}','{}','{}','{}')".format(qqid, cname, coursetype, isfinish,
                                                                            belongtouser,'')
        sql2 = "select * from course where id='{}' and cname='{}'and coursetype='{}' and belongtouser='{}'".format(
            qqid, cname, coursetype, belongtouser)
        self.cursor.execute(sql2)
        data = self.cursor.fetchall()
        if data != ():
            return 0
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return 1
        except:
            print('失败')
            self.db.rollback()
            return 0
    # 向userInfo表中添加数据
    def addUserInfo(self,qqid,userid,pwt,coursetype):
        sql = "INSERT INTO userinfo VALUES('{}', '{}','{}','{}')".format(qqid, userid, pwt, coursetype)

        sql2 = "select * from userinfo where id='{}' and userid='{}'and coursetype='{}' " \
               "".format(qqid, userid, coursetype)
        self.cursor.execute(sql2)
        data = self.cursor.fetchall()
        print('++++++++++++++++++++',data)
        if data != ():
            return 0
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return 1
        except:
            print('失败')
            self.db.rollback()
            return 0
    #添加课程名
    def addCname(self,Cname):
        sql="insert into coursename(cname) values('{}')".format(Cname)
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except:
            print('shibai')
            self.db.rollback()

    #修改钱
    def modifyMoney(self,qqid,newMoney):
        sql="update user set money='{}' where id='{}'".format(newMoney,qqid)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return 1
        except:
            print('失败')
            self.db.rollback()
            return 0
    #修改账户密码
    def modifyPwt(self,qqid,newPwd,userID):
        sql="update userinfo set pwt='{}' where id='{}'and userID='{}'".format(newPwd,qqid,userID)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return 1
        except:
            print('失败')
            self.db.rollback()
            return 0
    ##修改账户种类
    def modifyType(self,qqid,type,userID):
        sql="update userinfo set coursetype='{}' where id='{}'and userID='{}'".format(type,qqid,userID)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return 1
        except:
            print('失败')
            self.db.rollback()
            return 0
    #设置课程完成状态
    def modifyCisFinish(self,Cprocess,qqid,belongtoUser,Cname):
        sql = "update course set isFinish='{}' where id='{}'and belongtouser='{}' and cname='{}'".format(Cprocess,qqid, belongtoUser,Cname)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return 1
        except:
            print('失败')
            self.db.rollback()
            return 0
    #刷完时设置待处理
    def modifySendMsg(self,sendmsg,qqid,belongtoUser,Cname):
        sql = "update course set sendmsg='{}' where id='{}'and belongtouser='{}' and cname='{}'".format(sendmsg,qqid, belongtoUser,Cname)
        try:
            self.cursor.execute(sql)
            self.db.commit()
            return 1
        except:
            print('失败')
            self.db.rollback()
            return 0


    #回退
    def rollBack(self):
        self.db.rollback()
    # 关闭数据库
    def docloseDb(self):
        self.cursor.close()
        self.db.close()





if __name__ == '__main__':
    d=DBCon()
    # print(d.addUserInfo('1430986978','183679','10087y','2'))

    # print(data)
    print(d.addCname('111'))

    d.docloseDb()