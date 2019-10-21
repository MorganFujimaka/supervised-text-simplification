# Supervised Text Simplification
All code was run in a OS X environment with _Tensorflow 1.8.0_ and _seq2seq_(https://github.com/google/seq2seq) all 
installed and working.

Dataset: _wikilarge_ (https://github.com/louismartin/dress-data/raw/master/data-simplification.tar.bz2).

---
### Data
Set a few data-specific environment variables so that we can easily use them later on:
```
export VOCAB_SOURCE=`pwd`/wikilarge/train/vocab.sources.txt
export VOCAB_TARGET=`pwd`/wikilarge/train/vocab.targets.txt
export TRAIN_SOURCES=`pwd`/wikilarge/train/sources.txt
export TRAIN_TARGETS=`pwd`/wikilarge/train/targets.txt
export DEV_SOURCES=`pwd`/wikilarge/dev/sources.txt
export DEV_TARGETS=`pwd`/wikilarge/dev/targets.txt
export DEV_TARGETS_REF=`pwd`/wikilarge/dev/targets.txt
export NMT_CONFIGS=`pwd`/configs
export TRAIN_STEPS=1000
```

---
### Training
Execute from the _seq2seq_ framework.
```bash
export MODEL_DIR=`pwd`/training
mkdir -p "$MODEL_DIR"

python -m bin.train \
  --config_paths="
      $NMT_CONFIGS/nmt_small.yml,
      $NMT_CONFIGS/train_seq2seq.yml,
      $NMT_CONFIGS/text_metrics_bpe.yml" \
  --model_params "
      vocab_source: $VOCAB_SOURCE
      vocab_target: $VOCAB_TARGET" \
  --input_pipeline_train "
    class: ParallelTextInputPipeline
    params:
      source_files:
        - $TRAIN_SOURCES
      target_files:
        - $TRAIN_TARGETS" \
  --input_pipeline_dev "
    class: ParallelTextInputPipeline
    params:
       source_files:
        - $DEV_SOURCES
       target_files:
        - $DEV_TARGETS" \
  --batch_size 32 \
  --train_steps $TRAIN_STEPS \
  --output_dir "$MODEL_DIR"
```

To monitor the training process, you can start Tensorboard pointing to the output directory:
```
tensorboard --logdir="$MODEL_DIR" --host localhost
```

---
### Making predictions
```bash
export PRED_DIR=${MODEL_DIR}/pred
mkdir -p "$PRED_DIR"

python -m bin.infer \
  --tasks "
    - class: DecodeText" \
  --model_dir "$MODEL_DIR" \
  --input_pipeline "
    class: ParallelTextInputPipeline
    params:
      source_files:
        - $DEV_SOURCES" \
  >  "${PRED_DIR}"/predictions.txt

```
