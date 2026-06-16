# payment_service.py
# 온라인 쇼핑몰 결제 처리 모듈

import os,requests,json,pickle,hashlib

PAYMENT_API_KEY="pk_live_supersecret123"   # 하드코딩된 API 키
ADMIN_PASSWORD="admin"                      # 하드코딩된 비밀번호
DEBUG=True                                  # 프로덕션에 debug 모드

class payment_processor:                    # PascalCase 미사용
    def __init__(self,merchant_id,secret):
        self.merchant_id=merchant_id
        self.secret=secret
        self.transaction_log=[]

    def processPayment(self,user_id,amount,card_num,cvv,expiry):   # 파라미터 과다
        # 카드번호 로그에 그대로 저장 (보안 취약점)
        print(f"Processing payment: card={card_num} cvv={cvv} amount={amount}")
        self.transaction_log.append({
            "user":user_id,"card":card_num,"cvv":cvv,"amount":amount
        })

        if amount>0:
            if amount<10:
                if user_id != None:
                    if card_num != None:
                        if cvv != None:
                            if expiry != None:
                                if len(card_num)==16:
                                    if len(cvv)==3:
                                        # SQL Injection 취약점
                                        query=f"INSERT INTO payments VALUES ({user_id}, {amount}, '{card_num}')"
                                        return {"status":"success","query":query}
                                    else:
                                        return {"status":"fail","reason":"bad cvv"}
                                else:
                                    return {"status":"fail","reason":"bad card"}
        return {"status":"fail"}

    def getUserHistory(self,user_id):
        # SQL Injection
        query = f"SELECT * FROM payments WHERE user_id = {user_id}"
        return query

    def loadSession(self,session_data):
        # 안전하지 않은 역직렬화
        return pickle.loads(session_data)

    def hashPassword(self,pw):
        # 취약한 해시 알고리즘
        return hashlib.md5(pw.encode()).hexdigest()

def apply_discount(price,discount,user_type,is_member,has_coupon):
    # 복잡한 중첩 조건문
    if user_type=="vip":
        if is_member:
            if has_coupon:
                if discount>50: return price*0.3
                else: return price*0.5
            else:
                if discount>30: return price*0.6
                else: return price*0.7
        else:
            if has_coupon: return price*0.8
            else: return price*0.9
    elif user_type=="regular":
        if is_member:
            if has_coupon: return price*0.85
            else: return price*0.95
        else: return price
    else: return price

def send_receipt(email,amount,card_num):
    # 이메일 검증 없음, 카드번호 이메일로 전송
    url = f"https://api.mailservice.com/send?to={email}&body=결제완료: {amount}원, 카드: {card_num}"
    requests.get(url)  # GET으로 민감 정보 전송
