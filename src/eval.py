
import pickle
import tensorflow as tf
import cv2, os
import numpy as np
import time
import logging
import argparse
import json, re
from tensorflow.python.client import timeline
from tqdm import tqdm
from common import  CocoPairsRender, read_imgfile, CocoColors
from estimator import PoseEstimator , TfPoseEstimator
from networks import get_network
from pose_dataset import CocoPose
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

config = tf.ConfigProto()
config.gpu_options.allocator_type = 'BFC'
config.gpu_options.per_process_gpu_memory_fraction = 0.95
config.gpu_options.allow_growth = True

def round_int(val):
    return int(round(val))
    
def write_coco_json(human, image_w, image_h):
    keypoints = []
    transform_list = [0, 15, 14, 17, 16, 5, 2, 6, 3, 7, 4, 11, 8, 12, 9, 13, 10]
    #transform_list = list(range(18))
    for i in transform_list:
        if i not in human.body_parts.keys():
            # keypoints.extend([image_w/2, image_h/2, 0])
            keypoints.extend([0, 0, 0])
            continue
        body_part = human.body_parts[i]
        keypoints.extend([round_int(body_part.x * image_w), round_int(body_part.y * image_h), 2])
    return keypoints

def compute_oks(keypoints, anns):
    sigmas = np.array([.26, .25, .25, .35, .35, .79, .79, .72, .72, .62, .62, 1.07, 1.07, .87, .87, .89, .89]) / 10.0
    vars = (sigmas * 2) ** 2
    max_score = 0
    max_visible = []
    for ann in anns:
        score = 0
        gt = ann['keypoints']
        visible = gt[2::3]
        if np.sum(visible) == 0:
            continue
        else:
            gt_point = np.array([(x, y) for x , y in zip(gt[0::3], gt[1::3])])
            pred = np.array([(x, y) for x , y in zip(keypoints[0::3], keypoints[1::3])])
            # import pdb; pdb.set_trace()
            dist = (gt_point - pred) ** 2
            dist = np.sum(dist, axis=1)
            sp = (ann['area'] + np.spacing(1))

        dist[visible == 0] = 0.0
        # dist[visible_pred == 0] = 0.0
        score = np.exp(-dist / vars / 2.0 / sp)

        score = np.mean(score)
        if max_score < score:
            max_score = score
            max_visible = visible
    return max_score, max_visible


def compute_ap(score, threshold =0.5):
    b =  [ 1 if x > threshold else 0 for x in score]
    return np.sum(b)/1.0/len(score)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tensorflow Openpose Inference')
    parser.add_argument('--imgpath', type=str, default='./images/p2.jpg')
    parser.add_argument('--input-width', type=int, default=368)
    parser.add_argument('--input-height', type=int, default=368)
    parser.add_argument('--stage-level', type=int, default=6)
    parser.add_argument('--model', type=str, default='mobilenet_thin', help='mobilenet_original / mobilenet_thin')
    parser.add_argument('--image_dir', type=str, default='/home/zaikun/hdd/data/keypoint/val2017/')
    parser.add_argument('--coco_json_file', type = str, default = '/home/zaikun/hdd/data/keypoint/annotations/person_keypoints_val2017.json')
    parser.add_argument('--display', type=bool, default=False)
    args = parser.parse_args()
    write_json = 'json/%s_%d_%d.json' %(args.model, args.input_width, args.input_height)

    annType = ['segm', 'bbox', 'keypoints']
    annType = annType[2]
    cocoGt = COCO(args.coco_json_file)
    keys = list(cocoGt.imgs.keys())
    catIds = cocoGt.getCatIds(catNms = ['person'])
    imgIds = cocoGt.getImgIds(catIds = catIds)
    keys = list(cocoGt.imgs.keys())

    if not os.path.exists(write_json):
        input_node = tf.placeholder(tf.float32, shape=(1, args.input_height, args.input_width, 3), name='image')
        fp = open(write_json, 'w')
        result = []
        
        with tf.Session(config=config) as sess:
            net, _, last_layer = get_network(args.model, input_node, sess)
            for i, image_id in enumerate(tqdm(keys)):
                #image_id = int(getLastName(img))
                img_meta = cocoGt.imgs[image_id]
                img_idx = img_meta['id']
                ann_idx = cocoGt.getAnnIds(imgIds=image_id)
                anns = cocoGt.loadAnns(ann_idx)

                item = {
                    'image_id':1,
                    'category_id':1,
                    'keypoints':[],
                    'score': 0.0
                }
                img_name = args.image_dir +  '%012d.jpg' % image_id
                image = read_imgfile(img_name, args.input_width, args.input_height)
                run_options = tf.RunOptions(trace_level=tf.RunOptions.FULL_TRACE)
                run_metadata = tf.RunMetadata()
                pafMat, heatMat = sess.run(
                    [
                        net.get_output(name=last_layer.format(stage=args.stage_level, aux=1)),
                        net.get_output(name=last_layer.format(stage=args.stage_level, aux=2))
                    ], feed_dict={'image:0': [image]}, options=run_options, run_metadata=run_metadata
                )
                heatMat, pafMat = heatMat[0], pafMat[0]
                humans = PoseEstimator.estimate(heatMat, pafMat)
   
                for human in humans :
                    #import pdb; pdb.set_trace();
                    res = write_coco_json(human, img_meta['width'], img_meta['height'])
                    item['keypoints'] = res
                    item['image_id'] = image_id
                    item['score'] , visible = compute_oks(res, cocoGt.loadAnns(ann_idx))
                    if len(visible) != 0:
                        for vis in range(17):
                            item['keypoints'][3* vis + 2] = visible[vis]
                        result.append(item)

        json.dump(result,fp)
        fp.close()

    cocoDt = cocoGt.loadRes(write_json)
    cocoEval = COCOeval(cocoGt, cocoDt, annType)
    cocoEval.params.imgIds = keys
    cocoEval.params.catIds = [1]
    cocoEval.evaluate()
    cocoEval.accumulate()
    cocoEval.summarize()

    pred = json.load(open(write_json, 'r'))
    print('AP50')
    scores = [ x['score'] for x in pred]
    ap50 = compute_ap(scores, 0.5)
    print('ap50 is %f' % ap50)
    ap = 0
    for i in np.arange(0.5,1, 0.05).tolist():
        ap = ap + compute_ap(scores, i)
    ap = ap / len(np.arange(0.5, 1 , 0.05).tolist())
    print('ap is %f' % ap)
