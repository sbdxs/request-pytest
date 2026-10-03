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

用例与 `../接口测试用例/` 目录下的用例文档一一对应（用例编号见各 test 文件内的 docstring），共 **128 条**：

| 模块 | 用例文档 | 测试用例数 | P0 | P1 | P2 |
|------|-----------|-----------|----|----|----|
| 用户模块 | 01-用户模块用例.md | 33 | 11 | 17 | 5 |
| 论坛模块 | 02-论坛模块用例.md | 33 | 12 | 17 | 4 |
| 失物招领模块 | 03-失物招领模块用例.md | 26 | 6 | 15 | 5 |
| 新闻公告模块 | 04-新闻公告模块用例.md | 13 | 6 | 6 | 1 |
| 私信模块 | 05-私信模块用例.md | 13 | 4 | 8 | 1 |
| 首页+文件上传 | 06-首页与文件上传用例.md | 10 | 2 | 2 | 6 |
| **总计** | | **128** | **41** | **65** | **22** |

## 测试覆盖范围

用例设计遵循 `../接口测试用例/00-总览与设计说明.md` 的五条原则：

1. **每个接口至少一条正向用例**：注册、发帖、审核、私信等主流程闭环，并做"写后回查"（发帖后查详情、改资料后查信息）。
2. **参数校验以后端 DTO 为准**：用户名 3-20 位、密码 6-20 位、标题 2-200 字等边界值，断言后端注解的真实提示文案。
3. **权限三维覆盖**：未登录（code=401）、普通用户、管理员三类身份访问受保护接口。
4. **状态流转闭环**：发布 → 待审核 → 审核通过 → 可见 → 删除，按业务链路串联。
5. **测试数据自造自清**：注册/发帖使用唯一前缀数据，封禁用例 try/finally 保证解封，评论/收藏用例测完即删。

### 用户模块（test_user.py，USER-001 ~ USER-033）
- 注册：正常、重复用户名、用户名 2/21 位、密码 5 位、缺邮箱、仅必填项
- 登录：用户名/学号登录、密码错误、账号不存在、空账号、封禁用户登录
- 用户信息：获取当前用户、未登录 401
- 封禁状态查询、资料修改（昵称/邮箱回查）、密码修改（临时用户改密+新旧密码验证）
- 管理员：用户列表分页/关键词、仪表盘、用户详情/不存在/更新用户
- 封禁与解封：封号后无法登录、解封后恢复、禁言+到期时间仍可登录（try/finally 解封）

### 论坛模块（test_forum.py，FORUM-001 ~ FORUM-033）
- 分类列表、发帖（正常/未登录/标题过短/空内容/无分类/分类不存在）
- 列表（分页/分类筛选/关键词搜索）、详情（正常/不存在/未审核对他人不可见）
- 删除（作者删除+回查、非作者删除被拒）
- 我的发布/回复/收藏
- 评论（发表/列表回查/空内容/删除自己的评论）
- 点赞与取消、收藏与取消（回查状态翻转）
- 举报（他人帖子/空原因）、管理员：待审核列表、审核通过后可见、监管列表、评论列表、举报列表与处理、越权访问

### 失物招领模块（test_lostfound.py，LF-001 ~ LF-026）
- 发布寻物/招领、type 越界、标题过短、物品名为空、分类越界、描述超长
- 列表（分页/类型筛选/关键词）、详情（正常/不存在）、状态更新
- 编辑（本人/非作者被拒）、删除（本人+回查）、我的发布
- 举报（他人记录/原因过短）、管理员：列表、审核通过后可见、详情、举报记录、举报列表与处理、管理员删除、越权访问

### 新闻公告模块（test_news.py，NEWS-001 ~ NEWS-013）
- 浏览：列表、分类筛选、分页生效、详情、不存在、轮播
- 管理员：创建、创建后用户端可见、更新回查、删除回查、查询全部、分页查询、越权/未登录访问

### 私信模块（test_im.py，IM-001 ~ IM-013）
- 会话：创建、重复创建返回同一会话、目标不存在、会话列表包含
- 消息：发送、接收方查看、超长 1001 字、空内容、非参与者（管理员）无法查看
- 已读/未读：标记已读、未读计数
- 举报：举报消息 → 举报列表 → 管理员处理
- 未登录访问 401

### 首页与文件上传（test_home.py，HOME-001，FILE-001 ~ FILE-010）
- 首页热点内容（无需登录）
- 单图上传：头像、非图片文件、空文件、无扩展名、新闻图（管理员）、失物图
- 批量上传：失物 2 张、超限 10 张、论坛 2 张、空文件列表

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