import unittest
from common.generalAssert import GeneralAssert
from common.caseMsgLogs import class_case_decoration
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from business.businessRe import BusinessRe
from common.yamlRead import YamlRead
import time


@class_case_decoration
class GetNoteListHandle(unittest.TestCase):
    ga = GeneralAssert()
    dataclean = DataClear()
    datacreate = DataCreate()
    re = BusinessRe()
    apiConfig = YamlRead().api_config()['get_note_list']
    envConfig = YamlRead().env_config()
    user_id1 = envConfig['user_id1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    mustKeys = apiConfig['mustKeys']
    user_id2 = envConfig['user_id2']
    sid2 = envConfig['sid2']

    def setUp(self) -> None:
        """重置数据"""
        self.dataclean.del_notes(self.user_id1, self.sid1)
        self.dataclean.del_notes(self.user_id2, self.sid2)

    def testCase26_handle_valueLimit_startIndex(self):
        """获取首页便签列表接口，数值限制：startindex传入0"""
        # 前置条件：用户"user_id1"下新建2条便签主体
        note_lists_id = self.datacreate.note_create(2, self.user_id1, self.sid1)
        # 获取user_id1的首页便签列表
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)

        expect = {
            "responseTime": int,
            "webNotes": [
                {
                    "noteId": note_lists_id[1],
                    "createTime": int,
                    "star": 0,
                    "remindTime": int,
                    "remindType": int,
                    "infoVersion": int,
                    "infoUpdateTime": int,
                    "groupId": None,
                    "title": "test",
                    "summary": "test",
                    "thumbnail": None,
                    "contentVersion": int,
                    "contentUpdateTime": int
                },
                {
                    "noteId": note_lists_id[0],
                    "createTime": int,
                    "star": 0,
                    "remindTime": int,
                    "remindType": int,
                    "infoVersion": int,
                    "infoUpdateTime": int,
                    "groupId": None,
                    "title": "test",
                    "summary": "test",
                    "thumbnail": None,
                    "contentVersion": int,
                    "contentUpdateTime": int
                }
            ]
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())

    def testCase27_handle_valueLimit_startIndex(self):
        """获取首页便签列表接口，数值限制：startindex传入小于便签总数的数--1"""
        # 前置条件：用户"user_id1"下新建2条便签主体
        note_lists_id = self.datacreate.note_create(2, self.user_id1, self.sid1)
        # startindex传入1获取user_id1的首页便签列表
        startindex = 1
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        expect = {
            "responseTime": int,
            "webNotes": [
                {
                    "noteId": note_lists_id[0],
                    "createTime": int,
                    "star": 0,
                    "remindTime": int,
                    "remindType": int,
                    "infoVersion": int,
                    "infoUpdateTime": int,
                    "groupId": None,
                    "title": "test",
                    "summary": "test",
                    "thumbnail": None,
                    "contentVersion": int,
                    "contentUpdateTime": int
                }
            ]
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())

    def testCase28_handle_valueLimit_startIndex(self):
        """获取首页便签列表接口，数值限制：startindex传入大于或等于便签总数的数--3"""
        # 前置条件：用户"user_id1"下有2条便签主体
        self.datacreate.note_create(2, self.user_id1, self.sid1)
        # startindex传入3获取user_id1的首页便签列表
        startindex = 3
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        expect = {
            "responseTime": int,
            "webNotes": []
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())

    def testCase29_handle_valueLimit_rows(self):
        """获取首页便签列表接口，数值限制：row传入1"""
        # 前置条件：用户"user_id1"下有2条便签主体
        note_lists_id = self.datacreate.note_create(2, self.user_id1, self.sid1)
        # row传入1获取user_id1的首页便签列表
        startindex = 0
        rows = 1
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        expect = {
            "responseTime": int,
            "webNotes": [
                {
                    "noteId": note_lists_id[1],
                    "createTime": int,
                    "star": 0,
                    "remindTime": int,
                    "remindType": int,
                    "infoVersion": int,
                    "infoUpdateTime": int,
                    "groupId": None,
                    "title": "test",
                    "summary": "test",
                    "thumbnail": None,
                    "contentVersion": int,
                    "contentUpdateTime": int
                }
            ]
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())

    def testCase30_handle_valueLimit_rows(self):
        """获取首页便签列表接口，数值限制：row传入3"""
        # 前置条件：用户"user_id1"下有2条便签主体
        note_lists_id = self.datacreate.note_create(2, self.user_id1, self.sid1)
        # row传入3获取user_id1的首页便签列表
        startindex = 0
        rows = 3
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        expect = {
            "responseTime": int,
            "webNotes": [
                {
                    "noteId": note_lists_id[1],
                    "createTime": int,
                    "star": 0,
                    "remindTime": int,
                    "remindType": int,
                    "infoVersion": int,
                    "infoUpdateTime": int,
                    "groupId": None,
                    "title": "test",
                    "summary": "test",
                    "thumbnail": None,
                    "contentVersion": int,
                    "contentUpdateTime": int
                },
                {
                    "noteId": note_lists_id[0],
                    "createTime": int,
                    "star": 0,
                    "remindTime": int,
                    "remindType": int,
                    "infoVersion": int,
                    "infoUpdateTime": int,
                    "groupId": None,
                    "title": "test",
                    "summary": "test",
                    "thumbnail": None,
                    "contentVersion": int,
                    "contentUpdateTime": int
                }
            ]
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())

    def testCase31_handle_ultraVires(self):
        """获取首页便签列表接口，越权：用户A获取用户B的首页便签列表"""
        # 前置条件：用户B下有一条便签数据
        self.datacreate.note_create(1, self.user_id2, self.sid2)
        # 用户A获取用户B的首页便签列表
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id2}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(412, res.status_code, msg='状态码校验失败')

    def testCase32_handle_stateLimit_fz(self):
        """获取首页便签列表接口，状态限制：查询分组便签"""
        # 前置条件：用户A下有一条分组便签数据，无首页便签数据
        group_id = str(int(time.time() * 1000))
        self.datacreate.note_create(1, self.user_id1, self.sid1, group_id=group_id)
        # 获取user_id1的首页便签列表
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        expect = {
            "responseTime": int,
            "webNotes": []
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())

    def testCase33_handle_stateLimit_rl(self):
        """获取首页便签列表接口，状态限制：查询日历便签"""
        # 前置条件：用户A下有一条日历便签数据，无首页便签数据
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 获取user_id1的首页便签列表
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        expect = {
            "responseTime": int,
            "webNotes": []
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())

    def testCase34_handle_stateLimit_bsc(self):
        """获取首页便签列表接口，状态限制：查询被删除便签"""
        # 前置条件：用户A下有一条被删除的便签数据，无首页便签数据
        note_lists_id = self.datacreate.note_create(1, self.user_id1, self.sid1)
        self.dataclean.soft_del_notes(user_id=self.user_id1, sid=self.sid1, node_id=note_lists_id[0])
        # 获取user_id1的首页便签列表
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        expect = {
            "responseTime": int,
            "webNotes": []
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())

    def testCase35_handle_stateLimit_bqk(self):
        """获取首页便签列表接口，状态限制：查询被回收站清空的便签"""
        # 前置条件：用户A下有一条被回收站清空的便签数据，无首页便签数据
        self.datacreate.note_create(1, self.user_id1, self.sid1)
        self.dataclean.del_notes(self.user_id1, self.sid1)
        # 获取user_id1的首页便签列表
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{str(self.user_id1)}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        expect = {
            "responseTime": int,
            "webNotes": []
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())

    def testCase36_handle_rows_0(self):
        """获取首页便签列表接口，不同处理数量：用户A无首页便签数据"""
        # 获取user_id1的首页便签列表
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{str(self.user_id1)}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        expect = {
            "responseTime": int,
            "webNotes": []
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())
