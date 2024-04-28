# comments_project


### 1. 댓글 수집 & 전처리

-   pytchat을  활용하여  댓글  데이터  수집 : 5경기 (댓글 5000개 이상인 경기만)
-   hanspell을  활용하여  한글  맞춤법  및  띄어쓰기  오류  식별, 수정
-   KoNLPy 라이브러리를  통해 Okt 형태소  분석기를  적용하여  명사만  추출 (전체 명사 6484개)
-   출현빈도가 30 이하인  단어들을  제거 & 이벤트를  식별하는  데  도움이  되지  않거나  과적합을  일으킬  수  있는  단어들(비속어나  불용어) --- 불용어 추가 예정
- 한  글자만으로  이루어진  단어들  제거(주로  대명사  등으로  큰  의미를  찾기  어려움)(명사 '골' 제외)
- 분 단위로 데이터를 그룹화
-  전처리된  명사들을  문서-단어  행렬(document-term matrix, DTM)  형태로  정리
- 모든  경기들을  하나의  말뭉치(corpus)로  모은  다음  댓글을 1분  단위로  묶어 1분  동안  작성된  댓글들을  하나의  문서로  간주

### 2. 이벤트 스코어의 작성
- 이벤트 시점은 이벤트가 일어난 시점 + 2분까지 이벤트 시점으로 간주하여 오즈비를 계산하였다

- (1) 분당 댓글 갯수

- (2) 분당 이벤트 스코어(로그 오즈비 활용)
  
   : (1분  단위로  나누어진  구간에서  측정한  각  단어의  출현  빈도) * (로그-오즈비)

- (3) 분당 이벤트 스코어(단어 출현 횟수의 상대 빈도를 이용한 로그 오즈비 활용)
  
   : (1분  단위로  나누어진  구간에서  측정한  각  단어의  출현  빈도를  상대출현빈도로  변환) * (로그-오즈비)

- 아래는 왼쪽부터 순서대로 (1), (2), (3)
  
<img src="https://github.com/moon-jj/comments_project/assets/162339134/ab5cf0fb-dfd1-402c-9954-08112e7d731c" width="250" height="700">
<img src="https://github.com/moon-jj/comments_project/assets/162339134/49dff92f-9260-4a6c-8e0e-f6736b3204ae"  width="250" height="700">
<img src="https://github.com/moon-jj/comments_project/assets/162339134/4bae1ba5-adc7-4183-afb4-1402e4c3b461"  width="250" height="700">

- (1) 보다 (2), (3)이  모두  이벤트에  해당되는  시점들에서  이벤트  스코어의  값이  이벤트  상황이  아닌  시점들보다  상대적으로  크게  나타나  이벤트  상황을  잘  구분할  수  있다

- (3)보다는 (2)가 특이 데이터가 없어 더 나은 결과이다

### 3. 커널회귀모형을 이용한 이벤트 식별
- 예정

---
  
- '5_data_handling_code.ipynb' 가 깃허브에서 안열리는 이슈 -> 다운받아서 다른 프로그램으로 열면 가능합니다
