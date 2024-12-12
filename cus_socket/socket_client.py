import socketio  # type: ignore
from .socket_events import SocketEvents

"""
SocketIO client for communicating with the server.

This class provides a simple interface for connecting to the server,
sending messages, and receiving events.

Example usage:

    client = SocketClient('http://localhost:5000')
    client.connect()
    client.send_message('web', 'drone', 'droneStatus', 'Hello, server!')

Attributes:
    server_url (str): The URL of the server to connect to.
    isConnect (bool): Whether the client is currently connected to the server.
    socket_events (SocketEvents): The events handler for the client.
"""


class SocketClient:
    def __init__(self, server_url):
        """
        Initialize the SocketIO client.

        Args:
            server_url (str): The URL of the server to connect to.
        """
        self.sio = socketio.Client()
        self.server_url = server_url
        self.isConnect = False

        self.socket_events = SocketEvents(self.sio)

        self.socket_events.register_events()

    def connect(self):
        """
        Connect to the server.

        If the connection is successful, the `isConnect` attribute will be set
        to `True`. Otherwise, an error message will be printed.
        """
        try:
            self.sio.connect(self.server_url)
            self.isConnect = True
            self.sio.wait()  # Keep the socket running
        except socketio.exceptions.ConnectionError:
            print("Error connecting to server")

    def disconnect(self):
        """
        Disconnect from the server.

        If the client is connected, this method will disconnect the client
        and set the `isConnect` attribute to `False`.
        """
        self.sio.disconnect()
        self.isConnect = False

    def send_message(self, stream, direction, header, data, status=None):
        """
        Send a message to the server.

        Args:
            stream (str): The stream to send the message to.
            direction (str): The direction of the message (e.g. 'web' or 'drone').
            header (str): The header of the message.
            data (object): The data to send in the message.
            status (str, optional): The status of the message (e.g. 'ok' or 'error').

        The message will be sent as a SocketIO event with the name 'message'.
        The event data will be a dictionary with the following keys:

        - `stream`: The stream to send the message to.
        - `direction`: The direction of the message (e.g. 'web' or 'drone').
        - `header`: The header of the message.
        - `data`: The data to send in the message.
        - `status`: The status of the message (e.g. 'ok' or 'error').
        """
        self.sio.emit(
            stream,
            {"direction": direction, "header": header, "data": data, "status": status},
        )
