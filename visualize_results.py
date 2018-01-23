#!/usr/bin/python
import sys, json
import urllib, cStringIO
from PIL import Image, ImageDraw
from math import sqrt

# Definition of each skeleleton, as given by OpenPose
BODY_PAIRS = [[1,2],   [1,5],   [2,3],   [3,4],   [5,6],   [6,7],   [1,8],   [8,9],   [9,10],  [1,11],  [11,12], [12,13],  [1,0],   [0,14], [14,16],  [0,15], [15,17],  [2,16],  [5,17]]
HAND_PAIRS = [[0,1],  [1,2],  [2,3],  [3,4],  [0,5],  [5,6],  [6,7],  [7,8],  [0,9],  [9,10],  [10,11],  [11,12],  [0,13],  [13,14],  [14,15],  [15,16],  [0,17],  [17,18],  [18,19],  [19,20]]

# Color identifiers for skeletons
COLOR_IDS=['red','green','blue','orange']

# Where to write image with skeletons
OUTPUT_FILE = 'results.png'


def bone_length(j0,j1):
    return sqrt(pow(j0[0]-j1[0],2) + pow(j0[1]-j1[1],2))

def draw_skeleton(draw,skeleton,skeleton_definition,color_id='red'):
    for bone in skeleton_definition:
        joint0 = tuple(skeleton[bone[0]][:2])
        joint1 = tuple(skeleton[bone[1]][:2])

        # One of the joints is not visible
        if joint0 == (0,0) or joint1 == (0,0):
            continue

        bone_width=int(bone_length(joint0,joint1)/10)
        draw.line(joint0 + joint1, fill=color_id,width=bone_width)

def draw_results(image,results):
    draw = ImageDraw.Draw(image)

    if 'persons' in results:
        for ix,person in enumerate(results['persons']):
            rhand = results['right_hands'][ix]
            lhand = results['left_hands'][ix]

            # For each individual, draw its main skeleton, followed by his hands
            color=COLOR_IDS[ix%len(COLOR_IDS)]
            draw_skeleton(draw,person,BODY_PAIRS,color)
            draw_skeleton(draw,rhand,HAND_PAIRS,color)
            draw_skeleton(draw,lhand,HAND_PAIRS,color)
    
    del draw

def run(image_url,json_results_file):
    
    # Load json data
    body_joint_data = json.load(open(json_results_file,'r'))

    # Load image
    image_fp = cStringIO.StringIO(urllib.urlopen(image_url).read())
    image = Image.open(image_fp)

    draw_results(image,body_joint_data)

    # Save results to a file
    image.save(OUTPUT_FILE)
    print 'Results saved to',OUTPUT_FILE

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print 'Usage:',sys.argv[0],'<Image URL>','<JSON containing joint coordinates>'
        sys.exit(1)
    
    run(sys.argv[1],sys.argv[2])
