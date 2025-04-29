# Create server parameters for stdio connection
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.client import MultiServerMCPClient

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o")

async def main():
    print('开始执行...')
    
    print('初始化模型:', model)
    async with MultiServerMCPClient(
        {
            # "math": {
            #     "command": "python",
            #     "args": ["math_server.py"],
            #     "transport": "stdio",
            # },
            # "weather": {
            #     "url": "http://localhost:8000/sse",
            #     "transport": "sse",
            # },
            "doctor": {
                "url": "http://127.0.0.1:8000/sse",
                "transport": "sse",
            },
            # "llm": {
            #     "command": "python",
            #     "args": ["llm_server.py"],
            #     "transport": "stdio",
            # }
            # "poem": {
            #     # "url": "http://localhost:8000/sse",
            #     "url":"http://10.11.20.107:31091/e/fuv43z9mdd2icrtb/sse",
            #     "transport": "sse",
            # }
        }
    ) as client:
        print('已连接服务器，获取工具...')
        tools = client.get_tools()
        print(f'获取到 {len(tools)} 个工具')
        print(tools)
        
        agent = create_react_agent(model, tools)
        print('已创建agent，开始调用...')
        
        # 设置超时
        import asyncio
        
        # math_response = await asyncio.wait_for(
        #     agent.ainvoke({"messages": "what's (3 + 5) x 12?"}),
        #     timeout=30
        # )
        # print('数学响应:', math_response)
        
        weather_response = await agent.ainvoke({"messages": "肚子疼怎么办"})
        # weather_response = await agent.ainvoke({"messages": "北京市天气怎么样"})
        print('\n\n西医回复:', weather_response)
        
        # llm_response = await asyncio.wait_for(
        #     agent.ainvoke({"messages": "我肚子疼怎么办?"}),
        #     timeout=30
        # )
        # print('\n\nLLM响应:', llm_response)



# 运行主函数
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())