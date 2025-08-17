FUNCTION chat_endpoint(session_id, user_prompt, retrieval_mode):
    // 1. 获取并验证用户会话
    session = GET_SESSION_FROM_DB(session_id)
    VALIDATE_USER_PERMISSION(current_user, session)

    // 2. 保存用户消息
    SAVE_MESSAGE_TO_DB(session_id, role="user", content=user_prompt)

    // 3. 加载当前会话的状态机
    state = session.state

    // 4. 核心意图识别
    intent = DETERMINE_INTENT(user_prompt, state)

    // 5. 根据意图进入不同的处理流程 (状态机)
    SWITCH intent:
        CASE "restart_flow":
            state = INITIALIZE_NEW_STATE()
            response_text = "好的，我们重新开始。"
        CASE "request_guidance":
            state.current_flow = "newbie_guidance"
            response_text = HANDLE_NEWBIE_GUIDANCE(state)
        CASE "knowledge_query":
            // 如果是知识问答，直接调用RAG流程
            response_text = EXECUTE_RAG_QUERY(user_prompt, retrieval_mode)
        CASE "expert_filter_or_general_query":
            state.current_flow = "expert_mode"
            response_text = HANDLE_EXPERT_MODE(user_prompt, state, retrieval_mode)
        // ... 其他意图处理
    END SWITCH

    // 6. 更新并保存会话状态
    state.last_assistant_message = response_text
    UPDATE_SESSION_STATE_IN_DB(session_id, state)

    // 7. 保存助手消息并返回
    SAVE_MESSAGE_TO_DB(session_id, role="assistant", content=response_text)
    RETURN {response: response_text}
END FUNCTION

FUNCTION EXECUTE_RAG_QUERY(query, retrieval_mode):
    // 1. 使用AI从问题中提取关键实体
    entities = LLM_EXTRACT_ENTITIES(query)

    // 2. 初始化上下文容器
    vector_context = ""
    graph_context = ""
    cache_context = ""

    // 3. 根据检索模式，从不同知识源获取信息
    IF retrieval_mode IS "hybrid" OR "kg_only":
        IF entities IS NOT EMPTY:
            // 从知识图谱检索与实体相关的三元组
            graph_context = RAG_SERVICE.SEARCH_GRAPH(entities)
        END IF
    END IF

    IF retrieval_mode IS "hybrid" OR "kb_only":
        // 从向量数据库检索最相关的文本块
        vector_context = RAG_SERVICE.SEARCH_VECTORS(query)
    END IF

    // 4. 组合所有上下文信息
    final_context = COMBINE_CONTEXTS(vector_context, graph_context, cache_context)

    // 5. 如果没有任何上下文，返回无法回答
    IF final_context IS EMPTY THEN
        RETURN "抱歉，我无法回答这个问题。"
    END IF

    // 6. 将组合后的上下文和原始问题喂给LLM，生成最终答案
    final_answer = LLM_GENERATE_ANSWER(query, final_context)
    RETURN final_answer
END FUNCTION
