import unittest
from common.generalAssert import GeneralAssert
from common.caseMsgLogs import class_case_decoration
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from business.businessRe import BusinessRe
from common.yamlRead import YamlRead
import json


@class_case_decoration
class GetNoteListInput(unittest.TestCase):
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

    def setUp(self) -> None:
        """重置数据"""
        self.dataclean.del_notes(self.user_id1, self.sid1)

    def testCase02_input_userid_must(self):
        """获取首页便签列表接口，userid必填项校验：不传值"""
        userid = ""
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(404, res.status_code, msg='状态码校验失败')

    def testCase03_input_userid_must(self):
        """获取首页便签列表接口，userid必填项校验：不传key"""
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(404, res.status_code, msg='状态码校验失败')

    def testCase04_input_userid_must(self):
        """获取首页便签列表接口，userid必填项校验：传入None"""
        userid = None
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase05_input_userid_type(self):
        """获取首页便签列表接口，userid的int类型校验：传入长度较长的数"""
        userid = 12345678912345678912345678912345678
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase06_input_userid_type(self):
        """获取首页便签列表接口，userid的int类型校验：传入-1"""
        userid = -1
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(412, res.status_code, msg='状态码校验失败')

    def testCase07_input_userid_type(self):
        """获取首页便签列表接口，userid的int类型校验：传入-1"""
        userid = 1.5
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{userid}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase08_input_userid_type(self):
        """获取首页便签列表接口，userid的int类型校验：传入字符串形式的数值"""
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{str(self.user_id1)}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(412, res.status_code, msg='状态码校验失败')

    def testCase09_input_startindex_must(self):
        """获取首页便签列表接口，startindex的必填项校验：不传值"""
        startindex = ""
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(404, res.status_code, msg='状态码校验失败')

    def testCase10_input_startindex_must(self):
        """获取首页便签列表接口，startindex的必填项校验：不传key"""
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(404, res.status_code, msg='状态码校验失败')

    def testCase11_input_startindex_must(self):
        """获取首页便签列表接口，startindex的必填项校验：传入None"""
        startindex = None
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase12_input_startindex_type(self):
        """获取首页便签列表接口，startindex的int类型校验：传入一个长度较长的数"""
        startindex = 12345678912345678912345678912345678
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase13_input_startindex_type(self):
        """获取首页便签列表接口，startindex的int类型校验：传入0"""
        startindex = 0
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')

    def testCase14_input_startindex_type(self):
        """获取首页便签列表接口，startindex的int类型校验：传入-1"""
        startindex = -1
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')

    def testCase15_input_startindex_type(self):
        """获取首页便签列表接口，startindex的int类型校验：传入1.5"""
        startindex = 1.5
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase16_input_startindex_type(self):
        """获取首页便签列表接口，startindex的int类型校验：传入字符串形式的数值"""
        startindex = "1"
        rows = 10
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')

    def testCase17_input_rows_must(self):
        """获取首页便签列表接口，rows的必填项校验：不传值"""
        startindex = 0
        rows = ""
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(404, res.status_code, msg='状态码校验失败')

    def testCase18_input_rows_must(self):
        """获取首页便签列表接口，rows的必填项校验：不传key"""
        startindex = 0
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(404, res.status_code, msg='状态码校验失败')

    def testCase19_input_rows_must(self):
        """获取首页便签列表接口，rows的必填项校验：传入None"""
        startindex = 0
        rows = None
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase20_input_rows_type(self):
        """获取首页便签列表接口，rows的int类型校验：传入一个长度较长的数"""
        startindex = 0
        rows = 12345678912345678912345678912345678
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(500, res.status_code, msg='状态码校验失败')

    def testCase21_input_rows_type(self):
        """获取首页便签列表接口，rows的int类型校验：传入0"""
        startindex = 0
        rows = 0
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(200, res.status_code, msg='状态码校验失败')

    def testCase22_input_rows_type(self):
        """获取首页便签列表接口，rows的int类型校验：传入-1"""
        startindex = 0
        rows = -1
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(400, res.status_code, msg='状态码校验失败')

    def testCase23_input_rows_type(self):
        """获取首页便签列表接口，rows的int类型校验：传入1.5"""
        startindex = 0
        rows = 1.5
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(400, res.status_code, msg='状态码校验失败')

    def testCase24_input_rows_type(self):
        """获取首页便签列表接口，rows的int类型校验：传入传入字符串形式的数值"""
        startindex = 0
        rows = "1"
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        self.assertEqual(400, res.status_code, msg='状态码校验失败')

    def testCase25_input_rows_type(self):
        """获取首页便签列表接口，rows的int类型校验：边界值校验"""
        # 前置条件：用户"user_id1"下有2条便签主体
        self.datacreate.note_create(2, self.user_id1, self.sid1)
        startindex = 0
        rows = 3
        url = self.host + f'/v3/notesvr/user/{self.user_id1}/home/startindex/{startindex}/rows/{rows}/notes'
        res = self.re.get(url, self.sid1)
        res_len = len((json.loads(res.text))['webNotes'])
        self.assertEqual(200, res.status_code, msg='状态码校验失败')
        self.assertEqual(2, res_len, msg='返回的便签条数不一致')
