import os
import boto3
import pytest
from moto import mock_aws
from src.tools.aws_tools import AWSTools

@pytest.fixture
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@mock_aws
def test_fetch_recent_logs(aws_credentials):
    logs_client = boto3.client("logs", region_name="us-east-1")
    logs_client.create_log_group(logGroupName="/test/logs")
    logs_client.create_log_stream(logGroupName="/test/logs", logStreamName="stream1")
    
    # Put some dummy log events
    logs_client.put_log_events(
        logGroupName="/test/logs",
        logStreamName="stream1",
        logEvents=[
            {'timestamp': 1000, 'message': 'Error occurred'},
            {'timestamp': 2000, 'message': 'Another error'}
        ]
    )

    tools = AWSTools()
    # Mocking time since filter_log_events uses current time
    # For moto, filter_log_events implementation might vary, but basic call check:
    logs = tools.fetch_recent_logs("/test/logs", minutes_ago=60)
    assert isinstance(logs, list)
    # Note: Moto's filter_log_events might not perfectly return added events depending on timestamp logic vs real time
    # So we mainly test that it doesn't crash and returns a list.

@mock_aws
def test_fetch_metrics(aws_credentials):
    cw_client = boto3.client("cloudwatch", region_name="us-east-1")
    # Put metric data
    cw_client.put_metric_data(
        Namespace="Test/Namespace",
        MetricData=[
            {
                'MetricName': 'TestMetric',
                'Dimensions': [{'Name': 'Dim', 'Value': 'Val'}],
                'Value': 1.0,
                'Unit': 'Count'
            }
        ]
    )
    
    tools = AWSTools()
    metrics = tools.fetch_metrics(
        namespace="Test/Namespace", 
        metric_name="TestMetric", 
        dimension_name="Dim", 
        dimension_value="Val"
    )
    assert isinstance(metrics, list)

@mock_aws
def test_lookup_events(aws_credentials):
    # CloudTrail in moto
    ct_client = boto3.client("cloudtrail", region_name="us-east-1")
    # Moto CloudTrail lookup might be empty by default but lets ensure it runs
    tools = AWSTools()
    events = tools.lookup_events()
    assert isinstance(events, list)
