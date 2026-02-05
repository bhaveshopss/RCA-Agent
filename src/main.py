import os
from dotenv import load_dotenv
from crewai import Crew, Process
from src.agents.rca_agents import RCAAgents
from src.agents.rca_tasks import RCATasks

def main():
    load_dotenv()
    print("RCA Agent Starting...")

    # Define the inputs for the investigation
    # In a real scenario, this would come from an alert payload
    incident_context = {
        'log_group_name': '/aws/lambda/production-api-service',
        'namespace': 'AWS/Lambda',
        'metric_name': 'Errors',
        'dimension_name': 'FunctionName',
        'dimension_value': 'production-api-service',
        'minutes_ago': 60
    }

    # Instantiate Agents and Tasks
    agents = RCAAgents()
    tasks = RCATasks()

    detective = agents.detective_agent()
    auditor = agents.auditor_agent()
    sre = agents.sre_agent()
    remediator = agents.remediation_agent()

    # Create Tasks
    task1 = tasks.gather_logs_metrics_task(detective, incident_context)
    task2 = tasks.audit_changes_task(auditor, incident_context)
    task3 = tasks.root_cause_analysis_task(sre, [task1, task2])
    task4 = tasks.remediation_plan_task(remediator, [task3])

    # Instantiate Crew
    rca_crew = Crew(
        agents=[detective, auditor, sre, remediator],
        tasks=[task1, task2, task3, task4],
        verbose=True, # Adjusted verbose level to int 2 (basic logging)
        process=Process.sequential
    )

    print(f"Starting investigation for: {incident_context}")
    result = rca_crew.kickoff()

    print("\n\n########################")
    print("## RCA Report Generation ##")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    main()
