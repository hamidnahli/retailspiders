from urllib.parse import urlparse
import boto3
import botocore.exceptions
from requests.adapters import HTTPAdapter
import concurrent.futures
from random import choice, randint
from time import sleep
import ipaddress
import requests

from items.debugging import app_logger as log

# import http
#
# http.client.HTTPConnection.debuglevel = 2

MAX_IPV4 = ipaddress.IPv4Address._ALL_ONES

# Region lists that can be imported and used in the ApiGateway class
DEFAULT_REGIONS = [
    # "us-west-1",
    # "us-west-2",
    # "us-east-1",
    "us-east-2",
    # "eu-west-1",
    # "eu-west-2",
    # "eu-west-3",
    # "eu-north-1",
    # "eu-central-1",
    # "ca-central-1",
    # "ap-south-1",
    # "ap-southeast-2",
    # "ap-northeast-1",
]

EXTRA_REGIONS = DEFAULT_REGIONS + [
    "ap-south-1", "ap-northeast-3", "ap-northeast-2",
    "ap-southeast-1", "ap-southeast-2", "ap-northeast-1",
    "sa-east-1"
]

# These regions require manual opt-in from AWS
ALL_REGIONS = EXTRA_REGIONS + [
    "ap-east-1", "af-south-1", "eu-south-1", "me-south-1"
]

USER_AGENTS = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2919.83 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A',
    'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19577',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16.2',
    'Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.14.1) Presto/2.12.388 Version/12.16'
]


# Inherits from HTTPAdapter so that we can edit each request before sending
class ApiGateway(HTTPAdapter):
    api_id = None

    def __init__(self, site, regions=DEFAULT_REGIONS, access_key_id=None, access_key_secret=None, **kwargs):
        super().__init__(**kwargs)
        # Set simple params from constructor
        if site.endswith("/"):
            self.site = site[:-1]
        else:
            self.site = site
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.api_name = site + " - IP Rotate API"
        self.regions = regions

    # Enter and exit blocks to allow "with" clause
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.shutdown()

    def send(self, request, stream=False, timeout=None, verify=True, cert=None, proxies=None):
        # Get random endpoint
        endpoint = choice(self.endpoints)
        # Replace URL with our endpoint
        protocol, site = request.url.split("://", 1)
        site_path = site.split("/", 1)[1]
        request.url = "https://" + endpoint + "/ProxyStage/" + site_path
        # Replace host with endpoint host
        request.headers["Host"] = endpoint
        # Auto generate random X-Forwarded-For if doesn't exist.
        # Otherwise AWS forwards true IP address in X-Forwarded-For header
        x_forwarded_for = request.headers.get("X-Forwarded-For")
        if x_forwarded_for is None:
            x_forwarded_for = ipaddress.IPv4Address._string_from_ip_int(randint(0, MAX_IPV4))
        # Move "X-Forwarded-For" to "X-My-X-Forwarded-For". This then gets converted back
        # within the gateway.
        request.headers.pop("X-Forwarded-For", None)
        request.headers["X-My-X-Forwarded-For"] = x_forwarded_for
        # Run original python requests send function
        return super().send(request, stream, timeout, verify, cert, proxies)

    def init_gateway(self, region, force=False):
        # Init client
        session = boto3.session.Session()
        awsclient = session.client(
            "apigateway",
            region_name=region,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.access_key_secret
        )
        # If API gateway already exists for host, return pre-existing endpoint
        if not force:
            try:
                current_apis = ApiGateway.get_gateways(awsclient)
            except botocore.exceptions.ClientError as e:
                if e.response["Error"]["Code"] == "UnrecognizedClientException":
                    log.warning(f"Could not create region (some regions require manual enabling): {region}")
                    return {
                        "success": False
                    }
                else:
                    raise e

            for api in current_apis:
                if "name" in api and self.api_name == api["name"]:
                    return {
                        "success": True,
                        "endpoint": f"{api['id']}.execute-api.{region}.amazonaws.com",
                        "new": False
                    }

        # Create simple rest API resource
        create_api_response = awsclient.create_rest_api(
            name=self.api_name,
            endpointConfiguration={
                "types": [
                    "REGIONAL",
                ]
            }
        )

        # Get ID for new resource
        get_resource_response = awsclient.get_resources(
            restApiId=create_api_response["id"]
        )
        rest_api_id = create_api_response["id"]
        self.api_id = rest_api_id
        # Create "Resource" (wildcard proxy path)
        create_resource_response = awsclient.create_resource(
            restApiId=create_api_response["id"],
            parentId=get_resource_response["items"][0]["id"],
            pathPart="{proxy+}"
        )

        # Allow all methods to new resource
        awsclient.put_method(
            restApiId=create_api_response["id"],
            resourceId=get_resource_response["items"][0]["id"],
            httpMethod="ANY",
            authorizationType="NONE",
            requestParameters={
                "method.request.path.proxy": True,
                "method.request.header.X-My-X-Forwarded-For": True
            }
        )

        # Make new resource route traffic to new host
        awsclient.put_integration(
            restApiId=create_api_response["id"],
            resourceId=get_resource_response["items"][0]["id"],
            type="HTTP_PROXY",
            httpMethod="ANY",
            integrationHttpMethod="ANY",
            uri=self.site,
            connectionType="INTERNET",
            requestParameters={
                "integration.request.path.proxy": "method.request.path.proxy",
                "integration.request.header.X-Forwarded-For": "method.request.header.X-My-X-Forwarded-For"
            }
        )

        awsclient.put_method(
            restApiId=create_api_response["id"],
            resourceId=create_resource_response["id"],
            httpMethod="ANY",
            authorizationType="NONE",
            requestParameters={
                "method.request.path.proxy": True,
                "method.request.header.X-My-X-Forwarded-For": True
            }
        )

        awsclient.put_integration(
            restApiId=create_api_response["id"],
            resourceId=create_resource_response["id"],
            type="HTTP_PROXY",
            httpMethod="ANY",
            integrationHttpMethod="ANY",
            uri=f"{self.site}/{{proxy}}",
            connectionType="INTERNET",
            requestParameters={
                "integration.request.path.proxy": "method.request.path.proxy",
                "integration.request.header.X-Forwarded-For": "method.request.header.X-My-X-Forwarded-For"
            }
        )

        # Creates deployment resource, so that our API to be callable
        awsclient.create_deployment(
            restApiId=rest_api_id,
            stageName="ProxyStage"
        )

        # Return endpoint name and whether it show it is newly created
        return {
            "success": True,
            "endpoint": f"{rest_api_id}.execute-api.{region}.amazonaws.com",
            "new": True
        }

    @staticmethod
    def get_gateways(client):
        gateways = []
        position = None
        complete = False
        while not complete:
            if isinstance(position, str):
                gateways_response = client.get_rest_apis(
                    limit=500,
                    position=position
                )
            else:
                gateways_response = client.get_rest_apis(
                    limit=500
                )

            gateways.extend(gateways_response['items'])

            position = gateways_response.get('position', None)
            if position is None:
                complete = True

        return gateways

    def delete_gateway(self, region, endpoints=None):
        # Create client
        session = boto3.session.Session()
        awsclient = session.client('apigateway',
                                   region_name=region,
                                   aws_access_key_id=self.access_key_id,
                                   aws_secret_access_key=self.access_key_secret
                                   )
        # Extract endpoint IDs from given endpoints
        endpoint_ids = []
        if endpoints is not None:
            for endpoint in endpoints:
                endpoint_ids.append(endpoint.split(".")[0])
        # Get all gateway apis (or skip if we don't have permission)
        try:
            apis = ApiGateway.get_gateways(awsclient)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "UnrecognizedClientException":
                return 0
        # Delete APIs matching target name
        api_iter = 0
        deleted = []
        while api_iter < len(apis):
            api = apis[api_iter]
            # Check if hostname matches
            if "name" in api and self.api_name == api["name"]:
                # Attempt delete
                try:
                    # If endpoints list is given, only delete if within list
                    if endpoints is not None and api["id"] not in endpoint_ids:
                        api_iter += 1
                        continue
                    success = awsclient.delete_rest_api(restApiId=api["id"])
                    if success:
                        deleted.append(api["id"])
                    else:
                        log.warning(f"Failed to delete API {api['id']}.")
                except botocore.exceptions.ClientError as e:
                    # If timeout, retry
                    err_code = e.response["Error"]["Code"]
                    if err_code == "TooManyRequestsException":
                        sleep(1)
                        continue
                    else:
                        log.warning(f"Failed to delete API {api['id']}.")
            api_iter += 1
        return deleted

    def start(self, force=False, endpoints=[]):
        # If endpoints given already, assign and continue
        if len(endpoints) > 0:
            self.endpoints = endpoints
            return endpoints

        # Otherwise, start/locate new endpoints
        log.info(f"Starting an API gateway in {self.regions} regions.")
        self.endpoints = []
        new_endpoints = 0

        # Setup multithreading object
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            # Send each region creation to its own thread
            for region in self.regions:
                futures.append(executor.submit(self.init_gateway, region=region, force=force))
            # Get thread outputs
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result["success"]:
                    self.endpoints.append(result["endpoint"])
                    if result["new"]:
                        new_endpoints += 1

        log.info(f"Using endpoint {self.api_id} for {self.site}")
        return self.endpoints

    def shutdown(self, endpoints=None):
        log.info(f"Deleting gateway for site '{self.site}'.")
        futures = []
        # Setup multithreading object
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            # Send each region deletion to its own thread
            for region in self.regions:
                futures.append(executor.submit(self.delete_gateway, region=region, endpoints=endpoints))
            # Check outputs
            deleted = []
            for future in concurrent.futures.as_completed(futures):
                deleted += future.result()
        log.info(f"Deleted endpoint {self.api_id} for site '{self.site}'.")
        return deleted


global_headers = {
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Google Chrome";v="96"',
    'sec-ch-ua-mobile': '?0',
    'user-agent': choice(USER_AGENTS),
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,ar;q=0.8,fr;q=0.7,de;q=0.6',
}


def make_request(url, headers=False):
    domain = urlparse(url).netloc
    # Create gateway object and initialise in AWS
    gateway = ApiGateway('https://' + domain)
    gateway.start()
    # Assign gateway to session
    session = requests.Session()
    session.mount('https://' + domain, gateway)
    if headers:
        response = session.get(url, headers=global_headers)
    else:
        response = session.get(url)
    gateway.shutdown()
    return response


def start_session(url):
    domain = urlparse(url).netloc
    # Create gateway object and initialise in AWS
    gateway = ApiGateway('https://' + domain)
    gateway.start()
    # Assign gateway to session
    session = requests.Session()
    session.mount('https://' + domain, gateway)
    return gateway, session
