from crewai import Agent
from langchain_google_genai import ChatGoogleGenerativeAI
from src.tools.crew_tools import CloudWatchLogsTool, CloudWatchMetricsTool, CloudTrailLookupTool
import os

class RCAAgents:
    def __init__(self):
        # Initialize Gemini LLM
        # Ensure GOOGLE_API_KEY is in environment variables
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            verbose=True,
            temperature=0.5,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

    def detective_agent(self):
        return Agent(
            role='Cloud Detective',
            goal='Investigate anomalies in logs and metrics to find evidence of failure.',
            backstory='You are an expert Cloud Log Analyst. Your job is to sift through mountains of logs and metrics to find the needle in the haystack that explains a failure.',
            tools=[CloudWatchLogsTool(), CloudWatchMetricsTool()],
            verbose=True,
            memory=True,
            llm=self.llm
        )

    def auditor_agent(self):
        return Agent(
            role='Cloud Auditor',
            goal='Identify configuration changes or security events that could have caused the issue.',
            backstory='You are a meticulous Cloud Auditor. You track every change in the environment. You believe that "it was working yesterday, so someone must have changed something".',
            tools=[CloudTrailLookupTool()],
            verbose=True,
            memory=True,
            llm=self.llm
        )

    def sre_agent(self):
        return Agent(
            role='Site Reliability Engineer (SRE)',
            goal='Synthesize findings from the Detective and Auditor to determine the Root Cause.',
            backstory='You are a seasoned SRE. You take raw data from investigations and correlate it to form a coherent theory of what went wrong and why.',
            verbose=True,
            memory=True,
            allow_delegation=True,
            llm=self.llm
        )

    def remediation_agent(self):
        return Agent(
            role='Remediation Specialist',
            goal='Propose a safe and effective plan to fix the root cause.',
            backstory='You are a cautious engineer who focuses on fixing systems without causing further damage. You provide step-by-step remediation plans.',
            verbose=True,
            memory=True,
            llm=self.llm
        )
