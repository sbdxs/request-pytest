"""
首页模块API - 封装首页相关接口
"""
from api.base_api import BaseAPI
from allure import step


class HomeAPI(BaseAPI):
    """首页模块API"""
    
    @step("获取热点内容")
    def get_hot_content(self):
        """获取热点内容"""
        return self._get("/api/home/hot-content")


# 全局首页API实例
home_api = HomeAPI()