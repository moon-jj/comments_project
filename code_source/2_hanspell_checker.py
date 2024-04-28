from hanspell import spell_checker
import pandas as pd
import re
import os

# 채팅글의 한글의 맞춤법 검사

folder_path ='./chat_data'
new_folder_path = './chat_data_corrected'


for file_name in os.listdir(folder_path):

    file_path = os.path.join(folder_path, file_name)
    
    # 원본 데이터
    df = pd.read_csv(file_path, index_col=0, names = ['id', 'comment', 'time'])
    print(df.head())

    # NaN 값을 빈 문자열로 대체한다.
    df["comment"] = df["comment"].fillna("")

    # df["comment"]에 각 행에 대해 특수 문자를 제거하고 한글, 영어, 숫자만 남긴다
    regex = r'[^가-힣a-zA-Z0-9\s]'
    df["corrected_comment"] = df["comment"].apply(lambda x: re.sub(regex, '', str(x)))

    try:
        # df["corrected_comment"]에 hanspell의 spell_checker.check()를 적용한다.
        df["corrected_comment"] = df["corrected_comment"].apply(lambda x : spell_checker.check(x)[2])
    except:
        df["corrected_comment"] = ''
    
    
    new_file_path = os.path.join(new_folder_path, file_name[:-4] + "_corrected.csv")
    df.to_csv(new_file_path)
    
    
    
    