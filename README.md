# 개요
2021년도 1학기 캡스톤 디자인 프로젝트  

# 팀
- 팀명 : 강약중간약
- 팀원 및 역할  

  - 윤소영 : 알약 탐지 딥러닝 모델 구현, 딥러닝 오픈소스 탐색 및 활용, 프로젝트 총괄, 서류 작성
  - 김한나 : 웹&앱 디자인 작업, 프론트엔드 개발 
  - 함서은 : 서버 구축&관리, 백엔드 개발
  - 송기룡 : 서버 구축&관리, git 관리, 어플 연동
  - 윤수정 : 알약 탐지 딥러닝 모델 구현, 딥러닝 오픈소스 탐색 및 활용, 기능 구현  

# 주제 및 기대효과
- 프로젝트명 : 알약분석앱
  - 알약 사진을 받으면 해당 알약의 상세정보를 알려주는 기능  

- 기대효과
  - 처방전을 잃어버린 약의 정보를 이미지분석을 통해 알아내어 안전하게 약을 복용할 수 있음  

# 기능
- 처방전 없이 약봉지만 있는 약의 상세정보를 알 수 있음  

# 준비사항  
1. gpu 환경  
-> Colab  

2. static/js/putFile.js  
-> IAM USER 정보 기입  

3. S3 버킷 생성 및 권한 설정  
-> 버킷 생성 후 CORS 항목에 아래의 코드 복사     
```
[
  {
    "AllowedHeaders": [
        "*"
    ],
    "AllowedMethods": [
        "PUT",
        "POST",
        "DELETE"
    ],
    "AllowedOrigins": [
        "*"
    ],
    "ExposeHeaders": []
  }
]
```  
# 작동순서  
1. Google Drive에 디렉토리 'content' 복사  
2. Colab - Google Drive Mount  
```
from google.colab import drive
drive.mount('/content/drive')
```
3. pre-installed  
```
!sh requirements.sh  
sudo apt install tesseract-ocr -y 
sudo apt install nginx

```
4. Ngrok 고정 url 받기
  - Ngrok 다운로드  
  -    

5. Nginx 설정

6. 실행  
Colab Note에 app.py 복사 후 실행  





