FUNCTION register_user(user_data):
    // 检查用户名或邮箱是否已存在
    IF user_exists_in_db(user_data.username) THEN
        THROW Error("用户名已存在")
    END IF

    // 对密码进行哈希处理
    hashed_password = HASH_PASSWORD(user_data.password)

    // 创建新用户并存入数据库
    new_user = CREATE_USER_RECORD(username, email, hashed_password)
    SAVE_TO_DATABASE(new_user)
    RETURN new_user
END FUNCTION

FUNCTION login_for_token(form_data):
    // 从数据库查找用户
    user = GET_USER_FROM_DB(form_data.username)

    // 验证用户是否存在以及密码是否正确
    IF NOT user OR NOT VERIFY_PASSWORD(form_data.password, user.hashed_password) THEN
        THROW Error("用户名或密码错误")
    END IF

    // 创建JWT令牌
    access_token = CREATE_JWT_TOKEN(user_id=user.id, username=user.username)
    RETURN {access_token: access_token, token_type: "bearer"}
END FUNCTION

FUNCTION get_current_active_user(token):
    // 解码JWT令牌
    payload = DECODE_JWT_TOKEN(token)
    username = payload.get("username")

    // 从数据库获取用户并检查是否为活动状态
    user = GET_USER_FROM_DB(username)
    IF NOT user OR NOT user.is_active THEN
        THROW Error("用户不存在或未激活")
    END IF
    RETURN user
END FUNCTION
