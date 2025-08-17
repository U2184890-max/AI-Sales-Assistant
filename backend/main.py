FUNCTION main:
    // 1. 初始化FastAPI应用实例
    app = CREATE_FASTAPI_APP(title="AI Sales Assistant")

    // 2. 配置CORS中间件，允许所有跨域请求
    app.ENABLE_CORS_MIDDLEWARE()

    // 3. 定义并执行应用的生命周期管理函数
    ON_APP_STARTUP:
        LOG "应用启动，开始初始化..."
        CALL connect_to_databases() // 连接MySQL, Redis, Neo4j
        CALL load_ai_models_into_memory() // 加载嵌入、重排序和LLM模型
        LOG "初始化完成"
    ON_APP_SHUTDOWN:
        LOG "应用关闭，释放资源..."
        CALL close_database_connections()
        LOG "资源已释放"

    // 4. 挂载各个模块的API路由
    app.INCLUDE_ROUTER(auth_router, prefix="/auth")
    app.INCLUDE_ROUTER(chat_router, prefix="/chat")
    app.INCLUDE_ROUTER(kb_router, prefix="/kb")

    // 5. 挂载静态文件目录，用于手册下载
    app.MOUNT_STATIC_DIRECTORY(url="/manuals", path="/static/manuals")
END FUNCTION
