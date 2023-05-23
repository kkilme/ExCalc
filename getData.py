import requests
from datetime import datetime,timedelta
import pickle
from lists import countryName, countryhasdata
import time

class getData:
    def __init__(self):
        self.mykey = "atevqf24Qbq7EKUNTWNZRgjLZi9YkzKL" # api 발급 키
        if int(datetime.now().strftime('%H')) < 9:  # 오전 9시 이전일 시 오늘 날짜를 어제 날짜로
            self.today = (datetime.now() + timedelta(days=-1))
        else :
            self.today = datetime.now()
            # self.today = (datetime.now() + timedelta(days=-700))
        self.url = "https://www.koreaexim.go.kr/site/program/financial/exchangeJSON" # api 요청 링크
        self.dbfile = 'ExRateDB.dat' # 환율 데이터 파일 이름
        self.period = 800 # 기간 (수정 가능)
        self.startdate = (self.today - timedelta(days=(self.period))).strftime('%Y-%m-%d') # 시작 날짜
        self.param = {'authkey':self.mykey, 'searchdate':self.startdate, 'data':'AP01'} # api 요청에 필요한 파라미터


    def parseData(self, parsedData):
        count = 0
        t = time.time()
        date = self.startdate # 시작날짜
        
        if len(parsedData) == 0:
            for name in countryName:
                parsedData[name] = {} #딕셔너리 내의 딕셔너리 초기화

        # print("parseddata: ", parsedData)

        for _ in range(self.period):
            date = (datetime.strptime(date,'%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') # 날짜를 다음 날짜로
            # print(date)
            for country in countryhasdata: # 해당 날짜에 데이터가 없는 나라 판별용 딕셔너리, false로 초기화
                countryhasdata[country] = False

            if date in parsedData['아랍에미리트 디르함 (AED)'] : continue # 이미 데이터 있을 시 넘기기

            self.param['searchdate'] = date
            print('request start')
            response = requests.get(self.url,self.param) # api 요청
            rawdata = response.json()
            print('response done')
            count += 1

            # print("rawdata : ", rawdata)
            if len(rawdata) == 0: # 데이터 없을 시 이전 날 데이터 저장
                for country in parsedData:
                    prvday = (datetime.strptime(date,'%Y-%m-%d') - timedelta(days=1)).strftime('%Y-%m-%d')
                    try:
                        parsedData[country][date] = parsedData[country][prvday]
                    except:
                        parsedData[country][date] = 0
                continue

            for d in rawdata:
                if d['result'] == 1:
                    tempEx = float(d['deal_bas_r'].replace(",","")) # 환율 값에서 단위 쉼표 제거 후 float형으로 변환

                    if d['cur_unit'] == 'IDR(100)' or d['cur_unit'] == 'JPY(100)' : # 인도네시아, 일본 : 특수 케이스
                        d['cur_unit'] = d['cur_unit'].replace("(100)","")
                        tempEx = float(f"{tempEx/100:.4f}")

                    if d['cur_unit'] == 'KRW' : continue # 한국 패스

                    country = f"{d['cur_nm']} ({d['cur_unit']})"
                    parsedData[country][date] =  tempEx # 딕셔너리 업데이트
                    countryhasdata[country] = True # 해당 나라는 데이터 있음으로 표시
                    
                else : 
                    print("result code error:", d['result'], date) # result code error
                    break
            
            for country in countryhasdata: # 해당 날짜의 특정 국가만 데이터가 없는 경우
                if countryhasdata[country] == False:
                    parsedData[country][date] = 0
            

        # 0 제거
        for country in parsedData:
            for date in parsedData[country]:
                # if date == self.today.strftime('%Y-%m-%d') : pass
                if parsedData[country][date] == 0 :
                    print(country)
                    print(parsedData[country])
                    nxtday = (datetime.strptime(date,'%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                    try:
                        while parsedData[country][nxtday] == 0:
                            nxtday = (datetime.strptime(nxtday,'%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
                    except :
                        print("All 0") 
                        break #모든 날 값이 0일 시
                    try:
                        parsedData[country][date] = parsedData[country][nxtday]
                    except:
                        parsedData[country][date] = 0

        # print("after parse: ", parsedData)
        print("api request count: ", count) #api 요청횟수
        for country in parsedData:
            parsedData[country] = dict(sorted(parsedData[country].items(), key = lambda x:x[0]))
        self.writeDB(parsedData)
        print(time.time() - t, "소요됨")
        return parsedData

    # 환율 데이터 파일 읽기
    def readDB(self):
        try:
            exrateDBdat = open(self.dbfile, 'rb')
        except FileNotFoundError as e:
            print("No file")
            exrateDB = self.parseData({})
            return exrateDB

        exrateDB =  pickle.load(exrateDBdat)
        
        if list(exrateDB['아랍에미리트 디르함 (AED)'].keys())[0] != (datetime.strptime(self.startdate,'%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d') : # 저장된 데이터의 시작 날짜가 다를 시 다시 받아오기
            print("Not same start date", self.startdate, list(exrateDB['아랍에미리트 디르함 (AED)'].keys())[0])
            exrateDB = self.parseData(exrateDB)
            exrateDBdat.close()
            return exrateDB
        
        exrateDBdat.close()
        print("Successfully opened datafile")
        return exrateDB

    # 환율 데이터 파일 쓰기
    def writeDB(self, exrateDB):
        exrateDBdat = open(self.dbfile, 'wb')
        pickle.dump(exrateDB, exrateDBdat)
        exrateDBdat.close()
