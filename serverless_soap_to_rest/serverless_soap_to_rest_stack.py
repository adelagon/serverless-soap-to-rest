import os
from aws_cdk import (
    core as cdk,
    aws_ec2 as ec2,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_ecs as ecs,
    aws_ecs_patterns as ecs_patterns,
    aws_ecr_assets as ecr_assets
)

dirname = os.path.dirname(__file__)

class ServerlessSoapToRestStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        ### ECS Cluster for the example SOAP Server
        vpc = ec2.Vpc(
            self, "VPC",
            max_azs=2
        )
        cluster = ecs.Cluster(
            self, "Cluster",
            vpc=vpc
        )

        ### SOAP Server
        soap_server_asset = ecr_assets.DockerImageAsset(
            self,
            "SoapServerBuildImage",
            directory=os.path.join(dirname, "soap_server")
        )

        soap_server = ecs_patterns.ApplicationLoadBalancedFargateService(
            self, "SoapServer",
            cluster=cluster,
            cpu=1024,
            memory_limit_mib=4096,
            desired_count=2,
            public_load_balancer=True,
            task_image_options={
                "image": ecs.ContainerImage.from_docker_image_asset(soap_server_asset),
                "container_port": 8000,
                "enable_logging": True
            }
        )
        soap_server.target_group.configure_health_check(
            healthy_http_codes="405"
        )
        
        ### SOAP Proxy Lambda Function
        python_layer = _lambda.LayerVersion(
            self,
            "PythonLayer",
            code=_lambda.AssetCode(os.path.join(dirname, "layers/python_layer.zip")),
            compatible_runtimes = [_lambda.Runtime.PYTHON_3_7]
        )
        proxy_function = _lambda.Function(
            self,
            "ProxyFunction",
            code=_lambda.Code.from_asset(os.path.join(dirname, "lambda")),
            handler="proxy_function.handler",
            runtime=_lambda.Runtime.PYTHON_3_7,
            layers=[python_layer],
            timeout=cdk.Duration.seconds(60),
            environment={
                "SOAP_ENDPOINT": "http://{}".format(soap_server.load_balancer.load_balancer_dns_name)
            }
        )

        ### API Gateway
        api = apigw.LambdaRestApi(
            self, "RestEndpoint",
            handler=proxy_function,
            proxy=False
        )

        cars = api.root.add_resource("cars")
        cars.add_method("POST")
