import urllib.parse
import urllib.request
import base64
import urllib.error
import http.client
import ast
import os
from dotenv import load_dotenv
load_dotenv()

SUBSCRIPTION_KEY = os.getenv("AZURE_SUBSCRIPTION_KEY")
ENDPOINT = os.getenv("AZURE_ENDPOINT")
host = ENDPOINT.split("/")[2]
text_recognition_url = (ENDPOINT + "vision/v3.2/read/analyze")

def call_read_api(host, text_recognition_url, body):
    '''
    ReadAPIを呼び出す

    Args:
        host (str): エンドポイント
        text_recognition_url (str): ReadAPIのURL
        body (str): 画像ファイルのバイナリデータ

    Returns:
        OL_url (str): Operation Location URL
    '''
    try:
        conn = http.client.HTTPSConnection(host)
        params = urllib.parse.urlencode({
            'readingOrder': 'natural',
        })

        conn.request(
            method="POST",
            url=text_recognition_url + "?%s" % params,
            body=body,
            headers={
                "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
                "Content-Type": "application/octet-stream"
            },
        )
        read_response = conn.getresponse()
        # print(read_response.status)

        OL_url = read_response.headers["Operation-Location"]
        conn.close()
        # print("read_request:SUCCESS")

    except Exception as e:
        print("[ErrNo {0}]{1}".format(e.errno, e.strerror))
    return OL_url


def call_get_read_result_api(host, OL_url):
    '''
    Read Result API を呼び出す
    結果がなければ、10秒待って再度呼び出す

    Args:
        host (str): エンドポイント
        OL_url (str): Operation Location URL

    '''
    result_dict = {}
    try:
        conn = http.client.HTTPSConnection(host)

        poll = True
        while (poll):
            if (OL_url == None):
                print("None Operation-Location")
                break

            conn.request(
                method="GET",
                url=OL_url,
                headers={
                    "Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY,
                },
            )
            result_response = conn.getresponse()
            result_str = result_response.read().decode()
            result_dict = ast.literal_eval(result_str)

            if ("analyzeResult" in result_dict):
                poll = False
                print("get_result:SUCCESS")
            elif ("status" in result_dict and
                  result_dict["status"] == "failed"):
                poll = False
                print("get_result:FAILD")
            else:
                time.sleep(10)
        conn.close()

    except Exception as e:
        print("[ErrNo {0}] {1}".format(e.errno, e.strerror))

    return result_dict

if __name__ == "__main__":
    import time
    import json
    import urllib.parse
    import os
    from tqdm import tqdm

    target_directory = "target"
    output_directory = "output_json"

    def list_files(directory):
        '''
        ディレクトリ内のファイル一覧を取得する
        Args:
            directory (str): ディレクトリ名
        Returns:
            list: ファイル一覧
        '''
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

    # output_jsonにOCR結果のJSONファイルが存在していない画像ファイルを取得
    image_files = list_files(target_directory)
    image_base_names = [os.path.splitext(f)[0] for f in image_files]
    extension_dict = {os.path.splitext(f)[0]: os.path.splitext(f)[1] for f in image_files}

    json_files = list_files(output_directory)
    json_base_names = [os.path.splitext(f)[0] for f in json_files]

    target_image_base_names = list(set(image_base_names) - set(json_base_names))
    target_image_file_names = [f"{name}{extension_dict[name]}" for name in target_image_base_names]
    target_image_file_names.sort()

    print("target_image_file_names:")
    print(target_image_file_names)

    for image_file in tqdm(target_image_file_names):
        image_file_fullpath = target_directory + os.sep + image_file

        body = open(image_file_fullpath, "rb").read()
        OL_url = call_read_api(host, text_recognition_url, body)

        # print("OL_url:")
        # print(OL_url)

        # 1回の処理待ち10秒してから、結果を取得する
        time.sleep(10)
        result_dict = call_get_read_result_api(host, OL_url)

        json_file_fullpath =  output_directory + os.sep + os.path.splitext(image_file)[0] + ".json"
        with open(json_file_fullpath, "w", encoding="utf_8_sig") as f:
            json.dump(result_dict, f, indent=3, ensure_ascii=False)
