"""Demo"""

import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv
load_dotenv()

# pylint: disable=wrong-import-position
from fastapi import FastAPI
import uvicorn
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitSDK, LangGraphAgent
from research_canvas.langgraph.agent import workflow, compile_kwargs
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    """Lifespan for the FastAPI app with AsyncSqliteSaver for thread persistence."""
    async with AsyncSqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
        # Compile graph with persistent checkpointer
        graph = workflow.compile(checkpointer=checkpointer, **compile_kwargs)

        # Create SDK with the compiled graph
        sdk = CopilotKitSDK(
            agents=[
                LangGraphAgent(
                    name="research_agent",
                    description="Research agent.",
                    graph=graph,
                ),
            ],
        )

        # Add the CopilotKit FastAPI endpoint
        add_fastapi_endpoint(fastapi_app, sdk, "/copilotkit")
        yield

app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}


def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(
        "research_canvas.demo:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        reload_dirs=(
            ["."] +
            (["../../../sdk-python/copilotkit"]
             if os.path.exists("../../../sdk-python/copilotkit")
             else []
             )
        )
    )
