import os
import torch
import sys
sys.path.append('./options')
from AudioReader import AudioReader, write_wav, read_wav
import argparse
from torch.nn.parallel import data_parallel
from Conv_TasNet import ConvTasNet
from utils import get_logger
from option import parse
import tqdm


class Separation():
    def __init__(self, mix_path, yaml_path, model, gpuid=None):
        super(Separation, self).__init__()
        self.mix = read_wav(mix_path)
        opt = parse(yaml_path, is_tain=False)
        net = ConvTasNet(**opt['net_conf'])
        dicts = torch.load(model, map_location='cpu')
        net.load_state_dict(dicts["model_state_dict"])
        self.logger = get_logger(__name__)
        self.logger.info('Load checkpoint from {}, epoch {: d}'.format(model, dicts["epoch"]))
        
        if gpuid:
            self.logger.info("init gpu at", gpuid)
            self.net=net.cuda()
            self.device=torch.device('cuda:{}'.format(
                gpuid[0]) if len(gpuid) > 0 else 'cpu')
            self.gpuid=tuple(gpuid)
        else:
            self.gpuid = []
            self.net=net
            self.device = torch.device("cpu")

    def inference(self, file_path):
        with torch.no_grad():
            egs=self.mix.to(self.device)
            norm = torch.norm(egs,float('inf'))
            if len(self.gpuid) != 0:
                ests=self.net(egs)
                spks=[torch.squeeze(s.detach().cpu()) for s in ests]
            else:
                ests=self.net(egs)
                spks=[torch.squeeze(s.detach()) for s in ests]
            index=0
            for s in spks:
                s = s[:egs.shape[0]]
                #norm
                s = s*norm/torch.max(torch.abs(s))
                index += 1
                
                filename = file_path + '/' + str(index)+".wav"

                self.logger.info("writing to {}".format(filename))
                
                write_wav(filename, s, 8000)
        
        self.logger.info("Compute over {:d} utterances".format(len(self.mix)))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument(
        '-mix_scp', type=str, default='mix.wav', help='Path to mix scp file.')
    parser.add_argument(
        '-yaml', type=str, default='./options/train/train.yml', help='Path to yaml file.')
    parser.add_argument(
        '-model', type=str, default='./Conv-TasNet-non-pit-2/best.pt', help="Path to model file.")
    parser.add_argument(
        '-gpuid', type=str, default='', help='Enter GPU id number')
    parser.add_argument(
        '-save_path', type=str, default='./non-pit-2', help='save result path')
    args=parser.parse_args()
    
    gpuid=None
    if args.gpuid:
        gpuid=[int(i) for i in args.gpuid.split(',')]
    
    separation=Separation(args.mix_scp, args.yaml, args.model, gpuid)
    separation.inference(args.save_path)


if __name__ == "__main__":
    main()