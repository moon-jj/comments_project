import pytchat #실시간 댓글 크롤링 
# import pafy #유튜브 정보 
import pandas as pd
import asyncio
import os
from datetime import datetime
# from datetime import timedelta

# pytchat 라이브러리 이용하여 유튜브 라이브 방송 댓글 크롤링하기

# api_key = 'AIzaSyB0p8nVvVvchtOiM-MztbPKzyXsMPvrpg0' #gcp youtube data api 에서 api key 생성 \
# pafy.set_api_key(api_key) 
# url = 'https://www.youtube.com/watch?v=9sq0tli0RbY'
# video = pafy.new(url) 
# upload_time = video.published

folder_path ='./chat_data'

# video_id_list = []

# file_name_list = []
video_id_list = ['9sq0tli0RbY', 'sdZPUkhr7z0', '9zbwFa6pAjM',
                 'Dl67bLYk3bE', 'oVMFJ9tvpi8', '198wHOO9StY',
                 'fkD8hXicH_o', 'QQOgqgDhcUU']

file_name_list = ["chat_data_2023_04_04_Everton_Tottenhan.csv", "chat_data_2023_03_28_Korea_Uruguay.csv", "chat_data_2023_03_24_Korea_Colombia.csv",
                  "chat_data_2023_03_19_Tottenham_Southhampton.csv", "chat_data_2023_03_02_Sheffield_Tottenham.csv", "chat_data_2023_02_20_Tottenham_WestHam.csv",
                  "chat_data_2023_02_06_Tottenham_Manchester.csv", "chat_data_2023_01_30_Napoli_Roma.csv"]


async def main(video_id, file_path):
    # YouTube 비디오 ID를 지정하여 pytchat을 초기화
    chat = pytchat.create(video_id=video_id)
    
    # 채팅 데이터를 저장할 빈 리스트를 만듭니다.
    chat_data = []
    
    # 비동기 반복문을 사용하여 채팅 데이터를 가져옵니다.
    while chat.is_alive():
        # 비동기 이벤트를 기다립니다.
        data = chat.get()
        if data:
            # 채팅 데이터가 있으면 딕셔너리로 변환하여 리스트에 추가합니다.
            for c in data.items:

                chat_data.append({
                    "id": c.author.name,
                    "comment": c.message,
                    "time":c.datetime,
                })
    
    # 채팅 데이터를 데이터 프레임으로 변환합니다.
    df = pd.DataFrame(chat_data)
      
    # 데이터 프레임을 CSV 파일로 저장합니다.
    df.to_csv(file_path, mode='w', header=False)
    print(file_path, ' save!!')

# 비동기 함수 실행
async def run_async(video_id, file_name):
    await main(video_id, file_name)

# 비디오 ID, 파일 이름 및 시작 시간을 순서대로 짝지어서 반복문 실행
for video_id, file_name in zip(video_id_list, file_name_list):
    file_path = os.path.join(folder_path, file_name)
    asyncio.run(run_async(video_id, file_name))