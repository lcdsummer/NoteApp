import unittest
from common.generalAssert import GeneralAssert
from common.caseMsgLogs import class_case_decoration
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from business.businessRe import BusinessRe
from common.yamlRead import YamlRead
import time
from parameterized import parameterized


@class_case_decoration
class GreateNoteContentInput(unittest.TestCase):
    ga = GeneralAssert()
    dataclean = DataClear()
    datacreate = DataCreate()
    re = BusinessRe()
    apiConfig = YamlRead().api_config()['create_note_content']
    envConfig = YamlRead().env_config()
    user_id1 = envConfig['user_id1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    url = host + apiConfig['path']
    mustKeys = apiConfig['mustKeys']

    def setUp(self) -> None:
        """重置数据"""
        self.dataclean.del_notes(self.user_id1, self.sid1)

    @parameterized.expand(mustKeys)
    def testCase02_input_mustKey_remove(self, key):
        """上传/更新便签内容接口，input：必填字段的key缺失"""
        # 测试步骤：用户"user_id1"下新建一条便签内容
        noteid = str(int(time.time() * 1000))
        body = {
            "noteId": noteid,
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        body.pop(key)
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(400, res.status_code, msg='状态码校验失败')

    @parameterized.expand(mustKeys)
    def testCase03_input_mustKey_null(self, key):
        """上传/更新便签内容接口，input：必填字段的值为空"""
        # 测试步骤：用户"user_id1"下新建一条便签内容
        noteid = str(int(time.time() * 1000))
        body = {
            "noteId": noteid,
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        body[key] = ''
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(400, res.status_code, msg='状态码校验失败')

    def testCase04_input_noteId_type(self):
        """上传/更新便签内容接口，input：noteId的字符串类型校验--长度校验"""
        # 测试步骤：用户"user_id1"下新建一条便签内容
        body = {
            "noteId": "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz",
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase05_input_noteId_type(self):
        """上传/更新便签内容接口，input：noteId的字符串类型校验--特殊字符校验--中文"""
        # 测试步骤：用户"user_id1"下新建一条便签内容
        body = {
            "noteId": "中文",
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase06_input_noteId_type(self):
        """上传/更新便签内容接口，input：noteId的字符串类型校验--特殊字符校验"""
        # 测试步骤：用户"user_id1"下新建一条便签内容
        body = {
            "noteId": "&*%￥#@",
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase07_input_noteId_type(self):
        """上传/更新便签内容接口，input：noteId的字符串类型校验--英文大小写校验"""
        # 前置条件：用户"user_id1"下新建一条noteId为"ABCED"便签内容
        re_body = {
            "noteId": "ABCED",
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        self.re.post(self.url, self.sid1, self.user_id1, re_body)
        # 测试步骤：用户"user_id1"下新建一条noteId为"abcde"便签内容
        body = {
            "noteId": "abcde",
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1,
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        # 查看结果，若便签条数为两条，说明有进行英文大小写校验
        ress = self.dataclean.select_list_notes(self.user_id1, sid=self.sid1)
        self.assertEqual(2, len(ress), msg='英文大小写校验失败')

    def testCase08_input_localContentVersion_type(self):
        """上传/更新便签内容接口，input：localContentVersion的int类型校验--字符串形式的数值校验"""
        # 测试步骤：用户"user_id1"下新建一条便签内容
        noteid = str(int(time.time() * 1000))
        body = {
            "noteId": noteid,
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": '1',
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(400, res.status_code, msg='状态码校验失败')

    def testCase09_input_localContentVersion_type(self):
        """上传/更新便签内容接口，input：localContentVersion的int类型校验--传入特殊值 -1"""
        # 测试步骤：用户"user_id1"下新建一条便签内容
        noteid = str(int(time.time() * 1000))
        body = {
            "noteId": noteid,
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": -1,
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(400, res.status_code, msg='状态码校验失败')

    def testCase10_input_localContentVersion_type(self):
        """上传/更新便签内容接口，input：localContentVersion的int类型校验--传入小数 1.5"""
        # 测试步骤：用户"user_id1"下新建一条便签内容
        noteid = str(int(time.time() * 1000))
        body = {
            "noteId": noteid,
            "title": 'test',
            "summary": 'test',
            "body": 'test',
            "localContentVersion": 1.5,
            "BodyType": 0,
        }
        res = self.re.post(self.url, self.sid1, self.user_id1, body)
        self.assertEqual(400, res.status_code, msg='状态码校验失败')