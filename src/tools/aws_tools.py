import boto3
from typing import List, Dict, Optional
import os
from datetime import datetime, timedelta

class AWSTools:
    def __init__(self, region_name: str = "us-east-1"):
        self.region_name = region_name
        self.logs_client = boto3.client("logs", region_name=region_name)
        self.cloudwatch_client = boto3.client("cloudwatch", region_name=region_name)
        self.cloudtrail_client = boto3.client("cloudtrail", region_name=region_name)

    def fetch_recent_logs(self, log_group_name: str, minutes_ago: int = 30) -> List[Dict]:
        """
        Fetches logs from a specific log group for the last N minutes.
        """
        print(f"Fetching logs from {log_group_name} for the last {minutes_ago} minutes...")
        start_time = int((datetime.now() - timedelta(minutes=minutes_ago)).timestamp() * 1000)
        end_time = int(datetime.now().timestamp() * 1000)

        try:
            # Using filter_log_events for simplicity, scanning mostly recent events
            response = self.logs_client.filter_log_events(
                logGroupName=log_group_name,
                startTime=start_time,
                endTime=end_time,
                limit=100  # Limit to avoid overwhelming the agent initially
            )
            return response.get("events", [])
        except Exception as e:
            return [{"error": str(e)}]

    def fetch_metrics(self, namespace: str, metric_name: str, dimension_name: str, dimension_value: str, minutes_ago: int = 30) -> List[Dict]:
        """
        Fetches metric statistics for a specific resource.
        """
        print(f"Fetching metrics {namespace}/{metric_name} for {dimension_name}={dimension_value}...")
        start_time = datetime.now() - timedelta(minutes=minutes_ago)
        end_time = datetime.now()

        try:
            response = self.cloudwatch_client.get_metric_statistics(
                Namespace=namespace,
                MetricName=metric_name,
                Dimensions=[
                    {
                        'Name': dimension_name,
                        'Value': dimension_value
                    },
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300, # 5 minute period
                Statistics=['Average', 'Maximum']
            )
            return response.get("Datapoints", [])
        except Exception as e:
            return [{"error": str(e)}]

    def lookup_events(self, minutes_ago: int = 30) -> List[Dict]:
        """
        Looks up CloudTrail events for recent activities.
        """
        print(f"Looking up CloudTrail events for the last {minutes_ago} minutes...")
        start_time = datetime.now() - timedelta(minutes=minutes_ago)
        end_time = datetime.now()

        try:
            response = self.cloudtrail_client.lookup_events(
                StartTime=start_time,
                EndTime=end_time,
                MaxResults=50
            )
            return response.get("Events", [])
        except Exception as e:
            return [{"error": str(e)}]
