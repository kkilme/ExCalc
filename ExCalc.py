import sys
from PyQt5.QtWidgets import ( QWidget, QHBoxLayout, QVBoxLayout, QApplication, QLabel,
    QComboBox,QLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5 import QtGui
from getData import getData
from lists import countryName
from datetime import timedelta, date
from QClasses import DateLineEdit, CalcLineEdit, BigBoldText, Button, ChartTextEdit
from graph import graph

class ExCalc(QWidget):
    def __init__(self):
        super().__init__()
        self.getdata = getData() # 환율 정보를 받아오기 위한 객체 생성
        self.db = self.getdata.readDB() # 파일 읽어오기
        self.firstdate = list(self.db['유로 (EUR)'].keys())[0]
        self.today = self.getdata.today.strftime('%Y-%m-%d')
        self.DateNow = self.today
        # print(len(self.db))
        # print(self.db)
        print("데이터에 저장된 날짜 수:", len(self.db['아랍에미리트 디르함 (AED)']))
        # print(self.db['브루나이 달러 (BND)'])
        self.initUI()
        self.showChart()

    def initUI(self):
        # 현재 설정된 날짜 라벨
        self.DateNowL = QLabel("Current Date : "+ self.DateNow ,self)
        self.DateNowL.setAlignment(Qt.AlignCenter)
        self.DateNowL.setStyleSheet("color: blue;"
                      "border-style: solid;"
                      "border-width: 2px;"
                      "border-color: #A9ABA7;"
                      "border-radius: 3px;"
                      "background-color: #FFFFFF")
        self.DateNowL.setFont(QtGui.QFont("Times",weight=QtGui.QFont.Bold))

        # 최대 날짜 라벨
        LimitL = QLabel("Date Limit: " + self.firstdate, self)
        LimitL.setAlignment(Qt.AlignCenter)
        LimitL.setStyleSheet("color: red")

        
        # 현재 날짜 설정
        SetDateL = QLabel("Set Date:", self)
        self.SetDateYear = DateLineEdit()
        self.SetDateYear.setMaxLength(4)
        self.SetDateYear.setPlaceholderText("Year")
        self.SetDateMonth = DateLineEdit()
        self.SetDateMonth.setMaxLength(2)
        self.SetDateMonth.setPlaceholderText("Month")
        self.SetDateDay = DateLineEdit()
        self.SetDateDay.setMaxLength(2)
        self.SetDateDay.setPlaceholderText("Day")

        ButtonToday = Button("Today", self.SetDateButtonCliked)
        ButtonApply = Button("Apply", self.SetDateButtonCliked)
        
        # 날짜 설정 에러 라벨
        self.SetDateErrorL = QLabel("Error: not valid date", self)
        self.SetDateErrorL.setAlignment(Qt.AlignCenter)
        self.SetDateErrorL.setStyleSheet("color: red")
        self.SetDateErrorL.setHidden(True) 

        # "Table" 라벨
        TableL = BigBoldText("-----------------------  Table  -----------------------")

        # Table View Mode 설정
        ViewModeL = QLabel("View mode:", self)
        self.ViewModeCBox = QComboBox(self)
        # self.ViewModeCBox.setAlignment(Qt.AlignCenter)
        self.ViewModeCBox.setEditable(True)
        self.ViewModeCBox.addItem("=> KRW")
        self.ViewModeCBox.addItem("1000 KRW =")
        ViewModeLEdit = self.ViewModeCBox.lineEdit()
        ViewModeLEdit.setAlignment(Qt.AlignCenter)
        ViewModeLEdit.setReadOnly(True)
        self.ViewModeCBox.activated[str].connect(self.showChart)

        # Chart
        self.RateBox = ChartTextEdit()
        self.RateBox.setCurrentFont(QFont('Courier New'))

        # "Calculator" 라벨
        CalculatorL = BigBoldText("----------------------  Calculator  ----------------------")

        # Calculator 에러 메시지
        self.CalcErrorL = QLabel("Error: Not valid value", self)
        self.CalcErrorL.setAlignment(Qt.AlignCenter)
        self.CalcErrorL.setStyleSheet("color: red")
        self.CalcErrorL.setHidden(True)

        # Calculator
        self.fromCnt = QComboBox(self)
        self.fromCnt.setFixedSize(220,25)
        self.toCnt = QComboBox(self)
        self.toCnt.setFixedSize(220,25)
        self.fromNum = CalcLineEdit()
        self.fromNum.setPlaceholderText("Max: 1,000,000,000,000")
        self.fromNum.setMaxLength(21)
        self.fromNum.editingFinished.connect(self.fromNumChanged)
        self.toNum = CalcLineEdit()
        self.toNum.setReadOnly(True)
        equalL = BigBoldText("=")
        self.ButtonCalc = Button("Calc!", self.CalcButtonClicked)

        for box in [self.fromCnt, self.toCnt]:
            box.addItem("한국 원 (KRW)")
            for country in countryName:
                box.addItem(country)
        self.toCnt.setCurrentText("미국 달러 (USD)")

        # Graph
        GraphL = BigBoldText("------------------------  Graph  ------------------------")
        selectPeriod = QLabel("Select Period :")
        self.selectPeroidError = QLabel("The period is not in db", self)
        self.selectPeroidError.setHidden(True)
        self.selectPeroidError.setAlignment(Qt.AlignCenter)
        self.selectPeroidError.setStyleSheet("color: red")
        # self.selectPeroidError.setHidden(True)
        self.startdate = self.firstdate
        self.period = QLabel("Current Period : "+self.startdate+"  ~  "+self.today)
        pfont = self.period.font()
        pfont.setBold(True)
        pfont.setPointSize(11)
        self.period.setFont(pfont)
        self.period.setAlignment(Qt.AlignCenter)
        self.graphCountry = QComboBox(self)
        for country in countryName:
                self.graphCountry.addItem(country)
        self.ButtonAll = Button("All", self.graphButtonClicked)
        self.ButtonYear = Button("A year", self.graphButtonClicked)
        self.ButtonMonth = Button("A month", self.graphButtonClicked)
        self.ButtonWeek = Button("A week", self.graphButtonClicked)
        self.ButtonShow = Button("Show!", self.graphButtonClicked)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(2)
        hbox1.addWidget(SetDateL)
        hbox1.addWidget(self.SetDateYear)
        hbox1.addWidget(self.SetDateMonth)
        hbox1.addWidget(self.SetDateDay)
        hbox1.addWidget(ButtonToday)
        hbox1.addWidget(ButtonApply)
        hbox1.addStretch(2)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(3)
        hbox2.addWidget(ViewModeL)
        hbox2.addWidget(self.ViewModeCBox)
        hbox2.addStretch(3)
    
        hbox25 = QHBoxLayout()
        hbox25.addStretch(1)
        hbox25.addWidget(self.RateBox)
        hbox25.addStretch(1)

        hboxeswidget = [[self.fromCnt,self.fromNum],[equalL],[self.toCnt,self.toNum],[self.ButtonCalc]]
        hboxes = []
        for widget in hboxeswidget:
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            for w in widget:
                hbox.addWidget(w)
            hbox.addStretch(1)
            hboxes.append(hbox)

        hbox9 = QHBoxLayout()
        hbox9.addStretch(1)
        hbox9.addWidget(selectPeriod)
        hbox9.addWidget(self.ButtonAll)
        hbox9.addWidget(self.ButtonYear)
        hbox9.addWidget(self.ButtonMonth)
        hbox9.addWidget(self.ButtonWeek)
        hbox9.addStretch(1)
        
        hbox10 = QHBoxLayout()
        hbox10.addStretch(1)
        hbox10.addWidget(self.graphCountry)
        hbox10.addWidget(self.ButtonShow)
        hbox10.addStretch(1)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.DateNowL)
        vbox.addWidget(LimitL)        
        vbox.addLayout(hbox1)
        vbox.addWidget(self.SetDateErrorL)
        vbox.addWidget(TableL)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox25)
        vbox.addWidget(CalculatorL)
        vbox.addWidget(self.CalcErrorL)
        for hbox in hboxes:
            vbox.addLayout(hbox)
        vbox.addWidget(GraphL)
        vbox.addWidget(self.selectPeroidError)
        vbox.addWidget(self.period)
        vbox.addLayout(hbox9)
        vbox.addLayout(hbox10)
        vbox.addStretch(0)

        vbox.setSizeConstraint(QLayout.SetFixedSize)
        self.setLayout(vbox)
        self.setGeometry(700, 200, 600, 250)
        
        self.setWindowTitle('ExRateCalculator')    
        self.show()
    
    def SetDateButtonCliked(self):
        button = self.sender()
        key = button.text()

        if key == "Today":
            self.SetDateYear.setText(str(self.getdata.today.year))
            self.SetDateMonth.setText(str(self.getdata.today.month))
            self.SetDateDay.setText(str(self.getdata.today.day))
        
        if key == "Apply":
            try :
                year = int(self.SetDateYear.text())
                month = int(self.SetDateMonth.text())
                day = int(self.SetDateDay.text())
            except:
                self.SetDateErrorL.setHidden(False)
                return
            try : 
                datenow = date(year, month, day).isoformat()
                if not datenow in list(self.db['유로 (EUR)'].keys()):
                    self.SetDateErrorL.setHidden(False)
                    return
                else:
                    self.SetDateErrorL.setHidden(True)
                    self.DateNow = datenow
                    self.DateNowL.setText("Current Date : "+ self.DateNow)
                    self.showChart()
                    if self.fromNum.text() != '':
                        self.CalcButtonClicked()
            except :
                self.SetDateErrorL.setHidden(False)
    
    def CalcButtonClicked(self):
        # button = self.sender()
        # key = button.text()
        # if key == "Calc!":
        self.fromNumChanged()
        num = self.fromNum.text().replace(",","")
        try:
            moneyFrom = int(num)
        except:
            moneyFrom = float(num)
        try:
            currentFromRate = self.db[self.fromCnt.currentText()][self.DateNow]
        except:
            currentFromRate = 1
        try:
            currentToRate = self.db[self.toCnt.currentText()][self.DateNow]
        except:
            currentToRate = 1
        
        moneyTo = (currentFromRate/currentToRate)*moneyFrom
        moneyTo = f"{moneyTo:,.6f}" if moneyTo < 10 else f"{moneyTo:,.3f}"
        self.toNum.setText(moneyTo)

    def fromNumChanged(self):
        self.CalcErrorL.setHidden(True)
        num = self.fromNum.text().replace(",","")
        if not (num.replace(".","")).isdigit() or num.count('.') > 1:
            self.fromNum.setText('0')
            self.CalcErrorL.setHidden(False)
            return
        try:
            num = int(num)
            if(num > 1000000000000): num = 1000000000000
            txt = f"{num:,}"
            self.fromNum.setText(txt)
        except:
            num = float(num)
            if(num > 1000000000000): num = 1000000000000
            num = round(num, 3)
            txt = f"{num:,}"
            self.fromNum.setText(txt)
    
    def showChart(self):
        box = self.RateBox
        box.clear()
        if self.ViewModeCBox.currentText() == "=> KRW":
            box.setFontWeight(300)
            box.setFontPointSize(14)
            topText = "\tCountry\t\t    KRW\t"
            box.append(topText)
            box.setFontPointSize(10)
            # box.setFontWeight(QFont.Weight.Normal)
            box.append("--------------------------------------------------")
            for country in countryName:
                krw = self.db[country][self.DateNow]
                country = country.ljust(19)
                space = country.count(' ')
                krw = (space-3)*' '+str(krw)
                txt = f'    1 {country}{krw} KRW'
                box.append(txt)
                box.append("--------------------------------------------------")
            box.verticalScrollBar().setValue(0) #스크롤 맨위로

        if self.ViewModeCBox.currentText() == "1000 KRW =":
            box.setCurrentFont(QFont('Courier New'))
            box.setFontWeight(300)
            box.setFontPointSize(14)
            topText = "\t\t  1000 KRW =\t\t"
            box.append(topText)
            box.setFontPointSize(10)
            # box.insertPlainText("test")
            box.append("--------------------------------------------------")
            for country in countryName:
                krw = f'{1000.0/self.db[country][self.DateNow]:.4f}'
                txt = f'\t        {krw} {country} \t'
                box.append(txt)
                box.append("--------------------------------------------------")
            box.verticalScrollBar().setValue(0)

    def graphButtonClicked(self):
        button = self.sender()
        key = button.text()
        self.selectPeroidError.setHidden(True)
        if key == 'All':
            self.startdate = self.firstdate
        if key == 'A year':
            self.startdate = (self.getdata.today - timedelta(days=365)).strftime('%Y-%m-%d')
        if key == 'A month':
            self.startdate = (self.getdata.today - timedelta(days=30)).strftime('%Y-%m-%d')
        if key == 'A week':
            self.startdate = (self.getdata.today - timedelta(days=7)).strftime('%Y-%m-%d')
        if key == 'Show!':
            graph(self.startdate, self.today, self.graphCountry.currentText(), self.db)
        
        if self.startdate not in list(self.db["유로 (EUR)"].keys()):
            self.selectPeroidError.setHidden(False)
        self.period.setText("Current Period : "+self.startdate+"  ~  "+self.today)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    calc = ExCalc()
    sys.exit(app.exec_())

