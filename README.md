# AI Fire Detection System

## Overview

This project is designed for real-time fire detection using video input. It utilizes UDP sockets for video streaming and a pre-trained model for fire detection.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/VM-Thuan-2003/AI-FIRE-UDP-SOCKET.git
   cd AI-FIRE-UDP-SOCKET
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the fire detection system, execute the following command:

```bash
python main.py
```

The system will start streaming video from the configured UDP source and display the detection output in a window.

## Examples

### Real-time Detection

Run the system and observe how it detects fire in the video stream. The output will show two windows: one with the original video and another with detection annotations.

### Configuration

You can configure the video source and detection parameters in the `main.py` script to suit your needs.

## Contributing

To contribute to this project, please fork the repository and submit a pull request. For any issues, feel free to open an issue on GitHub.

## License

This project is licensed under the terms of the [MIT License](LICENSE).

## Acknowledgments

Special thanks to the contributors of the libraries and tools used in this project, including OpenCV and PyTorch.
