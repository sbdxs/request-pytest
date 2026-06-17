# pytest + PO + request + allure 自动化测试框架

## 框架结构

```
pycharm/
├── api/                    # API层 - 封装接口请求
│   ├── base_api.py         # 基础API类
│   ├── user_api.py         # 用户模块API
│   ├── lostfound_api.py    # 失物招领API
│   ├── forum_api.py        # 论坛API
│   ├── im_api.py           # 私信API
│   ├── news_api.py         # 新闻API
│   └── home_api.py         # 首页API
├── config/                 # 配置层
│   ├── config.py           # 配置文件
│   └── __init__.py
├── testcases/              # 测试用例层
│   ├── test_user.py        # 用户模块测试
│   ├── test_lostfound.py   # 失物招领测试
│   ├── test_forum.py       # 论坛测试
│   ├── test_im.py          # 私信测试
│   ├── test_news.py        # 新闻测试
│   └── test_home.py        # 首页测试
├── utils/                  # 工具层
│   ├── request_util.py     # 请求工具
│   ├── auth_util.py        # 认证工具
│   ├── data_util.py        # 数据工具
│   └── __init__.py
├── conftest.py             # pytest配置和fixtures
├── pytest.ini              # pytest配置文件
├── requirements.txt        # 依赖文件
└── README.md               # 说明文档
```

## 环境准备

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境

修改 `config/config.py` 中的配置：

```python
# 基础URL配置
BASE_URL = "http://localhost:8080"

# 用户配置
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"
```

## 运行测试

### 1. 运行所有测试

```bash
pytest
```

### 2. 运行指定模块测试

```bash
pytest -m user          # 用户模块
pytest -m lostfound     # 失物招领模块
pytest -m forum         # 论坛模块
pytest -m im            # 私信模块
pytest -m news          # 新闻模块
pytest -m home          # 首页模块
pytest -m admin         # 管理员功能
```

### 3. 运行指定级别测试

```bash
pytest -m p0            # P0级别测试
pytest -m p1            # P1级别测试
pytest -m p2            # P2级别测试
pytest -m smoke         # 冒烟测试
```

### 4. 运行指定文件

```bash
pytest testcases/test_user.py
pytest testcases/test_lostfound.py
```

### 5. 运行指定测试类

```bash
pytest testcases/test_user.py::TestUserLogin
```

### 6. 运行指定测试方法

```bash
pytest testcases/test_user.py::TestUserLogin::test_login_success_username
```

## 生成报告

### 1. 生成Allure报告

```bash
pytest --alluredir=./report/allure
allure serve ./report/allure
```

### 2. 生成HTML报告

```bash
pytest --html=./report/report.html --self-contained-html
```

## 测试用例统计

| 模块 | 测试用例数 | P0 | P1 | P2 |
|------|-----------|----|----|----| 
| 用户模块 | 23 | 8 | 15 | 0 |
| 失物招领模块 | 16 | 6 | 10 | 0 |
| 论坛模块 | 18 | 6 | 12 | 0 |
| 私信模块 | 12 | 5 | 7 | 0 |
| 新闻公告模块 | 11 | 3 | 8 | 0 |
| 首页模块 | 1 | 1 | 0 | 0 |
| **总计** | **81** | **29** | **52** | **0** |

## 测试覆盖范围

### 用户模块
- 用户注册（正常、重复用户名、空用户名、密码长度不足）
- 用户登录（用户名登录、密码错误、用户不存在、封号用户）
- 用户信息（获取当前用户、未登录获取）
- 用户资料（更新昵称、邮箱、手机号）
- 密码修改（正常修改、旧密码错误）
- 用户封禁（禁言、封号、解封、获取封禁状态）
- 管理员功能（用户列表、仪表盘、用户详情、权限校验）

### 失物招领模块
- 信息发布（寻物、招领、标题为空、禁言用户）
- 列表查询（全部、按类型、按区域、分页）
- 详情查看（正常、不存在记录）
- 状态管理（更新状态）
- 举报功能（正常举报、重复举报）
- 管理员审核（列表、审核通过、审核拒绝、净化状态、处理举报）

### 论坛模块
- 帖子管理（分类列表、创建帖子、敏感词过滤、列表、详情、删除）
- 评论管理（创建、列表、删除、禁言用户）
- 互动功能（点赞、取消点赞、收藏、取消收藏）
- 举报功能（举报帖子）
- 管理员审核（待审核列表、审核帖子、净化状态、处理举报）

### 私信模块
- 会话管理（普通会话、业务会话、列表、禁言用户）
- 消息管理（发送文本、消息列表、标记已读、未读计数）
- 举报功能（举报消息、举报自己的消息）
- 管理员审核（举报列表、处理举报并封禁）

### 新闻公告模块
- 新闻列表（全部、按分类、置顶、分页）
- 新闻详情（正常、不存在、轮播新闻）
- 管理员功能（所有新闻、创建、更新、删除、权限校验）

### 首页模块
- 热点内容（获取热点内容）

## 技术栈

- **pytest**: 测试框架
- **requests**: HTTP请求库
- **allure-pytest**: 测试报告
- **loguru**: 日志记录
- **faker**: 测试数据生成
- **PyYAML**: 配置文件解析

## 最佳实践

1. **PO模式**: API层封装接口，测试用例层调用API
2. **数据驱动**: 使用fixtures生成测试数据
3. **Allure报告**: 每个测试用例添加详细的报告信息
4. **日志记录**: 使用loguru记录请求和响应
5. **权限分离**: 区分管理员和普通用户测试

## 注意事项

1. 运行测试前确保后端服务已启动
2. 管理员账号需要有足够的权限
3. 测试数据会自动生成，无需手动准备
4. 封禁测试会自动解封用户，不影响后续测试