import argparse
import yaml

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, help='name or path of your configuration file', required=True)
    parser.add_argument('--common', type=str, help='path to common config', required=False)
    parser.add_argument('--common2', type=str, help='path to second common config', required=False)
    parser.add_argument('--nep_token', type=str, help='path to second common config', required=False)
    args = parser.parse_args()
    return args

def get_conf(args):
    conf = {}
    with open(args.config, 'r') as f:
        conf.update(yaml.safe_load(f))
    if args.common:
        with open(args.common, 'r') as f:
            conf.update(yaml.safe_load(f))
    if args.common2:
        with open(args.common2, 'r') as f:
            conf.update(yaml.safe_load(f))
    if args.nep_token:
        with open(args.nep_token, 'r') as f:
            conf.update(yaml.safe_load(f))
    
    return conf