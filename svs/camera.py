# svs/camera.py
import os
from typing import Optional

import cv2


def capture_image(rtsp_url: str, output_path: str) -> Optional[str]:
    """
    Capture an image from an RTSP camera asynchronously.

    Parameters:
    - rtsp_url (str): The RTSP URL of the camera.
    - output_path (str): The path to save the captured image.

    Returns:
    - Optional[str]: Path to the captured image or None if capturing fails.
    """
    cap = None
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        cap = cv2.VideoCapture(rtsp_url)
        ret, frame = cap.read()

        if ret:
            cv2.imwrite(output_path, frame)
            return output_path
        else:
            return None

    except Exception as e:
        print(f"Error capturing image: {e}")
        return None

    finally:
        if cap is not None:
            cap.release()
