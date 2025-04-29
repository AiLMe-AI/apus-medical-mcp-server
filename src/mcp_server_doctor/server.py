# dify_server.py
from typing import Dict, Optional
from mcp.server.fastmcp import FastMCP
import os
import httpx
import logging
import dotenv

dotenv.load_dotenv()

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# 初始化MCP服务
doctor_mcp = FastMCP(
    "mcp-server-doctor",
    prompt="你是一个医疗咨询助手，请根据用户的问题提供专业的医疗建议和诊断。",
)


async def doctor_answer(query: str, api: str, conversation_id: Optional[str] = None, user_id: Optional[str] = None) -> str:
    doctor_api_key = os.environ.get("DOCTOR_API_KEY", "")
    try:
        params = {
            "query": query
        }
        if conversation_id:
            params["conversation_id"] = conversation_id
        if user_id:
            params["user_id"] = user_id


        headers = {
            "Authorization": f"Bearer {doctor_api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                api, headers=headers, params=params, timeout=60.0
            )

            response.raise_for_status()
            resp = response.json()
            return resp.get("data",{"answer":"Doctor error."}).get("answer")

    except httpx.HTTPStatusError as e:
        return f"Doctor API HTTP error occurred: {e.response.status_code} - {e.response.text}"
    except httpx.RequestError as e:
        return f"Error communicating with Doctor API: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"


@doctor_mcp.tool()
async def western_doctor(query: str, conversation_id: Optional[str] = None, user_id: Optional[str] = None) -> str:
    """
    提供西医相关的医疗建议和诊断
    
    Args:
        query: 用户的问题
        conversation_id: 会话ID，可选
        user_id: 用户ID，可选
    
    Returns:
        西医相关的医疗建议和诊断
    """
    api = "https://open-ai.apusai.com/open-api/western_doctor"
    return await doctor_answer(query, api, conversation_id, user_id)


@doctor_mcp.tool()
async def tcm_doctor(query: str, conversation_id: Optional[str] = None, user_id: Optional[str] = None) -> str:
    """
    提供中国传统中医相关的医疗建议和诊断
    
    Args:
        query: 用户的问题
        conversation_id: 会话ID，可选
        user_id: 用户ID，可选
    
    Returns:
        中医相关的医疗建议和诊断
    """
    api = "https://open-ai.apusai.com/open-api/tcm_doctor"
    return await doctor_answer(query, api, conversation_id, user_id)


# def main():
#     log.info(f"启动服务中...")
#     doctor_mcp.run(transport="sse") 

# if __name__ == "__main__":
#     main()