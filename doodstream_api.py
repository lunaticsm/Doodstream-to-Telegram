# doodstream_api.py

import requests

class DoodStream:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://doodapi.com/api/"

    def _make_request(self, endpoint, params=None):
        headers = {"apikey": self.api_key}
        response = requests.get(self.base_url + endpoint, params=params, headers=headers)
        return response.json()

    def account_info(self):
        return self._make_request("account/info")

    def account_reports(self):
        return self._make_request("account/reports")

    def local_upload(self, file_path):
        endpoint = "upload"
        headers = {"apikey": self.api_key}
        files = {"file": open(file_path, "rb")}
        response = requests.post(self.base_url + endpoint, headers=headers, files=files)
        return response.json()

    def remote_upload(self, direct_link):
        endpoint = "remote"
        data = {"url": direct_link}
        headers = {"apikey": self.api_key}
        response = requests.post(self.base_url + endpoint, headers=headers, data=data)
        return response.json()

    def file_info(self, file_id):
        endpoint = f"file/{file_id}"
        return self._make_request(endpoint)

    def search_videos(self, keyword):
        endpoint = f"search/{keyword}"
        return self._make_request(endpoint)

    def rename_file(self, file_id, new_title):
        endpoint = f"file/rename/{file_id}"
        data = {"title": new_title}
        headers = {"apikey": self.api_key}
        response = requests.post(self.base_url + endpoint, headers=headers, data=data)
        return response.json()

    def copy_video(self, file_id):
        endpoint = f"file/copy/{file_id}"
        headers = {"apikey": self.api_key}
        response = requests.post(self.base_url + endpoint, headers=headers)
        return response.json()
