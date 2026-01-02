#!/bin/bash

set -ex

if ! [[ -d wav || -f metadata.csv ]]; then
  echo "Dataset not found."
  exit 1
fi

cpkt_url="https://huggingface.co/datasets/rhasspy/piper-checkpoints/resolve/main/ru/ru_RU/irina/medium/epoch%3D4139-step%3D929464.ckpt"
ckpt_path="ru_irina_medium_epoch=4139-step=929464.ckpt"

if ! [[ -f $ckpt_path ]]; then
  wget -O $ckpt_path $cpkt_url
fi

source ./piper1-gpl/.venv/bin/activate

python3 -m piper.train fit \
  --data.voice_name "glados" \
  --data.csv_path metadata.csv \
  --data.audio_dir wav \
  --data.batch_size 16 \
  --model.sample_rate 22050 \
  --data.espeak_voice "ru" \
  --data.cache_dir cache \
  --data.config_path config.json \
  --data.batch_size 16 \
  --trainer.accelerator "gpu" \
  --trainer.max_epochs 1000 \
  --ckpt_path ./$ckpt_path  # optional but highly recommended
