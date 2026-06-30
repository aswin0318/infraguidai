from fastapi import FastAPI

from infraguid_common.observability.logger import configure_logging, get_logger

from app.api.routes import router

configure_logging()
logger = get_logger(__name__)

app = FastAPI(
    title="InfraGuidAI Agent Service",
    description="LangGraph ReAct DevOps agent with LangChain tools over Amazon Bedrock.",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
async def root() -> dict:
    return {"service": "agent-service", "status": "running"}
