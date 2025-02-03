# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

from pathlib import Path
from typing import Optional, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)


class KinesisStreamConsumerProperties(TypedDict):
    ConsumerName: Optional[str]
    StreamARN: Optional[str]
    ConsumerARN: Optional[str]
    ConsumerCreationTimestamp: Optional[str]
    ConsumerStatus: Optional[str]
    Id: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class KinesisStreamConsumerProvider(ResourceProvider[KinesisStreamConsumerProperties]):
    TYPE = "AWS::Kinesis::StreamConsumer"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[KinesisStreamConsumerProperties],
    ) -> ProgressEvent[KinesisStreamConsumerProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - ConsumerName
          - StreamARN

        Create-only properties:
          - /properties/ConsumerName
          - /properties/StreamARN

        Read-only properties:
          - /properties/ConsumerStatus
          - /properties/ConsumerARN
          - /properties/ConsumerCreationTimestamp
          - /properties/Id



        """
        model = request.desired_state
        kinesis = request.aws_client_factory.kinesis

        if not request.custom_context.get(REPEATED_INVOCATION):
            # this is the first time this callback is invoked
            # TODO: idempotency

            response = kinesis.register_stream_consumer(
                StreamARN=model["StreamARN"], ConsumerName=model["ConsumerName"]
            )
            model["ConsumerARN"] = response["Consumer"]["ConsumerARN"]
            model["ConsumerStatus"] = response["Consumer"]["ConsumerStatus"]
            request.custom_context[REPEATED_INVOCATION] = True
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )

        response = kinesis.describe_stream_consumer(ConsumerARN=model["ConsumerARN"])
        model["ConsumerStatus"] = response["ConsumerDescription"]["ConsumerStatus"]
        if model["ConsumerStatus"] == "CREATING":
            return ProgressEvent(
                status=OperationStatus.IN_PROGRESS,
                resource_model=model,
                custom_context=request.custom_context,
            )
        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[KinesisStreamConsumerProperties],
    ) -> ProgressEvent[KinesisStreamConsumerProperties]:
        """
        Fetch resource information


        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[KinesisStreamConsumerProperties],
    ) -> ProgressEvent[KinesisStreamConsumerProperties]:
        """
        Delete a resource


        """
        model = request.desired_state
        kinesis = request.aws_client_factory.kinesis
        kinesis.deregister_stream_consumer(ConsumerARN=model["ConsumerARN"])

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[KinesisStreamConsumerProperties],
    ) -> ProgressEvent[KinesisStreamConsumerProperties]:
        """
        Update a resource


        """
        raise NotImplementedError
