import json
import os

import boto3
import sentry_sdk
import sys
from geopandas import GeoDataFrame
from sentry_sdk.integrations.aws_lambda import AwsLambdaIntegration

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config import MetricHandler, MetricHandlerException  # noqa
from helpers.logging import get_logger  # noqa
from helpers.util import required_keys  # noqa
from services.location_service import LocationService  # noqa

sns = boto3.client("sns")

SENTRY_DSN = os.environ["SENTRY_DSN"]
SNS_RESULT_TOPIC_ARN = os.environ["SNS_RESULT_TOPIC_ARN"]

sentry_sdk.init(dsn=SENTRY_DSN, integrations=[AwsLambdaIntegration()])  # AWS Lambda integration

logger = get_logger("worker-handler")

fetch_service = LocationService()


def lambda_handler(event, context):
    """
    :param event:  AWS Lambda uses this parameter to pass in event data to the handler.
        For details, see: https://docs.aws.amazon.com/lambda/latest/dg/with-sns.html
    :param context: AWS Lambda uses this parameter to provide runtime information to your handler.
        For details, see: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    :return:
    """
    logger.debug(f"Received event: {event['Records'][0]['Sns']['MessageId']}")

    message = event["Records"][0]["Sns"]["Message"]
    decoded = json.loads(message)

    required_keys(decoded, ["id", "version", "meta.worker.handler"])

    resource_id, version, handler = (
        decoded["id"],
        decoded["version"],
        decoded["meta"]["worker"]["handler"],
    )

    logger.debug(f"Handling event: {handler} for resource: {resource_id} and version: {version}")

    document = fetch_service.get_by_id(
        resource_id=resource_id, select_fields=["id", "geojson", "version", "areaKm2"]
    )  # fetch only required fields;

    required_keys(document, ["id", "geojson", "version", "areaKm2"])

    if version != document["version"]:
        raise ValueError("Version mismatch: document version does not match requested version")

    # resolve the metric handler class
    Handler = MetricHandler.get_handler(handler)
    if Handler is None:
        raise MetricHandlerException(f"No handler configured for: {handler}")

    # instantiate the metric object
    instance = Handler(grid=True, simplify=True, best_effort=False)

    # create a geopandas GeoDataFrame from the geojson shape
    gdf = GeoDataFrame.from_features(document["geojson"]["features"])

    logger.debug(f"Running {instance.slug} computations for resource: {resource_id}")

    # compute the metric
    metric = instance.measure(gdf, area_km2=document["areaKm2"])

    logger.debug(f"Computed {instance.slug} metric for resource: {resource_id} {metric}")

    payload = {
        "slug": instance.slug,
        "location": resource_id,
        "metric": metric._asdict(),  # convert namedtuple to dict
        "version": version,
    }

    required_keys(payload, ["slug", "location", "metric", "version"])

    logger.debug(f"Sending metric result event for {instance.slug} and resource: {resource_id}")

    sns.publish(TopicArn=SNS_RESULT_TOPIC_ARN, Message=json.dumps(payload))

    logger.debug(
        f"Successfully handled event {handler} for resource: {resource_id} and version: {version}"
    )
