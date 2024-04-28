from konlpy.tag import Okt
import pandas as pd
import os

# 채팅글에서 okt를 활용하여 nouns 뽑아내기
okt = Okt()


folder_path ='./chat_data_corrected'
new_folder_path = './chat_data_corrected_n'

for file_name in os.listdir(folder_path):
    
    file_path = os.path.join(folder_path, file_name)

    # 원본 데이터
    df = pd.read_csv(file_path, index_col=0)
    print(df.head())
    
    # 결측값을 빈 문자열로 대체
    df["corrected_comment"] = df["corrected_comment"].fillna('')

    # 모든 요소를 문자열로 변환
    df["corrected_comment"] = df["corrected_comment"].astype(str)

    try:
        df["nouns"] = df["corrected_comment"].apply(lambda x : okt.nouns(x))
    except:
        df["nouns"] = ''
    
    new_file_path = os.path.join(new_folder_path , file_name[:-4] + '_n.csv')
    df.to_csv(new_file_path)


