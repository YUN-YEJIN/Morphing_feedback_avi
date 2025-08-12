<Morphing 파일 구성>
aeiou, bcdfg -원본 이미지 / image -보정된 이미지
output -코드 실행 후 영상 파일 저장되는 곳
results -각 음소별 특징점 추출(JSON)
morphing.py는 데이터 분석 및 규칙 생성 코드
pipeline.py는 모핑 프레임,영상 만드는 코드


1. 아래 코드 사용해서 라이브러리 설치
 pip install numpy
 pip install opencv-contrib-python

2. 필요한 데이터셋: 총 3가지
 image(모든 음소 이미지 파일)
 results(모든 랜드마크 JSON 파일)
 phoneme_mapping.json 

3. 코드 실행시 터미널에 명령어 입력 형식
    python pipeline.py sequence --phonemes ㅏ_혀,ㄴ_혀,ㅕ_혀,ㅇ_혀 --frames 8 --diphthong-frames 8 --liaison-frames 25 --fps 10
   :프레임 수랑 fps(=frames per second)

4. pipeline.py 16줄에 BASE_DIR = r"C:\Morphing" 이 경로랑
   morphing.py 11줄, 447줄에 있는 경로 또한 Morphing 파일 있는 경로로 수정해주세요.

5. 예시
   "화이팅"
   python pipeline.py sequence --phonemes ㅜ_입,ㅏ_입,ㅌ_입,ㅣ_입,ㅇ_입 --frames 18 --diphthong-frames 12 --liaison-frames 20 --fps 12

   "고구마"
   python pipeline.py sequence --phonemes ㄱ_혀,ㅗ_혀,ㄱ_혀,ㅜ_혀,ㅁ_혀,ㅏ_혀 --frames 12 --diphthong-frames 8 --liaison-frames 18 --fps 15

   "수고했어"
   python pipeline.py sequence --phonemes ㅅ_혀,ㅜ_혀,ㄱ_혀,ㅗ_혀,ㅎ_혀,ㅐ_혀,ㅆ_혀,ㅇ_혀,ㅓ_혀 --frames 12 --diphthong-frames 8 --liaison-frames 15 --fps 15