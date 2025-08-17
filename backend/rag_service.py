FUNCTION rebuild_kb_assets (BACKGROUND TASK):
    // 这是在后台运行的核心任务，用于构建知识库
    LOG "开始构建知识库..."
    SET_KB_STATUS_IN_REDIS("processing")

    // 1. 解析上传的文档，将其分割成文本块 (chunks)
    chunks = PARSE_DOCUMENTS_INTO_CHUNKS(uploaded_files)

    // 2. 为每个文本块生成向量嵌入
    embeddings = EMBEDDING_MODEL.ENCODE(chunks)

    // 3. 构建并保存Faiss向量索引
    faiss_index = BUILD_FAISS_INDEX(embeddings)
    SAVE_FAISS_INDEX(faiss_index)

    // 4. 并发地从每个文本块中提取知识图谱三元组
    graph_triples = CONCURRENTLY_CALL_LLM_FOR_GRAPH_EXTRACTION(chunks)

    // 5. 将提取出的三元组写入Neo4j图数据库
    WRITE_TRIPLES_TO_NEO4J(graph_triples)

    // 6. (可选) 如果是结构化文档，提取产品规格并缓存
    IF document_type IS "structured":
        specs = CONCURRENTLY_CALL_LLM_FOR_SPECS_EXTRACTION(chunks)
        SAVE_SPECS_TO_CACHE_FILE(specs)
    END IF

    SET_KB_STATUS_IN_REDIS("completed")
    LOG "知识库构建完成"
END FUNCTION

FUNCTION SEARCH_VECTORS(query):
    // 向量检索流程
    query_embedding = EMBEDDING_MODEL.ENCODE(query)
    // 1. 在Faiss中进行初步的相似度搜索，召回Top-K个候选文档
    candidate_indices = FAISS_INDEX.SEARCH(query_embedding, k=20)
    candidate_docs = GET_DOCS_BY_INDICES(candidate_indices)

    // 2. 使用更强大的重排序模型对候选文档进行精确排序
    scores = RERANKER_MODEL.PREDICT(query, candidate_docs)
    sorted_docs = SORT_DOCS_BY_SCORES(scores)

    // 3. 返回最终的Top-N个最相关文档
    RETURN sorted_docs.slice(0, 3)
END FUNCTION

FUNCTION SEARCH_GRAPH(entities):
    // 知识图谱检索流程
    // 构建一个Cypher查询，查找与给定实体直接相连的所有节点和关系
    cypher_query = "MATCH (n)-[r]-(neighbor) WHERE n.id IN $entities RETURN n, r, neighbor"
    
    // 执行查询并格式化结果
    results = NEO4J_DATABASE.EXECUTE_QUERY(cypher_query, entities=entities)
    formatted_triples = FORMAT_NEO4J_RESULTS_AS_TEXT(results)
    RETURN formatted_triples
END FUNCTION
