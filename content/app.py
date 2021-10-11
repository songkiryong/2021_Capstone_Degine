
from flask import Flask, request, render_template
import json
import requests
#import model
import json
import os
import shutil

from bs4 import BeautifulSoup
from flask import Blueprint, request, render_template, flash, redirect, url_for, Flask
from flask import current_app as current_app
#from flask_ngrok import run_with_ngrok
import pill_deeplearning_result as pmodel # 딥러닝 모델 파이썬 파일
from django.shortcuts import render
from urllib.request import urlopen
from django.conf import settings
from django import template

pillDict = {} # 파싱한 알약의 이름과 링크를 key,value 형태로 저장하기 위한 딕셔너리 변수
pillDictBackup = {} # 재설정된 조건으로 파싱한 결과가 없을때를 대비해 그 전 dict값을 넣는 딕셔너리 변수
pillresult = {}

#pillImg = {} pillImgBackup = {}pillresult = {}

app = Flask(__name__, template_folder='static/template')
#app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 300
#run_with_ngrok(app)

#파싱
# againNotagain이 1이면 조건값을 재설정한 후 파싱하는 것으로 pillDict을 초기화해준다
def parser(result, againNotagain):
    #beautifulSoup을 통해 html에서 알약 세부사항이 있는 링크들만 따오는 ide
    dest="https://terms.naver.com/medicineSearch.naver?mode=exteriorSearch&shape="+str(result['sha'])+"&color="+str(result['col'])+"&dosageForm=&divisionLine=&identifier="+str(result['ide'])
    res = requests.get(dest)
    soup = BeautifulSoup(res.text, 'html.parser')

    pill_tags = soup.find_all("div", attrs={"class":"image_area"})
    
    pillLink = '' # 알약 링크 저장
    pillName = '' # 알약 이름 저장

    if(againNotagain == 1): # 재설정된 조건으로 파싱할 경우 pillDict 초기화
      global pillDict
      global pillDictBackup
      pillDictBackup = pillDict # pillDict 백업
      pillDict = {}

    siteNum = 0
    for tag in pill_tags:
      if(siteNum == 7):
        break
      tmp='https://terms.naver.com/' + tag.find("a")["href"] # 파싱할 링크
      
      res = requests.get(tmp)
      soup = BeautifulSoup(res.text, 'html.parser')
      soupImg = soup.find("span",class_="img_box")

      if(soup.strong.string != '다시 한번 확인해주세요!'): # 잘못된 링크 값이 아니면


        imgUrl = soupImg.find("img")["data-src"]
        num = 1
        filename=''
        filestaticname = ''
        while True: # 파일이 없는 걸 발견할 때 까지 무한반복
          filename = '/content/static/pills/pillImg' + str(num) + '.jpg'#'pillImg' + str(num) + '.jpg' # 
          
          if(os.path.isfile(filename) == False):
            filestaticname = 'pills/pillImg' + str(num) + '.jpg'
            break
          num += 1 # 파일 존재시 num 1증가

        with urlopen(imgUrl) as f:
          with open(filename,'wb') as h: # 이미지 + 사진번호 + 확장자는 jpg
            img = f.read() #이미지 읽기
            h.write(img) # 이미지 저장

        # 알약 링크, 이름 저장
        pillLink = 'https://terms.naver.com/' + tag.find("a")["href"]
        pillName = tag.find("img")["alt"]
        #print(filename)
        pillDict[str(num)] = filestaticname
        pillDict[pillName] = pillLink # 딕셔너리에 이름 : 링크 형식으로 저장
        siteNum += 1

    return pillDict # 알약 딕셔너리 리턴

def pill_text_par(link): # 알약의 세부내용을 파싱하는 함수

    cnt = 0
    for i, j in link.items():
      if(cnt==1):
        parsingLink = link[i]
      cnt += 1

    res = requests.get(parsingLink)
    soup = BeautifulSoup(res.text, 'html.parser') # link의 내용을 soup에 저장


    title = soup.find_all("h3", attrs={"class":"stress"}) # 세부사항 큰 제목 파싱
    detailText = soup.find_all("p", attrs={"class":"txt"}) # 세부사항 내용 파싱

    detail=[] # 세부내용 초기화
    detailParsingcnt = 0 # 사용 주의사항 전까지의 글만 읽어오기 위한 count
    for tag1,tag2 in zip(title, detailText): # 세부내용 detail에 저장
        detail.append(tag1.get_text())
        detail.append(tag2.get_text())

        if(detailParsingcnt == 4):
          break
        detailParsingcnt+=1

    return detail # 저장된 세부내용 값 리턴

#메인화면
@app.route('/',methods=['GET','POST'])
def main():
    return render_template('mainsite.html')
      
@app.route('/post',methods=['GET','POST'])
def post():
    global pillDict
    pillDict = {}
    global pillDictBackup
    pillDictBackup = {}
    global pillresult
    pillresult = {}

    f = request.files['pill_file'] 

    testdata_path = '/content/test_data/xx.png'
    f.save(testdata_path) # 사용자에게 받은 파일 filepath 경로에 저장 

    # 알약 사진 정보 mst.txt로
    !python '/content/yolov5/detect.py' --weights '/content/best_s.pt' --img 416 --conf 0.5 --source '/content/test_data/xx.png' > '/content/yolov5/msg.txt'
    
    num = 2 # exp1은 없기에 2부터 시작
    while True: # expnum(num:양수) 폴더가 없는 걸 발견할 때 까지 무한반복
      if(os.path.isdir('/content/runs/detect/exp2') == False): # exp2폴더가 없을 때
        num= -1
        break

      filename = '/content/runs/detect/exp' + str(num+1) # exp(num+1)폴더가 없을 때, exp(num)폴더를 사용
      if(os.path.isdir(filename) == False):
        break
      num += 1 # 폴더 존재시 num 1증가

    if(os.path.isfile('/content/static/test_data/xx.jpg') == True):
      os.remove('/content/static/test_data/xx.jpg')
    elif(os.path.isfile('/content/static/test_data/xx.png') == True):
      os.remove('/content/static/test_data/xx.png')  

    shutil.copyfile(testdata_path, '/content/static/test_data/xx.png')

    tmp = pmodel.detectPill(num) # 사진 색, 모양 추출, num은 detect할 exp폴더 num

    pillresult['sha'] = tmp['sha']
    pillresult['col'] = tmp['col']
    pillresult['ide'] = tmp['ide'] # 다른 함수에서 사용하기 위해 값 각각 선언

    parser_dic = parser(pillresult, 0) # parser함수를 통해 알약의 이름과 링크값이 들어있는 딕셔너리를 받음

    if(len(parser_dic) >= 4): # 파싱 결과 값이 4개(사진포함) 이상일 때
      return render_template('pillsList.html', testDataHtml=parser_dic, imgHtml = 'test_data/xx.png')
    elif(len(parser_dic) == 0): # 파싱 결과가 없을 경우 메인사이트로 이동한단
      return render_template('mainsite.html')

    detailText = pill_text_par(parser_dic)
    return render_template('onePillResult.html', testDataHtml=parser_dic, detailHtml=detailText, imgHtml = 'test_data/xx.png')

@app.route('/result',methods=['GET','POST'])
def result():
    getpillname = request.values.get('pill_name') # 사용자가 입력한 알약 이름 가져옴

    pillresult['ide'] = getpillname # 알약의 ide값 입력받은 값으로 수정

    parser_again_dic = {}
    parser_again_dic = parser(pillresult, 1) # 수정된 조건값으로 다시 파싱

    

    #같은 이름의 알약이 없으면 다시 원래의 사이트를 보여준다.
    if(len(parser_again_dic) < 1):
      return render_template('pillsList.html', testDataHtml = pillDictBackup, imgHtml = 'test_data/xx.png')  
    elif(len(parser_again_dic) >= 4): # 알약 종류 2개 이상 나올시
      return render_template('pillsList.html', testDataHtml = parser_again_dic, imgHtml = 'test_data/xx.png')  
    else: # 한 개의 알약 값만 나올 때
      detailText = pill_text_par(parser_again_dic)
      return render_template('onePillResult.html', testDataHtml = parser_again_dic, detailHtml=detailText, imgHtml = 'test_data/xx.png')  #return render_template('ex.html', testDataHtml = detailText)
@app.route("/toMain", methods=["GET", "POST"])
def toMain():
    global pillDict
    pillDict = {}
    global pillDictBackup
    pillDictBackup = {}
    global pillresult
    pillresult = {}
    return redirect('/')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    app.run(host='0.0.0.0')
