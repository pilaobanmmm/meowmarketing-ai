# 🐱 MeowMarketing AI —— 零基础练手版

营销/内容运营求职作品集练习：一个可以直接上传 GitHub 的 Streamlit 小应用。

## 功能与诚实标注

- **阶段 1（不需要 API）**：填写品牌、产品、目标用户、平台、营销目标，生成 7 或 14 天内容排期，导出 CSV（Excel 可打开）。**这是规则模板生成，不是 AI。**
- **阶段 2（需要 API）**：调用 OpenAI 模型，根据营销 Brief 和排期生成内容创意。需要你自己开通 API 计费。ChatGPT Plus/Pro 订阅不等于 API 额度。
- 这个包是原创轻量入门示例，可参考 [AI Content Calendar Generator](https://github.com/celalakcelikk/ai-content-calendar-generator) 学习更复杂的版本。并未拷贝其源代码。

## A. 电脑运行（需要安装 Python）

1. 解压整个文件夹，打开终端并进入这个文件夹。
2. 输入：`python -m pip install -r requirements.txt`
3. 输入：`python -m streamlit run app.py`
4. 浏览器打开终端显示的地址（一般是 `http://localhost:8501`）。
5. 在左边填写信息、点击“生成内容排期”、导出 CSV。

有的 Windows 环境用 `py` 而不是 `python`；需要先安装 Python 3.10+。

## B. 不想安装 Python？使用 GitHub + Streamlit Cloud

1. 注册/登录 GitHub，并创建一个新的 public 仓库（例如 `meowmarketing-ai`）。
2. 解压 ZIP，在 GitHub 仓库中使用 **Add file → Upload files** 上传 `app.py`、`requirements.txt`、`README_CN.md` 和 `.gitignore`。点击 **Commit changes**。
3. 打开 https://share.streamlit.io/ ，关联 GitHub，选择刚创建的仓库。
4. 部署时将入口文件设置为 `app.py`。第一阶段无需 API Key，应该能够看到页面。
5. 页面错误时，复制**完整报错**给 AI，询问哪一个文件的哪一行要改；不要一次修改十处。

官方说明：https://docs.streamlit.io/deploy/streamlit-community-cloud/get-started

注意：免费部署环境的限制和账户政策可能变化，按官方页面为准。

## C. 第二阶段：启用真正的 AI 功能

**不要把 API Key 写在代码里、截图里，或上传至公共 GitHub。**

本机 macOS/Linux 可在终端设置：
`export OPENAI_API_KEY="你的密钥"`

Windows PowerShell：
`$env:OPENAI_API_KEY="你的密钥"`

再从同一终端运行 `python -m streamlit run app.py`。

如果部署到 Streamlit Community Cloud，请到你的应用设置中通过 **Secrets** 添加：
`OPENAI_API_KEY = "你的密钥"`

模型默认 `gpt-4o-mini`，如果当前 API 不提供该模型，可通过 `OPENAI_MODEL` 环境变量调整为账户可用的文本模型。API Key 需要来自 OpenAI API 平台，不是 ChatGPT 登录密码。请设置用量/消费控制，并仅上传无敏感信息的演示数据。

## D. 怎么改成“自己做的项目”

建议至少完成 **三项原创改动**（可请 AI 协助编程）：

1. 将选题模板由美妆通用版改成你自己的目标行业（如游戏、餐饮或时尚）。
2. 增加一个自己的营销策略模块，例如按“认知—种草—转化”分配内容类型，并解释为何如此安排。
3. 设计两组不同受众的测试 Brief，比较内容是否真的适配目标用户，写一页人工评估报告。
4. 改善界面或导出字段，例如加入负责人、制作状态和 KPI 计划值（不要冒充真实投放数据）。
5. 录制 1 分钟操作展示视频，并写清楚参考仓库、AI 协作内容和自己实际完成的部分。

## E. 给 AI 的第一句提示词

> 我完全不会 Python。这是一个用于营销/内容运营求职作品集的 Streamlit 项目。请先阅读 `app.py` 和 `README_CN.md`。不要重写整个项目，也不要一下增加多个功能。先用通俗中文告诉我文件各自负责什么，然后帮我做**唯一一个改动**：为排期表添加“内容负责人”字段。给出完整需替换的代码位置、修改原因和我应该如何测试。任何步骤都不要假设我会用终端或 Git。

## F. 作品集展示建议

简历/面试时诚实讲述：业务问题、为什么选择这个工具、你设计的规则与测试数据、AI 帮你写了哪些代码、发现过什么 bug、你如何验证输出、接下来如何改进。**不要把模板排期说成 AI 生成，也不要把模拟数据说成真实经营效果。**
