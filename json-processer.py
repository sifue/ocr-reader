import json

# ファイルを開く
with open('./OCR_sample_data.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

# 'lines'内の全ての'text'要素を改行しながら結合
text = '\n'.join(line['text'] for result in data['analyzeResult']['readResults'] for line in result['lines'])

# 結果を出力
print(text)
