FUNCTION LLM_GENERATE_ANSWER(query, context):
    // 通用问答生成
    prompt = FORMAT_QA_PROMPT(query, context)
    // 调用在线LLM API，并处理重试等逻辑
    response = CALL_ONLINE_LLM_API(prompt)
    RETURN response.content
END FUNCTION

FUNCTION LLM_EXTRACT_ENTITIES(query):
    // 从用户问题中提取实体
    prompt = FORMAT_ENTITY_EXTRACTION_PROMPT(query)
    response = CALL_LOCAL_LLM(prompt) // 使用本地模型以提高效率
    // 解析并验证返回的JSON
    entities = PARSE_AND_VALIDATE_JSON(response.content)
    RETURN entities
END FUNCTION

FUNCTION LLM_EXTRACT_... (other extraction tasks):
    // 其他结构化信息提取任务的通用模式
    // 1. 构建一个带有详细指令和JSON Schema的Prompt
    prompt = FORMAT_SPECIFIC_EXTRACTION_PROMPT(text_chunk, json_schema)
    // 2. 调用LLM
    response = CALL_LLM(prompt)
    // 3. 修复、解析并验证返回的JSON数据
    structured_data = REPAIR_AND_PARSE_JSON(response.content)
    RETURN structured_data
END FUNCTION