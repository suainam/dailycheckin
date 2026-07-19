# GitHub Actions 签到

Fork 可通过 GitHub Actions 独立执行签到，不影响 Docker、青龙、群晖或 AuroraOps 执行面。

本文是本 fork 的 GitHub Actions 运维权威；其他执行面继续使用各自入口。

## 配置

1. 在仓库 Settings → Environments 创建 `production` environment。
2. 添加 environment secret `DAILYCHECKIN_CONFIG_JSON`。
3. Secret 值使用完整 `config.json` 内容，不要提交真实配置文件。
4. 在 Actions 页面手动运行 `Daily check-in` 完成首次验证。

工作流使用 `Asia/Shanghai` 时区，每天北京时间 `00:01`、`17:01` 运行。第二次不是按首次结果触发的条件重试，而是固定补跑；签到服务应能安全处理“今日已签到”。GitHub 定时任务可能延迟；需要严格准点时继续使用宿主机执行面。

Actions 使用 `python -m dailycheckin.main --fail-on-error`：所有账号仍会依次执行，但任一账号抛出执行异常或配置无效都会令 workflow 失败。签到服务返回的业务提示仍保留原项目语义，不通过文本关键字猜测成败。传统调用不传此参数，保持原有退出行为。

运行日志默认只记录消息长度、HTTP 状态及脱敏诊断，不输出消息或响应体。临时排障可设置 `DAILYCHECKIN_DEBUG_LOGS=true`，但详细日志可能包含账号信息，不应在公共 Actions 中启用。配置、Cookie 和 token 不得写入日志或作为 artifact 上传。

## 运维边界

- Workflow 使用只读仓库权限，单次最长运行 20 分钟，同一调度组不主动取消正在执行的签到。
- `config.json` 只在 Job 内物化，权限为 `0600`，清理步骤始终执行。
- `Quality checks` 是代码与契约验证；真实 Provider 响应仍需手动或定时签到验证。
- 本 fork 不使用上游的 Deploy、Docker 发布和 PyPI 发布 workflows；不要为了签到重新启用它们。
- 修改依赖时才更新 `uv.lock`。一般代码和文档变更使用 `uv run --frozen`，避免隐式重写锁文件。
