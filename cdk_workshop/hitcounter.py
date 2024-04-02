from constructs import Construct
from aws_cdk import (
    aws_lambda as _lambda,
    aws_dynamodb as ddb,
    RemovalPolicy,
)


class HitCounter(Construct):
    @property
    def handler(self):
        return self._handler

    def __init__(self, scope: Construct, id: str, downstream: _lambda.IFunction, **kwargs) -> None:
        super().__init__(scope, id)

        table = ddb.Table(
            self,
            "Hits",
            partition_key={"name": "path", "type": ddb.AttributeType.STRING},
            removal_policy=RemovalPolicy.DESTROY,
        )

        self._handler = _lambda.Function(
            self,
            "HitCounterHandler",
            runtime=_lambda.Runtime.PYTHON_3_9,
            code=_lambda.Code.from_asset("lambda"),
            handler="hitcount.handler",
            environment={"DOWNSTREAM_FUNCTION_NAME": downstream.function_name, "HITS_TABLE_NAME": table.table_name},
        )

        table.grant_read_write_data(self.handler)
        downstream.grant_invoke(self.handler)
