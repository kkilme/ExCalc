from itertools import count
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime,timedelta
from lists import moneyName

def graph(startdate, enddate, country, db):
    plt.close('all')  # 열려있는 창 닫기
    startdate = datetime.strptime(startdate,'%Y-%m-%d') # 그래프 시작 날짜
    enddate = datetime.strptime(enddate,'%Y-%m-%d') # 그래프 끝 날짜
    periodDays = (enddate-startdate).days # 기간
    tempEndDate = enddate + timedelta(days=1) # 끝 날짜 다음날
    rates = [] # 지정된 기간동안의 환율이 저장됨
    dates = [] # 지정된 기간동안의 날짜 하루하루가 저장됨
    d = startdate.strftime('%Y-%m-%d')
    for _ in range(periodDays+1):
        dates.append(d)
        rates.append(float(db[country][d]))
        d = (datetime.strptime(d,'%Y-%m-%d') + timedelta(days=1)).strftime('%Y-%m-%d')
    days = mdates.drange(startdate,tempEndDate,timedelta(days=1)) # matplotlib date format
    maxrate = max(rates)# 최대 환율
    minrate = min(rates) # 최소 환율
    maxdateString = dates[rates.index(maxrate)] # 최대 환율 날짜
    mindateString = dates[rates.index(minrate)] # 최소 환율 날짜
    # maxdate = datetime.strptime(maxdateString, '%Y-%m-%d')
    # maxdate = mdates.date2num(maxdate)

    # 기간 길이에 따라서 그래프 x축 날짜의 간격이 정해짐
    if periodDays > 630 :
        inter = 60
    elif periodDays > 180 :
        inter = 30
    elif periodDays > 20 :
        inter = 7
    else : inter = 1

    # 그래프 x축 지정
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=inter))
    plt.gca().set_xlim(startdate, enddate)
    plt.gcf().autofmt_xdate()

     # 기간 길이에 따라서 그래프의 점과 선의 스타일이 정해짐
    if inter > 50 : plt.plot(days, rates, '.-', color = 'navy', linewidth = 1, markersize = 2)
    elif inter > 20 : plt.plot(days, rates, '.-', color = 'navy', linewidth = 1.5, markersize = 3)
    else : plt.plot(days, rates, 'o-', color = 'navy')
    
    plt.grid(True) # 그래프 그리드 활성화
    mngr = plt.get_current_fig_manager()
    mngr.window.setGeometry(1400,210,1000,545) # 그래프 창 크기 및 위치
    # plt.xlabel("Date", labelpad=10, fontdict={'family': 'Courier New', 'color': 'black', 'weight': 'bold', 'size': 14} , loc='right')
    plt.ylabel("Exchange Rate", labelpad=25, fontdict={'family': 'Courier New', 'color': 'black', 'weight': 'bold', 'size': 14}) # y축 라벨
    plt.title(f'{moneyName[country]}\nMax {maxdateString}, {maxrate} // Min {mindateString}, {minrate}') # 그래프 제목 (최대 최소 환율 정보 포함)
    # plt.gca().annotate(f'Max {maxdateString}, {maxrate}', xy=(maxdate, maxrate), xytext=(maxdate, maxrate),horizontalalignment='right',
    #         verticalalignment='top')
    # arrowprops=dict(facecolor='black', shrink=0.1, width = 9, headwidth = 2.2)
    plt.ion()
    plt.show()
