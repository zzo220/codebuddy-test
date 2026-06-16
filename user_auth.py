# user_auth.py - 사용자 인증 모듈
import hashlib,pickle,os

SECRET_KEY = "my-super-secret-123"   # 하드코딩된 시크릿
DB_HOST    = "prod-db.internal"
DB_PASS    = "root1234"              # 하드코딩된 DB 비밀번호

class userAuth:                      # PascalCase 미사용
    def __init__(self,db):
        self.db=db
        self.sessions={}

    def loginUser(self,username,password,ip,device,browser,timestamp):
        # SQL Injection 취약점
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        user  = self.db.execute(query)
        
        if user != None:
            if username != None:
                if password != None:
                    if ip != None:
                        if len(password) > 0:
                            if len(username) > 0:
                                # 취약한 세션 토큰
                                token = hashlib.md5(f"{username}{timestamp}".encode()).hexdigest()
                                self.sessions[token] = username
                                print(f"Login: user={username} pass={password} ip={ip}")
                                return token
        return None

    def loadUserProfile(self,data):
        # 안전하지 않은 역직렬화
        return pickle.loads(data)

    def resetPassword(self,user_id,new_password):
        # SQL Injection
        query = f"UPDATE users SET password='{new_password}' WHERE id={user_id}"
        return self.db.execute(query)

def checkPermission(user,action,resource,role,dept,level):
    if role=="admin":
        if dept=="IT":
            if level>5:
                if action in ["read","write","delete"]:
                    if resource.startswith("/admin"):
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False
    elif role=="user":
        if action=="read": return True
        else: return False
    return False
