#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from pathlib import Path
import argparse
import json
import tempfile
import subprocess


# In[ ]:


from pysster import Data, Model
from pysster import utils


# In[ ]:


parser = argparse.ArgumentParser()
parser.add_argument('-s', '--seed', type=int, default=None)
parser.add_argument('-o', '--output-dir', default='.')
parser.add_argument('-p', '--params', default=None)
parser.add_argument('--save-model-only', action='store_true', default=False)
parser.add_argument('--tmp-scratch', action='store_true', default=False)
parser.add_argument('--in-fasta', nargs='+')

args = parser.parse_args()

out_path = Path(args.output_dir)


# In[ ]:


# load 'params' dict from json file
if args.params is None:
    params = {}
else:
    with open(args.params) as f:
        params = json.load(f)


# In[ ]:


pysster_data = Data.Data(args.in_fasta, alphabet='ACGT')


with open(str(out_path.joinpath('data_summary.txt')), 'w') as f:
    print(pysster_data.get_summary(), file=f)


# In[ ]:
pysster_model = Model.Model(params, pysster_data, seed=args.seed)


# In[ ]:
pysster_model.train(pysster_data)
utils.save_model(pysster_model, out_path.joinpath('model.pkl'))

# In[ ]:
predictions = pysster_model.predict(pysster_data, "test")
labels = pysster_data.get_labels("test")


# In[ ]:
# write predictions and labels to csv
with open(str(out_path.joinpath('predictions_on-test.csv')), 'w') as f:
    print('label,score_0,score_1,score_2', file=f)
    for label, (s_0, s_1, s_2) in zip(labels, predictions):
        print(f'{label},{s_0},{s_1},{s_2}', file=f)
