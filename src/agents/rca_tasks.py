from crewai import Task

class RCATasks:
    def gather_logs_metrics_task(self, agent, context_data):
        return Task(
            description=f"""
                Analyze the CloudWatch Logs and Metrics for the following resources/time window:
                {context_data}

                1. Fetch logs for the specified log group. Look for ERROR, EXCEPTION, or WARNING patterns.
                2. Fetch key metrics (like CPU, Memory, ErrorCount) if applicable.
                3. Summarize any anomalies found.
            """,
            expected_output="A list of suspicious log lines and abnormal metric datapoints.",
            agent=agent
        )

    def audit_changes_task(self, agent, context_data):
        return Task(
            description=f"""
                Check CloudTrail for any 'Write' events or configuration changes in the last {context_data.get('minutes_ago', 60)} minutes.
                Focus on events related to the resources involved in the incident.
            """,
            expected_output="A list of recent configuration changes or API calls that might be relevant.",
            agent=agent
        )

    def root_cause_analysis_task(self, agent, context_from_tasks):
        return Task(
            description="""
                Review the findings from the Log Analysis and the CloudTrail Audit.
                Correlate the timestamps of errors with configuration changes.
                Determine the most likely root cause of the incident.
                Provide a confidence score (0-100%) for your conclusion.
            """,
            expected_output="A detailed Root Cause Analysis report explaining what happened, why, and the evidence supporting it.",
            agent=agent,
            context=context_from_tasks
        )

    def remediation_plan_task(self, agent, context_from_tasks):
        return Task(
            description="""
                Based on the identified root cause, propose a remediation plan.
                The plan should include:
                1. Immediate actions to mitigate impact.
                2. Long-term fixes to prevent recurrence.
                3. CLI commands or steps to execute the fix if possible.
            """,
            expected_output="A structured remediation plan with actionable steps.",
            agent=agent,
            context=context_from_tasks
        )
