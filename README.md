# SpectraScout
SpectraScout is a multi-agent, AI-powered assistant designed to analyze companies, validate job offers, debug and execute code, and help users grow their technical skills. It combines GitHub MCP intelligence, web search, and code-analysis tools to deliver reliable insights, trust scores, and personalized roadmaps.

Key Features

GitHub MCP Integration
Retrieves organization data, repo activity, contributors, engineering quality, and more.

Web Search Intelligence
Uses a dedicated SearchAgent (Wikipedia/Google-compatible) to validate company presence, detect scams, find employee profiles, and cross-check information.

Job & Company Trust Scoring
A multi-stage evaluation system that assigns points based on authenticity, activity, reviews, employee credibility, and overall online footprint.

Code Debugging & Execution
Built-in tools (debug_code and run_code) analyze, fix, and safely execute user code inside an isolated environment.

Personalized Career Roadmaps
Compares the user’s skills and repositories with company tech stacks and generates clear, actionable learning paths.

Day-to-Day Assistance
Simplifies tasks, summarizes content, organizes plans, and explains concepts in a friendly tone.

TO see it in action follow the steps below:
1. Clone this directory.
2. Install all the dependencies: 
   > pip install google-adk, dotenv
3. Create a .env file in the same folder.
4. Get your Gemini API key from https://aistudio.google.com/
5. Get your GitHub Personal Access Token
Go to GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic) → Generate new token with repo access
6. Set the tokens in .env file
7. Create a parent folder at the path where you want to keep SpectraScout and clone the repo within the folder
8. Open the terminal in parent folder and type:
   >adk web