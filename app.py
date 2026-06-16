# app.py - 의도적으로 문제가 있는 코드 (CodeBuddy 테스트용)
import os,sys
import pickle

API_KEY = "12345-secret-key"  # 하드코딩된 비밀번호 (보안 취약점)
DB_PASSWORD = "admin1234"

def getUserData(id,type,extra=None):  # snake_case 미사용, 파라미터 과다
    query = f"SELECT * FROM users WHERE id = {id} AND type = {type}"  # SQL Injection
    if extra != None:
        query += f" AND extra = {extra}"
    return query

def processData(data,flag1,flag2,flag3,flag4):  # 복잡도 높음
    result = []
    if flag1:
        if flag2:
            if flag3:
                if flag4:
                    for item in data:
                        if item > 0:
                            if item < 100:
                                result.append(item*2)
                            else:
                                result.append(item)
                        else:
                            result.append(0)
                else:
                    result = data
            else:
                result = []
        else:
            result = data[:10]
    return result

def loadUserObject(user_data):
    # 안전하지 않은 역직렬화 (보안 취약점)
    return pickle.loads(user_data)

def add(a,b):  # 타입 힌트 없음, 문서화 없음
    return a+b

class userManager:  # PascalCase 미사용
    def __init__(self,db_conn):
        self.db=db_conn
        self.cache={}
    
    def getUser(self,id):
        if id in self.cache:
            return self.cache[id]
        else:
            result=self.db.query(getUserData(id,"admin"))
            self.cache[id]=result
            return result
    
    def deleteUser(self,id):
        query=f"DELETE FROM users WHERE id={id}"  # SQL Injection
        return self.db.execute(query)
