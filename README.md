# ExCalc
## **환율 계산 및 환율 변동에 관한 그래프를 제공하는 프로그램**

대학교 1학년 2학기 소프트웨어프로젝트 2 강의에서 진행한 프로젝트로, 1년 반 가까이 지났지만 보존을 위해 늦게라도 Git에 업로드.

<p align="center">
<img src="https://github.com/kkilme/ExCalc/assets/80762534/0040760e-ae64-4a92-b303-35b6fe56591b" width='auto' height='800'>
</p>

## 특징
- 한국수출입은행이 제공하는 공식 API 활용
- **PyQT5** 패키지를 이용하여 UI 구현
- **matplotlib** 패키지를 이용하여 그래프 기능 구현

## 기능
- 특정 날짜의 환율을 알려줌
- 특정 날짜의 환율을 이용하여 각국 통화간 환율 계산
- 특정 기간동안, 특정 통화의 환율 변동을 그래프로 보여줌

<p align="center">
<img src="https://github.com/kkilme/ExCalc/assets/80762534/7a9b3d72-0a24-4c12-9085-c51c1364cc39">
</p>

## 파일 설명
- ExCalc.py
  - 메인 클래스, 해당 파일을 실행하여 프로그램 실행
  - UI 구성
- getData.py
  - 저장되어있는 데이터를 불러오거나 씀. API를 활용하여 데이터를 가져오고, 이를 적절히 파싱하여 데이터 생성
- graph.py
  - matplotlib을 활용하여 그래프 생성
- lists.py
  - 프로그램에 필요한 각종 자료구조 저장
- QClasses.py
  - PyQT의 각종 클래스를 override하여 UI를 본 프로그램에 맞게 변형