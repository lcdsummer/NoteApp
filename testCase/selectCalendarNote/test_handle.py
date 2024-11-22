import unittest
from common.generalAssert import GeneralAssert
from common.caseMsgLogs import class_case_decoration
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from business.businessRe import BusinessRe
from common.yamlRead import YamlRead
import time
import json


@class_case_decoration
class SelectCalendarNoteHandle(unittest.TestCase):
    ga = GeneralAssert()
    dataclean = DataClear()
    datacreate = DataCreate()
    re = BusinessRe()
    apiConfig = YamlRead().api_config()['select_calendar_note']
    envConfig = YamlRead().env_config()
    user_id1 = envConfig['user_id1']
    sid1 = envConfig['sid1']
    user_id2 = envConfig['user_id2']
    sid2 = envConfig['sid2']
    host = envConfig['host']
    url = host + apiConfig['path']
    mustKeys = apiConfig['mustKeys']

    def setUp(self) -> None:
        """重置数据"""
        self.dataclean.del_notes(self.user_id1, self.sid1)

    def testCase24_handle_value_limit(self):
        """查看日历便签接口，handle：数值限制--startindex为0"""
        # 前置条件：用户"user_id1"下新建2条日历便签
        remind_time = time.time()
        res_noteid = self.datacreate.note_create(2, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)

        expect = {
            "responseTime": int,
            "webNotes": [
                {
                    "noteId": res_noteid[0],
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
                    "noteId": res_noteid[1],
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

    def testCase25_handle_value_limit(self):
        """查看日历便签接口，handle：数值限制--startindex为1"""
        # 前置条件：用户"user_id1"下新建2条日历便签
        remind_time = time.time()
        res_noteid = self.datacreate.note_create(2, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 1,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)

        expect = {
            "responseTime": int,
            "webNotes": [
                {
                    "noteId": res_noteid[0],
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

    def testCase26_handle_value_limit(self):
        """查看日历便签接口，handle：数值限制--startindex为5"""
        # 前置条件：用户"user_id1"下新建2条日历便签
        remind_time = time.time()
        self.datacreate.note_create(2, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 5,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        expect = {
            "responseTime": int,
            "webNotes": []
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())

    def testCase27_handle_value_limit(self):
        """查看日历便签接口，handle：数值限制--rows为1"""
        # 前置条件：用户"user_id1"下新建2条日历便签
        remind_time = time.time()
        res_noteid = self.datacreate.note_create(2, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 1
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        expect = {
            "responseTime": int,
            "webNotes": [
                {
                    "noteId": res_noteid[0],
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

    def testCase28_handle_value_limit(self):
        """查看日历便签接口，handle：数值限制--rows为3"""
        # 前置条件：用户"user_id1"下新建2条日历便签
        remind_time = time.time()
        res_noteid = self.datacreate.note_create(2, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 0,
            "rows": 3
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        expect = {
            "responseTime": int,
            "webNotes": [
                {
                    "noteId": res_noteid[0],
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
                    "noteId": res_noteid[1],
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

    def testCase29_handle_value_limit(self):
        """查看日历便签接口，handle：数值限制--remindStartTime > remindEndTime"""
        # 前置条件：用户"user_id1"下新建1条日历便签
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：用户"user_id1"下查看该日历便签
        body = {
            "remindStartTime": 4102452000000,
            "remindEndTime": remind_time,
            "startIndex": 0,
            "rows": 3
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(412, res.status_code, msg='状态码校验失败')

    def testCase30_handle_ultraVires(self):
        """获取首页便签列表接口，越权：用户A查看用户B的日历便签"""
        # 前置条件：用户B下有一条便签数据
        remind_time = time.time()
        self.datacreate.note_create(1, self.user_id2, self.sid2, remind_time=remind_time)
        # 用户A获取用户B的首页便签列表
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 5,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id2, body)
        self.assertEqual(412, res.status_code, msg='状态码校验失败')

    def testCase31_handle_different_handleCount(self):
        """获取首页便签列表接口，不同处理数量：用户"user_id1"无便签数据"""
        remind_time = time.time()
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 5,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        expect = {
            "responseTime": int,
            "webNotes": []
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())

    def testCase32_handle_state_limit(self):
        """获取首页便签列表接口，状态限制：查询被删除的日历便签"""
        # 前置条件：用户"user_id1"下有1条被删除的日历便签
        remind_time = time.time()
        res_noteid = self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        self.dataclean.soft_del_notes(user_id=self.user_id1, sid=self.sid1, node_id=res_noteid[0])
        # 测试步骤：用户"user_id1"下查看该被删除的日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 5,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        expect = {
            "responseTime": int,
            "webNotes": []
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())

    def testCase33_handle_state_limit(self):
        """获取首页便签列表接口，状态限制：查询被回收站清空的日历便签"""
        # 前置条件：用户"user_id1"下有1条被回收站清空的日历便签
        remind_time = time.time()
        res_noteid = self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        self.dataclean.soft_del_notes(user_id=self.user_id1, sid=self.sid1, node_id=res_noteid[0])
        self.dataclean.del_recycel(user_id=self.user_id1, sid=self.sid1)
        # 测试步骤：用户"user_id1"下查看该被回收站清空的日历便签
        body = {
            "remindStartTime": remind_time,
            "remindEndTime": 4102452000000,
            "startIndex": 5,
            "rows": 10
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        expect = {
            "responseTime": int,
            "webNotes": []
        }
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.ga.http_assert(expect, res.json())