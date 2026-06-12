import httpx
from fastapi import HTTPException

from app.core.config import settings


async def request_deepseek(messages: list[dict]) -> str:
    if not settings.deepseek_api_key:
        raise HTTPException(status_code=503, detail="AI 服务未配置，请检查 DEEPSEEK_API_KEY。")

    url = f"{settings.deepseek_base_url.rstrip('/')}/chat/completions"
    payload = {
        "model": settings.deepseek_model,
        "messages": messages,
        "temperature": 0.2,
    }
    headers = {
        "Authorization": f"Bearer {settings.deepseek_api_key}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=httpx.Timeout(30.0, connect=10.0)) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
    except httpx.TimeoutException as exc:
        raise HTTPException(status_code=504, detail="AI 服务响应超时，请稍后重试。") from exc
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=502, detail=f"AI 服务调用失败，状态码 {exc.response.status_code}。") from exc
    except (httpx.HTTPError, ValueError, KeyError) as exc:
        raise HTTPException(status_code=502, detail="AI 服务调用失败，请检查 DeepSeek 配置。") from exc

    try:
        answer = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError, AttributeError) as exc:
        raise HTTPException(status_code=502, detail="AI 服务返回格式异常。") from exc
    if not answer:
        raise HTTPException(status_code=502, detail="AI 服务未返回有效内容。")
    return answer
