from routing.EndpointExecutor import EndpointExecutor
from security.exceptions.InvalidHeaderException import InvalidHeaderException
from lambda_event import LambdaEvent
from helper.LoggingHelper import LoggingHelper
from response.SetResponses import SetResponses
from routing.endpoint_router import EndpointRouter
from security.UserAuthoriser import UserAuthorizer
from security.exceptions.AuthError import AuthError

logger = LoggingHelper("Handler").retrieve_logger()


def handle(event, context):
    logger.info("Handling")

    # TODO: Remove
    logger.info(event)

    # Gather event information
    try:
        lambda_event = LambdaEvent(event)
    except InvalidHeaderException as e:
        logger.error("Invalid event: " + str(e))
        response = SetResponses.INVALID_REQUEST.value
        logger.info("Response: " + str(response) + "type:" + str(type(response)))
        return response

    # Authenticate User
    try:
        user = UserAuthorizer(lambda_event.get_header()).authorise_user()
    except AuthError as e:
        logger.error(e)
        return SetResponses.UNAUTHENTICATED.value

    # Route request to desired endpoint
    endpoint_executor = EndpointExecutor(user, lambda_event.get_body())
    endpoint_router = EndpointRouter(endpoint_executor, lambda_event.get_request_path())
    response = endpoint_router.route_endpoint()

    if not response or response == {}:
        logger.error("Invalid Response: " + str(response) + ", replacing with server error")
        return SetResponses.INTERNAL_ERROR.value

    return response
