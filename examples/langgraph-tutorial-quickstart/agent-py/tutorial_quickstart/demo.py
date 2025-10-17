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
from tutorial_quickstart.agent import graph_builder
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager to set up AsyncSqliteSaver"""
    async with AsyncSqliteSaver.from_conn_string("checkpoints.db") as checkpointer:
        # Compile graph with persistent checkpointer
        graph = graph_builder.compile(
            checkpointer=checkpointer,
            interrupt_before=["human"],
        )

        # Create SDK with the compiled graph
        sdk = CopilotKitSDK(
            agents=[
                LangGraphAgent(
                    name="quickstart_agent",
                    description="Quickstart agent.",
                    graph=graph,
                ),
            ],
        )

        # Add endpoint
        add_fastapi_endpoint(app, sdk, "/copilotkit")
        yield

app = FastAPI(lifespan=lifespan)

# add new route for health check
@app.get("/health")
def health():
    """Health check."""
    return {"status": "ok"}


def main():
    """Run the uvicorn server."""
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("tutorial_quickstart.demo:app", host="0.0.0.0", port=port)
