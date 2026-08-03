# app/api — HTTP 层

## 职责

- 路由、请求/响应绑定、Cookie、依赖注入
- 将 HTTP 输入交给 service；将结果写成 HTTP 输出
- `deps.py`：组装 Repository / Service、鉴权依赖

## 约定

- 路由挂在 `v1/router.py`，由 `main.py` 按 `api_v1_prefix` 挂载
- 未实现的接口可返回 `501`，并在 docstring 标明
- 本层可使用 `HTTPException`（鉴权失败、参数错误等）
- 不在路由里写业务规则或直接操作 ORM

## 禁止

- 在 api 中实现密码校验、幂等去重、token 轮转等业务
- 绕过 service 直接调用 repository（健康检查等基础设施除外）
