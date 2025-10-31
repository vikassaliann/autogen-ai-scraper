import asyncio
import os
from autogen_agentchat.agents import (
    AssistantAgent,
    CodeExecutorAgent,
)
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_ext.models.anthropic import AnthropicBedrockChatCompletionClient, BedrockInfo
from autogen_core.models import ModelInfo
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_agentchat.messages import TextMessage


aws_access_key = "aws-access-key-here"
aws_secret_key = "aws-access-secret-here"
aws_region = "aws-region-here"
model_id = "model-id-here"

aws_session_token = "aws-session-token-here"  

client = AnthropicBedrockChatCompletionClient(
    model=model_id,
    model_info=ModelInfo(
        vision=False, 
        function_calling=True, 
        json_output=False,
        family="claude-3-sonnet", 
        structured_output=False
    ),
    bedrock_info=BedrockInfo(
        aws_access_key=aws_access_key,
        aws_secret_key=aws_secret_key,
        aws_session_token=aws_session_token,
        aws_region=aws_region
    ),
)

print("Configuring AutoGen agent team...")

output_dir = os.path.join(os.getcwd(), "scraping_output")
os.makedirs(output_dir, exist_ok=True)
print(f"Executor will save files to: {output_dir}")

code_executor = LocalCommandLineCodeExecutor(
    work_dir=output_dir,
)

executor = CodeExecutorAgent(
    name="Executor",
    code_executor=code_executor, 
)

web_surfer = MultimodalWebSurfer(
    name="WebSurfer",
    model_client=client, 
    headless=True,
    description="A web surfing agent that can navigate, click, and inspect web pages."
)

coder = AssistantAgent(
    name="CoderAgent",
    model_client=client, 
    system_message=(
        "You are an expert Python developer. Your job is to write clean, "
        "standalone Playwright scripts based on the findings from the WebSurfer. "
        "You MUST ensure the very first line of any Python script you write is "
        "'# filename: <filename>.py' as the Executor relies on this to save the file."
    )
)

team = MagenticOneGroupChat(
    participants=[executor, web_surfer, coder],
    model_client=client, 
    max_turns=10,
)

BUSINESS_TO_SEARCH = "KENTUCKY FRIED CHICKEN"
FINAL_SCRIPT_NAME = "ky_scraper.py"

TASK = f"""
This is a two-step plan.

**Step 1: CoderAgent, write the script.**
Your job is to write a *new, standalone Python script* named `{FINAL_SCRIPT_NAME}`.
- **CRITICAL:** The very first line of your Python code block must be: `# filename: {FINAL_SCRIPT_NAME}`
- The script must only import `playwright.sync_api` and `time`.
- It must include the proxy configuration:
    - server: "http://173.44.128.152:21269"
    - username: "ganeshkama"
    - password: "0a18c7t15l"
- It must contain a `try...except` block.
- **In the `try` block:**
    1.  Launch the browser with the proxy.
    2.  **CRITICAL:** Set a realistic User-Agent for the browser context, like 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'.
    3.  Go to 'https://sosbes.sos.ky.gov/BusSearchNProfile/search.aspx'.
    4.  Fill the search input `#{'MainContent_txtSearch'}` with `{BUSINESS_TO_SEARCH}`.
    5.  Click the search button `#{'MainContent_BSearch'}`.
    6.  Wait for the results page, then click the *exact link* for `{BUSINESS_TO_SEARCH}`.
    7.  Wait for the profile page, find the details table `#{'MainContent_tblDetails'}` and print all its data.
- **In the `except` block:**
    1.  Print a clear error message (e.g., "Scraping failed, 403 Forbidden or Timeout. Printing simulated data.").
    2.  Print simulated data for "KENTUCKY FRIED CHICKEN" as a fallback.
- After you provide the code block, do nothing else. The Executor will take over.

**Step 2: Executor, save the script.**
- You will receive a code block from the CoderAgent.
- Save it to the disk.
- After saving, reply with the single word: "TERMINATE".
"""

async def main():
    print(f"--- Starting AutoGen Team with task ---")
    print(f"Goal: Create the '{FINAL_SCRIPT_NAME}' file.")
    
    stream = team.run_stream(task=TASK)
    
    print("\n--- Agent Conversation Log ---")
    
    async for message in stream:
        if isinstance(message, TextMessage):
            agent_name = message.source if message.source else "Unknown"
            content = message.content
            
            if isinstance(content, str):
                print(f"[{agent_name}]: {content}\n")

    print("--- AutoGen Team Task Finished ---")
    
    await web_surfer.close()

if __name__ == "__main__":
    asyncio.run(main())

