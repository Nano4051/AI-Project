# AI-Project
보행영상 AI 분석

프로젝트 계획서  https://1drv.ms/w/c/10027babd671489a/EUX_xULf6vRFk7gPV1klSR0BidyiKm2BZkrne1cGfr3Jvw?e=Xuc9rY  
프로젝트 일지    https://1drv.ms/w/c/10027babd671489a/EZOgVS-THPZAqIhBbrGpLBgB8sAyjKNURlcMhFobtPwegw?e=wHcLq4  
WBS             https://1drv.ms/x/c/10027babd671489a/Edcso3DSHfZMiXSZbzc9ZzwB7PF1eTDFKOeJoVJyIX9GWQ?e=TEsbdX  
PPT             https://1drv.ms/p/c/10027babd671489a/Ech8dtK3iTxOtZouzubr_tABC-OaMHIOIUOncu_30n3Rtw?e=paaF4L  

#개발 환경 구축(vscode,anaconda3(AI),Qdrant(DB),react(Front),Python(Back))  
Anaconda 3 설치 설치옵션 Register Anaconda as default Python 아나콘다 네비게이터 에서 vscode 런치
VSCode에서 Ctrl + Shift + P → “Python: Select Interpreter” 검색 후 Python 3.13.5(base)이런식으로 검색창 아래 뜨면 conda환경 감지성공 (만약에 다르면 GPT 서치해보기)  
vscode 실행후 Ctrl + `로 터미널 창을 띄운 후 conda --version입력 해서 버전 뜨면 정상인식 안뜨면 GPT 서치  
conda create -n walkvideo python=3.10 입력(walkvideo가 가상환경이름)   
필수 패키지 리스트랑 y/n뜨면 y입력후 done이 출력되면 conda activate walkvideo 입력 성공하면 (walkvideo 표시됨)  
앞에 설정과정이 안될시에는 Path 경로에 몇가지 추가를 해야됨  
C:\Users\nano4\anaconda3  
C:\Users\nano4\anaconda3\Scripts  
C:\Users\nano4\anaconda3\Library\bin  
환경변수에 추가가 되었으면 PowerShell을 켜서 conda init powershell 실행후 창 닫기  
만약에 파워셸에서 보안 관련 오류메시지 출력될때  
1️⃣ PowerShell을 관리자 권한으로 실행  
시작 메뉴 → “PowerShell” 검색 →  
오른쪽 클릭 → “관리자 권한으로 실행”  
  
2️⃣ 아래 명령어 입력  
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser 입력후 질문뜨면 y 입력  
이후 conda activate walkvideo 입력후 (walkvideo) PS C:\Users\nano4> 이런식으로 출력되면 설정완료  
pip install fastapi uvicorn qdrant-client numpy opencv-python scikit-learn  
