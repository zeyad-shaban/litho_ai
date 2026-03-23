import numpy as np
from sensor_msgs.msg import Image

def imgmsg_to_cv2(msg: Image):
    return np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, 3)