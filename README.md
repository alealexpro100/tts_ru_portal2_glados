# Russian GlaDOS dataset

File [wiki_to_dataset.py](wiki_to_dataset.py) downloads wav files of GlaDOS from portal 2 (except potatos).

Based on [glados-tts](https://github.com/R2D2FISH/glados-tts).


## How to use

### Get dataset

This step needs python3 installed on your system.
Just run `wiki_to_dataset.py`. No additional deps.

### Prepare

Tested on debian bookworm with CUDA card (P104-100).

Steps:
1. Install deps: `sudo apt-get install build-essential python3 python3-dev python3-venv cmake`
2. Build espeak with patches: `./build_espeak.sh` (will ask for `sudo` password).
3. Install espeak pkgs: `(cd deb; apt-get install ./*.deb)`.
4. Build piper: `./build_piper.sh`.

### Train

Read instruction in original repo. Included in this repo script `train.sh` should work.
Do not forget about `tensorboard` for metrics: `tensorboard --logdir lightning_logs`.