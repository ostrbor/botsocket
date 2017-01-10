import pickle
from .commandbus import Bus
from .exceptions import BotSocketBaseException


def handle_request(binary_request):
    """: binary_request : -> binary_response """
    command = pickle.loads(binary_request)
    bus = Bus()
    try:
        result = bus.execute(command)
    except BotSocketBaseException as e:
        response = '500: ' + str(e)
    else:
        msg = result if result else 'None'
        response = '200: ' + msg
    return pickle.dumps(response)
