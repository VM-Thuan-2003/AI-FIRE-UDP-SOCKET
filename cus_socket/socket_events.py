from .event_drone import EventDrone


class SocketEvents:
    def __init__(self, sio):
        self.sio = sio
        self.isConnect = False
        self.event_drone = EventDrone()

    def register_events(self):
        @self.sio.event
        def connect():
            self.isConnect = True
            print(f"Connected to server, {self.isConnect}")

        @self.sio.event
        def disconnect():
            self.isConnect = False
            print(f"Disconnected from server, {self.isConnect}")

        @self.sio.event
        def connect_error(data):
            print(f"Failed to connect to server: {data}")

        @self.sio.event
        def drone(data):
            self.event_drone.handle_event_drone(data)
