"""
数据工具类 - 处理测试数据生成和管理
"""
from faker import Faker
import random
import string
import time


class DataUtil:
    """数据工具类"""
    
    def __init__(self):
        self.faker = Faker("zh_CN")
    
    def generate_username(self):
        """生成随机用户名"""
        return f"test_{self.faker.user_name()[:8]}"
    
    def generate_password(self, length=8):
        """生成随机密码"""
        return self.faker.password(length=length)
    
    def generate_nickname(self):
        """生成随机昵称"""
        return self.faker.name()
    
    def generate_phone(self):
        """生成随机手机号"""
        return self.faker.phone_number()
    
    def generate_email(self):
        """生成随机邮箱"""
        return self.faker.email()
    
    def generate_title(self, prefix="测试"):
        """生成随机标题"""
        return f"{prefix}_{self.faker.sentence(nb_words=4)}"
    
    def generate_content(self, paragraphs=2):
        """生成随机内容"""
        return self.faker.text(max_nb_chars=200)
    
    def generate_student_id(self):
        """生成随机学号"""
        year = random.randint(2020, 2024)
        return f"{year}{random.randint(10000, 99999)}"
    
    def generate_unique_id(self):
        """生成唯一ID"""
        return f"{int(time.time() * 1000)}_{random.randint(1000, 9999)}"
    
    def generate_reason(self):
        """生成举报/封禁原因"""
        reasons = [
            "内容违规",
            "虚假信息",
            "垃圾广告",
            "恶意攻击",
            "骚扰他人",
            "传播不良信息"
        ]
        return random.choice(reasons)


# 全局数据工具实例
data_util = DataUtil()