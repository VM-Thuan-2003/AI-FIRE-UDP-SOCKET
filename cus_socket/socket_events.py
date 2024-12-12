from .event_cuda_ai import EventCudaAI


class SocketEvents:
    def __init__(self, sio):
        self.sio = sio
        self.isConnect = False
        self.event_cuda_ai = EventCudaAI()

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
        def cuda_ai(data):
            self.event_cuda_ai.handle_event_cuda_ai(data)
