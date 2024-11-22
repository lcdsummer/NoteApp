import json
import requests


class DataClear:
    """创建用例前置和后置数据"""
    host = 'http://note-api.wps.cn'
    note_ids = []
    group_ids = []

    def del_notes(self, user_id, sid):
        """重置数据：清空便签数据"""
        headers = {
            'Cookie': f'wps_sid={sid}',
            'X-user-key': str(user_id),
            'Content-Type': 'application/json'
        }
        # 获取首页便签的noteId
        self.select_list_notes(user_id, headers=headers)
        # 获取日历便签的noteId
        self.select_rl_notes(headers=headers)
        # 获取分组Id
        self.select_fz(headers=headers)
        # 获取分组便签的noteId
        self.select_fz_notes(headers=headers)
        # 删除便签
        self.soft_del_notes(headers=headers)
        # 删除分组
        self.del_group(headers=headers)
        # 清空回收站
        self.del_recycel(headers=headers)

    def select_list_notes(self, user_id, headers=None, sid=None):
        # 获取首页便签的noteId
        if headers is None:
            headers = {
                'Cookie': f'wps_sid={sid}',
                'X-user-key': str(user_id),
                'Content-Type': 'application/json'
            }
        url_getlist = self.host + f'/v3/notesvr/user/{str(user_id)}/home/startindex/0/rows/10000/notes'
        res = requests.get(url_getlist, headers=headers)
        res = json.loads(res.text)['webNotes']
        noteIds = []
        for index in res:
            self.note_ids.append(index['noteId'])
            noteIds.append(index['noteId'])
        return noteIds


    def select_rl_notes(self, headers=None, user_id=None, sid=None):
        # 获取日历便签的noteId
        if headers is None:
            headers = {
                'Cookie': f'wps_sid={sid}',
                'X-user-key': str(user_id),
                'Content-Type': 'application/json'
            }
        url_getdatenode = self.host + '/v3/notesvr/web/getnotes/remind'
        body = {
            "remindStartTime": 946692000,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 10000
        }
        res = requests.post(url_getdatenode, headers=headers, json=body)
        res = json.loads(res.text)['webNotes']
        noteIds = []
        for index in res:
            self.note_ids.append(index['noteId'])
            noteIds.append(index['noteId'])
        return noteIds

    def select_fz(self, headers=None, user_id=None, sid=None):
        # 获取分组Id
        if headers is None:
            headers = {
                'Cookie': f'wps_sid={sid}',
                'X-user-key': str(user_id),
                'Content-Type': 'application/json'
            }
        url_getgroups = self.host + '/v3/notesvr/get/notegroup'
        body = {
            "excludeInValid": True
        }
        res = requests.post(url_getgroups, headers=headers, json=body)
        res = json.loads(res.text)['noteGroups']
        groupIds = []
        for index in res:
            self.group_ids.append(index['groupId'])
            groupIds.append(index['groupId'])
        return groupIds

    def select_fz_notes(self, headers=None, user_id=None, sid=None, group_id=None):
        # 获取分组便签
        if headers is None:
            headers = {
                'Cookie': f'wps_sid={sid}',
                'X-user-key': str(user_id),
                'Content-Type': 'application/json'
            }
            url_getgroupnote = self.host + '/v3/notesvr/web/getnotes/group'
            body = {
                "groupId": group_id,
                "startIndex": 0,
                "rows": 10000
            }
            res = requests.post(url_getgroupnote, headers=headers, json=body)
            res = json.loads(res.text)['webNotes']
            noteIds = []
            for i in res:
                noteIds.append(i['noteId'])
            return noteIds
        else:
            for groupId in self.group_ids:
                url_getgroupnote = self.host + '/v3/notesvr/web/getnotes/group'
                body = {
                    "groupId": groupId,
                    "startIndex": 0,
                    "rows": 10000
                }
                res = requests.post(url_getgroupnote, headers=headers, json=body)
                res = json.loads(res.text)['webNotes']
                for i in res:
                    self.note_ids.append(i['noteId'])

    def soft_del_notes(self, headers=None, user_id=None, sid=None, node_id=None):
        # 删除便签
        if headers is None:
            headers = {
                'Cookie': f'wps_sid={sid}',
                'X-user-key': str(user_id),
                'Content-Type': 'application/json'
            }
            url_delnote = self.host + '/v3/notesvr/delete'
            body = {'noteId': node_id}
            requests.post(url_delnote, headers=headers, json=body)
        else:
            url_delnote = self.host + '/v3/notesvr/delete'
            for noteId in self.note_ids:
                body = {'noteId': noteId}
                requests.post(url_delnote, headers=headers, json=body)

    def del_group(self, headers=None, user_id=None, sid=None):
        # 删除分组
        if headers is None:
            headers = {
                'Cookie': f'wps_sid={sid}',
                'X-user-key': str(user_id),
                'Content-Type': 'application/json'
            }
        url_delgroup = self.host + '/notesvr/delete/notegroup'
        for groupId in self.group_ids:
            body = {'groupId': groupId}
            requests.post(url_delgroup, headers=headers, json=body)

    def del_recycel(self, headers=None, user_id=None, sid=None):
        # 清空回收站
        if headers is None:
            headers = {
                'Cookie': f'wps_sid={sid}',
                'X-user-key': str(user_id),
                'Content-Type': 'application/json'
            }
        url_delrecycle = self.host + '/v3/notesvr/cleanrecyclebin'
        body = {'noteIds': [-1]}
        requests.post(url_delrecycle, headers=headers, json=body)
