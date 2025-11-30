from google.adk.tools import AgentTool
from google.adk.agents import Agent
from google.adk.tools.mcp_tool.mcp_toolset import (McpToolset, StreamableHTTPConnectionParams)
from google.adk.code_executors import BuiltInCodeExecutor
from google.adk.sessions import InMemorySessionService
from google.adk.runners import InMemoryRunner
from google.adk.tools import google_search
from dotenv import load_dotenv
import os

load_dotenv()
YOUR_GITHUB_AUTH_TOKEN = os.getenv("GITHUB_AUTH_TOKEN")

executor = BuiltInCodeExecutor()


def debug_code(code: str) -> str:
    """
    Analyzes Python code, finds likely errors, and suggests a corrected version.
    """
    import ast

    try:
        ast.parse(code)
        return "No syntax errors detected."
    except SyntaxError as e:
        return f"Syntax Error: {e.msg} at line {e.lineno}, column {e.offset}"

    except Exception as e:
        return f"Unexpected issue: {str(e)}"


def run_code(code: str) -> str:
    """
    Runs Python code inside the ADK sandbox using InBuiltCodeExecutor.
    """
    result = executor.run(code)

    if result.error:
        return f"Runtime Error: {result.error}"
    else:
        return f"Output:\n{result.output}"

SearchAgent = Agent(
    name="SearchAgent",
    model="gemini-2.5-flash",
    instruction="You are a helpful agent that performs simple google searches.",
    description="Use this agent to perform simple google searches.",
    tools=[
        google_search
    ]
)

seeker = AgentTool(agent=SearchAgent)

instruction = """You are a friendly and helpful AI assistant. You can answer general questions, explain ideas,
and help with day-to-day tasks.

You have access to:
- The GitHub MCP server (for checking public GitHub info)
- debug_code (to find bugs in code)
- run_code (to safely execute code)

When asked about a company or job:
STAGE 1 : Check the reputation of the company by using GitHub MCP, web search (via the SearchAgent / google_search), web-scraping, and a summarizer to confirm the company's existence and reviews. Follow the steps below and give points for each step as described (0 -> worst to n -> best).

{
Step 0 - Basics: Scrape the official website of the company offering the job. Give -10 points if it does not exist. Gather vital information such as locations, achievements, reviews, clients, nationality, and details of key employees (LinkedIn profiles, roles).
Step 1 - 10 points: Search (via web search) for any scams or fraud reports related to the company. If you find reports, examine their severity by checking multiple sources and summarizing the findings. If there are criminal recruitment cases or severe, confirmed fraud across reliable sites, flag the response as high-risk, give 0 points for this step, and list the references.
Step 2 - 5 points: Check reviews from current or former employees (e.g., GitHub discussions, public profiles, or other web sources) and rate overall employee sentiment from 1–5.
Step 3 - 5 points: Look for employee complaints or ongoing legal cases between employees and the company. If there's an ongoing case, give 0 points; otherwise rate reputation from 1–5 based on evidence.
}

STAGE 2 : Verify company location and multiple site listings using the official website and supporting web search results (via SearchAgent / google_search). Cross-check locations mentioned on the job posting with addresses found on the official site and via web searches; use map links or authoritative pages found by search to corroborate addresses.
{
Step 1 - 10 points: Confirm the location(s) of the company by comparing the job posting location, official website, and reputable web search results. If location cannot be validated by these sources, give 0 points.
Step 2 - 5 points: Check for other official or authoritative sites (e.g., regional offices, corporate filings, business directories) via web search and give points based on reliability.
}

STAGE 3 : Validity of the company
{
Step 1 - 10 points: Assess company validity by surveying internet presence (official registrations, press coverage, corporate pages) and award points according to the strength of evidence.
Step 2 - 15 points: Check professional contact details of key employees (CEOs, CFOs, COOs, HR, recruiters) listed on the job site. Verify LinkedIn or other professional profiles via web search and summarizer. Give full points if credible profiles exist and clearly tie to the company (strong connections/followers); reduce points if profiles are missing or do not mention the company. Give -20 if no key employees have verifiable professional profiles and flag this strongly in the final report.
}
Summarize the whole report, include the scored breakdown, short reasoning for each score, and 

When given code:
- Use debug_code to identify issues.
- Use run_code to test and show results.

For everything else:
- Answer normally in a friendly tone.
- Help simplify tasks, summarize content, organize plans, and offer useful guidance.

"""

root_agent = Agent(
    name="GithubRepoInfoAgent",
    model="gemini-2.5-flash",
    description="An agent that provides Github repository information from the github API.",
    instruction=instruction,
    tools=[
        McpToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="https://api.githubcopilot.com/mcp/",
                headers={"Authorization": YOUR_GITHUB_AUTH_TOKEN},
                sse_read_timeout=10,
            ),
        ),
        debug_code,
        run_code,
        seeker,
        ],
)

session_service = InMemorySessionService()
runner = InMemoryRunner(agent=root_agent)