# 🚀 Vocab-AI-Agent: LLM 驱动的词汇结构化提取引擎

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![LLM API](https://img.shields.io/badge/LLM-DeepSeek--V4-green.svg)](https://api.deepseek.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

一个基于 Python 与大模型 API 构建的轻量级、高可用的词汇扩展与处理流（Workflow）。本项目致力于解决非结构化文本在 AI 提取过程中的痛点，通过深度的 Prompt 工程与容错机制，实现 **100% 稳定的结构化 JSON 数据输出**。

## ✨ 核心工程特性 (Features)

*   **🛡️ 结构化输出保障**: 针对 LLM 常见的“格式幻觉”进行底层优化，强制输出标准 JSON，可直接对接数据库或其他前端业务流，实现真正的“即插即用”。
*   **🧠 深度 Prompt 调优**: 专为英语词汇解析场景设计的上下文锚点（Context Anchor），精准提取词性、多义词释义及原生语境例句。
*   **⚙️ 强健的异常处理**: 内置 API 超时重试、异常捕获与脏数据清洗管道，确保批量处理任务时的工程稳定性。

## 🛠️ 技术栈 (Tech Stack)

*   **核心逻辑**: Python 3.10+
*   **模型大脑**: 接入 DeepSeek-V4 API（兼容其他主流大语言模型标准接口）
*   **数据处理**: JSON 序列化 / dotenv 环境变量管理

## 🚀 快速开始 (Quick Start)

### 1. 环境准备
确保您的本地环境已安装 Python 3.10 或更高版本。克隆本仓库到本地：

```bash
git clone [https://github.com/nitianxia2026-rgb/vocab-ai-agent.git](https://github.com/nitianxia2026-rgb/vocab-ai-agent.git)
cd vocab-ai-agent
```

### 2. 配置凭证
系统采用了严格的环境变量隔离机制。请在项目根目录创建 `.env` 文件，并填入您的大模型 API Key：

```text
# .env 示例
LLM_API_KEY=sk-your_api_key_here
```

### 3. 运行引擎
```bash
# 运行主控脚本
python main.py
```

## 📂 输出示例 (Output Example)

引擎运行后，将直接生成可被下游业务层无缝调用的 JSON 结构：

```json
{
  "word": "architect",
  "part_of_speech": "n.",
  "definition": "a person who designs buildings and in many cases also supervises their construction.",
  "example": "He is the chief architect of the company's new AI workflow."
}
```

## 🤝 关于我 (About)
专注于 AI 应用层开发与 AI 工作流架构落地。追求以最简洁的代码和最优的 API 组合，构建高性价比、可商业化的智能体（Agent）解决方案。