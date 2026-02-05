from crewai_tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
from src.tools.aws_tools import AWSTools

# Instantiate the library
aws_tools_lib = AWSTools()

class CloudWatchLogsInput(BaseModel):
    log_group_name: str = Field(..., description="The name of the CloudWatch log group to query.")
    minutes_ago: int = Field(30, description="How many minutes back to search.")

class CloudWatchLogsTool(BaseTool):
    name: str = "CloudWatch Logs Fetcher"
    description: str = "Fetches recent log events from a specified CloudWatch Log Group."
    args_schema: Type[BaseModel] = CloudWatchLogsInput

    def _run(self, log_group_name: str, minutes_ago: int = 30) -> str:
        logs = aws_tools_lib.fetch_recent_logs(log_group_name, minutes_ago)
        return str(logs)

class CloudWatchMetricsInput(BaseModel):
    namespace: str = Field(..., description="The namespace of the metric (e.g., 'AWS/EC2').")
    metric_name: str = Field(..., description="The name of the metric (e.g., 'CPUUtilization').")
    dimension_name: str = Field(..., description="The name of the dimension.")
    dimension_value: str = Field(..., description="The value of the dimension.")

class CloudWatchMetricsTool(BaseTool):
    name: str = "CloudWatch Metrics Fetcher"
    description: str = "Fetches metric statistics from CloudWatch."
    args_schema: Type[BaseModel] = CloudWatchMetricsInput

    def _run(self, namespace: str, metric_name: str, dimension_name: str, dimension_value: str) -> str:
        metrics = aws_tools_lib.fetch_metrics(namespace, metric_name, dimension_name, dimension_value)
        return str(metrics)

class CloudTrailLookupInput(BaseModel):
    minutes_ago: int = Field(30, description="How many minutes back to search for events.")

class CloudTrailLookupTool(BaseTool):
    name: str = "CloudTrail Event Lookup"
    description: str = "Looks up recent CloudTrail management events."
    args_schema: Type[BaseModel] = CloudTrailLookupInput

    def _run(self, minutes_ago: int = 30) -> str:
        events = aws_tools_lib.lookup_events(minutes_ago)
        return str(events)
