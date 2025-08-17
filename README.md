Enterprise-Level AI Sales Assistant (企业级AI智能销售助手)
This is a full-stack, enterprise-level AI application designed to act as an intelligent sales assistant for the precision instrument industry. It leverages a sophisticated Retrieval-Augmented Generation (RAG) system to understand customer needs through multi-turn conversations and recommend the most suitable products from a complex knowledge base.

这是一个全栈的企业级AI应用，旨在模拟精密仪器行业的专业销售顾问。它通过一套先进的检索增强生成（RAG）系统，在多轮对话中理解客户需求，并从复杂的知识库中推荐最合适的产品。

核心功能 (Core Features)
双模对话系统 (Dual-Mode Dialogue System):

引导模式: 为新手用户提供逐步引导式问答，系统性地收集需求。

专家模式: 允许经验丰富的用户通过自然语言进行高效、灵活的直接查询和筛选。

高级混合式RAG引擎 (Advanced Hybrid RAG Engine):

向量检索: 使用 Faiss 和 Sentence-Transformers 进行高效的语义相似度搜索，并配备重排序模型（Re-ranker）优化精度。

知识图谱: 利用 Neo4j 构建产品、技术和业务问题的关系网络，通过AI实体提取和图查询，提供更具逻辑性的答案。

多模式查询: 支持“混合模式”、“仅知识图谱”、“仅向量库”三种检索模式，灵活应对不同查询场景。

全功能Web界面 (Full-Featured Web Interface):

基于原生JS构建的动态单页应用（SPA）。

实时聊天，支持Markdown渲染和代码高亮。

知识库管理：支持多种格式文档（Word, PDF等）的上传、处理和状态追踪。

知识图谱可视化：基于D3.js的交互式图谱编辑器，支持节点的增删改查。

多语言支持：完整的中/英文界面和AI交互。

异步后台任务 (Asynchronous Background Tasks):

知识库的构建、向量化和图谱提取等耗时操作均在后台处理，前端通过Redis实时获取任务进度。

技术栈 (Tech Stack)
后端 (Backend): Python, FastAPI, SQLModel, Uvicorn

数据库 (Databases): MySQL (业务数据), Neo4j (知识图谱), Redis (缓存 & 任务队列)

AI & RAG: PyTorch, Transformers, Sentence-Transformers, Faiss, LangChain

前端 (Frontend): HTML, CSS, JavaScript (ES6 Modules), Bootstrap 5, D3.js, Marked.js

DevOps: Docker, Docker Compose

运行与部署 (Setup & Deployment)
本项目已完全容器化，可通过 Docker Compose 一键启动。

1. 克隆仓库

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
cd your-repo-name

2. 准备模型文件 (Prepare Models)

本项目依赖于预先下载的Hugging Face模型。请将以下模型下载到项目根目录下的 models/ 文件夹中：

Qwen/Qwen2.5-7B-Instruct

BAAI/bge-m3

BAAI/bge-reranker-v2-m3

3. 配置环境变量 (Configure Environment)

复制环境变量模板文件 .env.example 并重命名为 .env。

cp .env.example .env

然后，编辑 .env 文件，填入您自己的 DASHSCOPE_API_KEY 和其他必要的凭证。

4. 启动服务 (Launch Services)

确保您已安装 Docker 和 Docker Compose，并已配置好NVIDIA Docker（如果使用GPU）。

docker-compose up --build -d

服务将在后台启动。您可以通过 docker-compose logs -f 查看日志。

5. 访问应用

前端界面: 在浏览器中直接打开 frontend/index.html 文件，或将其部署在任何静态文件服务器上。

后端API文档: http://localhost:5000/docs

Neo4j Browser: http://localhost:7474

许可证 (License)
本项目采用 MIT License。