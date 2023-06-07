import json
from tqdm import tqdm
import os

json_directory = "output_json"
text_directory = "output_text"

def list_files(directory):
    '''
    ディレクトリ内のファイル一覧を取得する
    Args:
        directory (str): ディレクトリ名
    Returns:
        list: ファイル一覧
    '''
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

json_files = list_files(json_directory)
json_files.sort()
for json_file in tqdm(json_files):
    if os.path.splitext(json_file)[1] != ".json":
        continue

    json_file_fullpath = json_directory + os.sep + json_file
    text_file_fullpath = text_directory + os.sep + os.path.splitext(json_file)[0] + ".txt"

    # print("json_file_fullpath:")
    # print(json_file_fullpath)

    with open(json_file_fullpath, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)

        # 'lines'内の全ての'text'要素を改行しながら結合
        text = '\n'.join(line['text'] for result in data['analyzeResult']['readResults'] for line in result['lines'])
        
        # print(text)
        # print(text_file_fullpath)
        with open(text_file_fullpath, 'w', encoding='utf-8') as f2:
            f2.write(text)
