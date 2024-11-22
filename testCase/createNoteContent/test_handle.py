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
class GreateNoteContentHandle(unittest.TestCase):
    ga = GeneralAssert()
    dataclean = DataClear()
    datacreate = DataCreate()
    re = BusinessRe()
    apiConfig = YamlRead().api_config()['create_note_content']
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

    def testCase11_handle_repeat_data(self):
        """上传/更新便签内容接口，handle：重复数据校验"""
        # 前置条件：用户"user_id1"下新建一条便签内容
        noteid = str(int(time.time() * 1000))
        body = {
            "noteId": noteid,
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        self.re.post(self.url, self.sid1, self.user_id1, body)
        # 测试步骤：更新noteId为noteid的便签内容
        body = {
            "noteId": noteid,
            "title": 'test1',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        # 数据源校验
        ress = self.dataclean.select_list_notes(self.user_id1, sid=self.sid1)
        self.assertEqual(noteid, ress[0], msg='数据源校验失败')

    def testCase12_handle_ultraVires(self):
        """上传/更新便签内容接口，handle：越权"""
        # 前置条件：用户"user_id2"下有一条便签数据
        res_noteid = self.datacreate.note_create(1, self.user_id2, self.sid2)
        # 用户"user_id1"修改用户B的便签内容
        body = {
            "noteId": res_noteid[0],
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id2, body)
        self.assertEqual(412, res.status_code, msg='状态码校验失败')

    def testCase13_handle_stateLimit_fz(self):
        """上传/更新便签内容接口，handle：状态限制--修改分组便签"""
        # 前置条件：用户"user_id1"下有一条分组便签数据，无首页便签数据
        group_id = str(int(time.time() * 1000))
        res_noteid = self.datacreate.note_create(1, self.user_id1, self.sid1, group_id=group_id)
        # 测试步骤：修改该分组便签的便签内容
        body = {
            "noteId": res_noteid[0],
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        # 数据源校验
        # 校验是否无首页便签
        ress = self.dataclean.select_list_notes(self.user_id1, sid=self.sid1)
        self.assertEqual(0, len(ress), msg='数据源校验失败')
        # 校验分组便签是否仅有一条
        ress = self.dataclean.select_fz_notes(user_id=self.user_id1, sid=self.sid1, group_id=group_id)
        self.assertEqual(1, len(ress), msg='数据源校验失败')

    def testCase14_handle_stateLimit_rl(self):
        """上传/更新便签内容接口，handle：状态限制--修改日历便签"""
        # 前置条件：用户"user_id1"下有一条日历便签数据，无首页便签数据
        remind_time = time.time()
        res_noteid = self.datacreate.note_create(1, self.user_id1, self.sid1, remind_time=remind_time)
        # 测试步骤：修改该日历便签的便签内容
        body = {
            "noteId": res_noteid[0],
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        # 数据源校验
        # 校验是否无首页便签
        ress = self.dataclean.select_list_notes(self.user_id1, sid=self.sid1)
        self.assertEqual(0, len(ress), msg='数据源校验失败')
        # 校验日历便签是否仅有一条
        ress = self.dataclean.select_rl_notes(user_id=self.user_id1, sid=self.sid1)
        self.assertEqual(1, len(ress), msg='数据源校验失败')

    def testCase15_handle_stateLimit_bsc(self):
        """上传/更新便签内容接口，handle：状态限制--修改被删除便签"""
        # 前置条件：用户"user_id1"下有一条被删除便签数据，无首页便签数据
        note_lists_id = self.datacreate.note_create(1, self.user_id1, self.sid1)
        self.dataclean.soft_del_notes(user_id=self.user_id1, sid=self.sid1, node_id=note_lists_id[0])
        # 测试步骤：修改该被删除便签的便签内容
        body = {
            "noteId": note_lists_id[0],
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')

    def testCase35_handle_stateLimit_bqk(self):
        """上传/更新便签内容接口，handle：状态限制--修改被清空便签"""
        # 前置条件：用户"user_id1"下有一条被清空便签数据，无首页便签数据
        note_lists_id = self.datacreate.note_create(1, self.user_id1, self.sid1)
        self.dataclean.del_notes(self.user_id1, self.sid1)
        # 测试步骤：修改该被清空便签的便签内容
        body = {
            "noteId": note_lists_id[0],
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
