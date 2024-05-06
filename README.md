# comments_project




### 1. 댓글 수집 & 전처리

#### 1.1 데이터 수집
pytchat을  활용하여  댓글  데이터  수집 : 5경기 (댓글 5000개 이상인 경기만)
| 날짜         | 경기                        | url                                                                                        |
| ---------- | ------------------------- | ------------------------------------------------------------------------------------------ |
| 2023_02_06 | Tottenham vs Manchester   | [https://www.youtube.com/watch?v=fkD8hXicH_o](https://www.youtube.com/watch?v=fkD8hXicH_o) |
| 2023_02_20 | Tottenham vs WestHam      | [https://www.youtube.com/watch?v=198wHOO9StY](https://www.youtube.com/watch?v=198wHOO9StY) |
| 2023_03_19 | Tottenham vs Southhampton | [https://www.youtube.com/watch?v=Dl67bLYk3bE](https://www.youtube.com/watch?v=Dl67bLYk3bE) |
| 2023_03_24 | Korea vs Colombia         | [https://www.youtube.com/watch?v=9zbwFa6pAjM](https://www.youtube.com/watch?v=9zbwFa6pAjM) |
| 2023_04_04 | Everton vs Tottenham      | [https://www.youtube.com/watch?v=9sq0tli0RbY](https://www.youtube.com/watch?v=9sq0tli0RbY) |

#### 1.2 데이터 전처리
-   hanspell을  활용하여  한글  맞춤법  및  띄어쓰기  오류  식별, 수정
-   KoNLPy 라이브러리를  통해 Okt 형태소  분석기를  적용하여  명사만  추출 (전체 명사 6484개)
-   출현빈도가 30 이하인  단어들을  제거 & 이벤트를  식별하는  데  도움이  되지  않거나  과적합을  일으킬  수  있는  단어들(비속어나  불용어) --- 불용어 추가 예정
- 한  글자만으로  이루어진  단어들  제거(주로  대명사  등으로  큰  의미를  찾기  어려움)(명사 '골' 제외)
- 분 단위로 데이터를 그룹화
-  전처리된  명사들을  문서-단어  행렬(document-term matrix, DTM)  형태로  정리
- 모든  경기들을  하나의  말뭉치(corpus)로  모은  다음  댓글을 1분  단위로  묶어 1분  동안  작성된  댓글들을  하나의  문서로  간주

### 2. 이벤트 스코어의 작성
- 이벤트 시점은 이벤트가 일어난 시점 + 2분까지 이벤트 시점으로 간주하여 오즈비를 계산하였다
- data 별 : (1)comment_cnt, (2)frequnecy, (3)relative frequency

- (1) comment_cnt
  
	: 분당 댓글 갯수

- (2) frequnecy
  
	: 분당 이벤트 스코어(로그 오즈비 활용) = (1분  단위로  나누어진  구간에서  측정한  각  단어의  출현  빈도) * (로그-오즈비)

- (3) relative frequency
  
	: 분당 이벤트 스코어(단어 출현 횟수의 상대 빈도를 이용한 로그 오즈비 활용) = (1분  단위로  나누어진  구간에서  측정한  각  단어의  출현  빈도를  상대출현빈도로  변환) * (로그-오즈비)


 <img src = "https://github.com/moon-jj/temp2/assets/162339134/eb7f05b2-bbeb-4cbc-b8f6-c6fa53649b29" width="750" height="900">



- (1) 보다 (2), (3)이  모두  이벤트에  해당되는  시점들에서  이벤트  스코어의  값이  이벤트  상황이  아닌  시점들보다  상대적으로  크게  나타나  이벤트  상황을  잘  구분할  수  있다


### 3. 커널회귀모형을 이용한 이벤트 식별

-  i+1, i+2 시점에  해당되는  이벤트  스코어를  제거한  데이터에  커널 회귀/상수 모형을  적용한  후 i시점의  이벤트  스코어를  보간법으로  예측하여  제거된  잔차r(i)를  구하는 방식
	(댓글의  특성상  이벤트  시점 1~2분  후까지도  이벤트  스코어가  높게  나타날  수  있기  때문)
- 잔차의  크기가 3사분위수 Q3와 k*IQR의  합 Q3 + k IQR 이상인  관측값을  이상점, 즉  이벤트  시점의  후보로  선정


#### 3.1 결과


##### fitted model
- data 별 : comment_cnt, frequnecy, relative frequency 
- 모델 별 : 국소선형/상수 모델 
  
<img src = "https://github.com/moon-jj/temp2/assets/162339134/b1ac7e77-29f3-42bd-98f6-31eefc336251" width="750" height="900">

#### Prediction results

- window k : +- k interval 내 이벤트 상황 예측
- data별 : comment_cnt, frequnecy, relative frequency
- 모델 별 : 국소선형/상수 모델

  
<img src = "https://github.com/moon-jj/temp2/assets/162339134/09e6c5a2-8fd8-477b-b86a-789f21d8467c" width="750" height="900">


- 이벤트가 발생한 시점에 비해 이벤트가 발생하지 않은 시점이 월등히 많으므로 정확도와 특이도는 높은 반면, 민감도와 정밀도가 낮음
- r(i) >= Q3 + k*IQR 에서  k 값이 커지면 이상점, 즉 양성으로 식별되는 점들이 적어지므로 진양성 예측값과 함께 위양성 예측값도 적어짐
	특히 위양성 예측값이 더 큰 폭으로 적어지므로 k값이 커짐에 따라 민감도는 낮아지고, 정밀도는 높아지는 상반되는 경향
	두 지표의 조화평균에 해당되는 F1 은 조금씩 커지는 경향 ( k=1, 1.5까지 증가하다가 2 되면 다시 작아짐)

- <상대빈도/절대빈도>
  
  window =1,2 일때는 절대빈도가 많은 차이로, window=0 일때는 상대빈도가 아주 적은 차이로 더 좋은 성능
  
- <국소상수/국소회귀모형>
  
   오즈비를 가중치로 작성한 이벤트 스코어에서는 국소상수모형이
  
  단순한 댓글의 빈도를 사용했을 때는 국소선형모형이 더 좋은 성능

--- 

#### 기존논문과 다른 점 

- <단순한 댓글 빈도/오즈비를 가중치로 작성한 이벤트 스코어>
  
	단순한 댓글 빈도 보다 오즈비를 가중치로 작성한 이벤트 스코어가 모든 지표에서 더 좋은것으로 나타남
 
	(단순 댓글의 빈도를 사용했을 때는 특히 위양성 및 위음성 값들이 많아 정밀도와 민감도 값이 크게 낮아지기 때문)

- <상대빈도/절대빈도>
  
  대부분의 지표에서 상대빈도를 기반으로 한 이벤트 스코어를 사용했을 때의 예측결과가 좋게 나옴
  
  다만 k 값이 클 때의 민감도 등 일부 경우에는 상대빈도보다 절대빈도를 사용하는 것이 더 좋은 결과

- <국소상수/국소회귀모형>
  
  큰 차이는 없지만 상대도수를 이용했을 때 - 국소상수 모형 / 절대도수를 이용했을 때 - 국소선형 모형이 더 좋은 결과
  
---
  
- '5_data_handling_code.ipynb' 가 깃허브에서 안열리는 이슈 -> 다운받아서 다른 프로그램으로 열면 가능합니다









