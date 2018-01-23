import os, json, urllib
import PyOpenPose as OP
import cv2
import numpy as np

OPENPOSE_ROOT = os.environ["OPENPOSE_ROOT"]

# Optimized for landscape pictures
DEFAULT_NET_WIDTH=368
DEFAULT_NET_HEIGHT=240
DEFAULT_HAND_NET_SIZE=240
DOWNLOAD_HEATMAPS = False
WITH_FACE =  False
WITH_HANDS = True
op = OP.OpenPose((DEFAULT_NET_WIDTH, DEFAULT_NET_HEIGHT), (DEFAULT_HAND_NET_SIZE, DEFAULT_HAND_NET_SIZE), (DEFAULT_NET_WIDTH, DEFAULT_NET_HEIGHT), "COCO",
        OPENPOSE_ROOT + os.sep + "models" + os.sep, 0,
        DOWNLOAD_HEATMAPS,  OP.OpenPose.ScaleMode.ZeroToOne ,
        WITH_FACE,WITH_HANDS)


def handler(context, event):

    output_dict = {}
    
    # extract RGB image from URL
    image_url = event.body.decode('utf-8').strip()
    
    if image_url:
        resp = urllib.urlopen(image_url)
        rgb = np.asarray(bytearray(resp.read()), dtype="uint8")
        rgb = cv2.imdecode(rgb, cv2.IMREAD_COLOR)


        if rgb is not None:

            op.detectPose(rgb)
            op.detectHands(rgb)
                                                        
            output_dict['left_hands'] = op.getKeypoints(op.KeypointType.HAND)[0].tolist()
            output_dict['right_hands'] = op.getKeypoints(op.KeypointType.HAND)[1].tolist()
            output_dict['persons'] = op.getKeypoints(op.KeypointType.POSE)[0].tolist()


    return context.Response(body=json.dumps(output_dict),
            headers={},
            content_type='application/json',
            status_code=200)