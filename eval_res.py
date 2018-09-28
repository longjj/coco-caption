from pycocotools.coco import COCO
from pycocoevalcap.eval import COCOEvalCap
import matplotlib.pyplot as plt
import json
from json import encoder
import argparse
import os

if __name__=='__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--folder',   type=str,   default='',     help="result_folders")
    args = parser.parse_args()

    annFile='captions_test5k.json'
    coco = COCO(annFile)

    if os.path.isfile(os.path.join(args.folder, 'performance.txt')):
        with open(os.path.join(args.folder, 'performance.txt')) as f:
            content = f.readlines()
            evaledFile = [x.split(' ')[0].strip() for x in content]
    else:
        evaledFile = []

    resFiles = [resFile for resFile in os.listdir(args.folder) if (('.json' in resFile) and (resFile not in evaledFile))]
	
    # Eval all result in the args.folder
    for resFile in resFiles:
        try:
            print('Evaluate: ' + resFile)
            cocoRes = coco.loadRes(os.path.join(args.folder, resFile))
            cocoEval = COCOEvalCap(coco, cocoRes)
            cocoEval.evaluate()
            with open(os.path.join(args.folder, 'performance.txt'), 'a') as fid:
                fid.write(resFile + ' ' + str(cocoEval.eval) + '\n')
        except Exception as e:
            print(e)
            with open(os.path.join(args.folder, 'error.txt'), 'a') as f:
                f.write('============================\n' + resFile + '\n' + str(e) + '\n')
