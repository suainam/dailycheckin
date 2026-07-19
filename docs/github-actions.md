# GitHub Actions 签到

Fork 可通过 GitHub Actions 独立执行签到，不影响 Docker、青龙、群晖或 AuroraOps 执行面。

## 配置

1. 在仓库 Settings → Environments 创建 `production` environment。
2. 添加 environment secret `DAILYCHECKIN_CONFIG_JSON`。
3. Secret 值使用完整 `config.json` 内容，不要提交真实配置文件。
4. 在 Actions 页面手动运行 `Daily check-in` 完成首次验证。

工作流使用 `Asia/Shanghai` 时区，每天北京时间 `00:01`、`17:01` 运行。第二次不是按首次结果触发的条件重试，而是固定补跑；签到服务应能安全处理“今日已签到”。GitHub 定时任务可能延迟；需要严格准点时继续使用宿主机执行面。

Actions 使用 `python -m dailycheckin.main --fail-on-error`：所有账号仍会依次执行，但任一账号抛出执行异常或配置无效都会令 workflow 失败。签到服务返回的业务提示仍保留原项目语义，不通过文本关键字猜测成败。传统调用不传此参数，保持原有退出行为。

运行日志默认只记录消息长度、HTTP 状态及脱敏诊断，不输出消息或响应体。临时排障可设置 `DAILYCHECKIN_DEBUG_LOGS=true`，但详细日志可能包含账号信息，不应在公共 Actions 中启用。配置、Cookie 和 token 不得写入日志或作为 artifact 上传。
