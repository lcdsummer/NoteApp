import time
import requests


class DataCreate:
    """创建用例前置和后置数据"""
    host = 'http://note-api.wps.cn'

    def note_create(self, num, user_id, sid, group_id=None, remind_time=None):
        """通用的便签新建方法"""
        note_lists_id = []
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(user_id)
        }
        for i in range(num):
            note_id = str(int(time.time() * 1000))
            # 新建便签主体接口
            url_info = self.host + '/v3/notesvr/set/noteinfo'

            if remind_time:  # 日历便签
                body = {
                    "noteId": note_id,
                    'star': 0,
                    "remindTime": remind_time,
                    "remindType": 0
                }

            elif group_id:  # 分组便签
                # 新建分组
                self.group_create(1, user_id, sid)
                # 新建分组便签
                body = {
                    "noteId": note_id,
                    'star': 0,
                    "groupId": group_id
                }

            else:
                body = {
                    "noteId": note_id,
                    'star': 0
                }

            requests.post(url=url_info, headers=headers, json=body)

            url_content = self.host + '/v3/notesvr/set/notecontent'
            body_content = {
                "noteId": note_id,
                "title": 'test',
                "summary": 'test',
                "body": 'test',
                "localContentVersion": 1,
                "BodyType": 0
            }
            requests.post(url=url_content, headers=headers, json=body_content)
            note_lists_id.append(body["noteId"])
        return note_lists_id

    def group_create(self, user_id, sid, group_id=None, num=None):
        """通用的分组新建方法"""
        group_ids = []
        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(user_id)
        }
        # 新建分组接口
        url_group = self.host + '/v3/notesvr/set/notegroup'
        if group_id is None and num is not None:
            for i in range(num):
                group_id = str(int(time.time() * 1000))
                group_ids.append(group_id)
                body = {
                    "groupId": group_id,
                    'groupName': group_id,
                    "order": 0
                }
                requests.post(url=url_group, headers=headers, json=body)
        else:
            body = {
                "groupId": group_id,
                'groupName': group_id,
                "order": 0
            }
            requests.post(url=url_group, headers=headers, json=body)
            group_ids.append(group_id)
        return group_id