import numpy as np

sfilepath = '../wikilarge/train/sources.txt'
tfilepath = 'train/sources.txt'

high = sum(1 for line in open(sfilepath))
size = 10000

sample_ids = np.random.choice(range(high), size, replace=False)

with open(sfilepath) as sfp:
    with open(tfilepath, 'w') as tfp:
        for i, line in enumerate(sfp):
            if i in sample_ids:
                tfp.write(line)


sfilepath = '../wikilarge/train/targets.txt'
tfilepath = 'train/targets.txt'

with open(sfilepath) as sfp:
    with open(tfilepath, 'w') as tfp:
        for i, line in enumerate(sfp):
            if i in sample_ids:
                tfp.write(line)
