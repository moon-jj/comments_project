import pandas as pd
from datetime import datetime
import os


# time 형식을 minute 단위의 float 형식으로 변한

folder_path ='./chat_data_corrected_n'
new_folder_path = './chat_data_corrected_n_t'

for file_name in os.listdir(folder_path):
    
    file_path = os.path.join(folder_path, file_name)

    # 원본 데이터
    df = pd.read_csv(file_path, index_col=0)
    print(df.head())

    # datetime 형식으로 형식 맞추기
    datetime_format = '%Y-%m-%d %H:%M:%S'
    datetime_start = datetime.strptime(df["time"][0], datetime_format)

    
    try:
        df["time_minutes"] =  df["time"].apply(lambda x : datetime.strptime(x, datetime_format) - datetime_start)
        df["time_minutes"] =  df["time_minutes"].apply(lambda x : round(x.seconds /60, 3))
    except:
        pass
    
    new_file_path = os.path.join(new_folder_path , file_name[:-4] + '_t.csv')
    df.to_csv(new_file_path)