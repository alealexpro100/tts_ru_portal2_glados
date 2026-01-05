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
3. Install espeak pkgs: `sudo apt-get install ./deb/*.deb`.
4. Build piper: `./build_piper.sh`.

### Train

Read instruction in original repo. Included in this repo script `train.sh` should work.
Do not forget about `tensorboard` for metrics: `tensorboard --logdir lightning_logs`. [URL](http://localhost:6007/?pinnedCards=%5B%7B%22plugin%22%3A%22scalars%22%2C%22tag%22%3A%22loss_d%22%7D%2C%7B%22plugin%22%3A%22scalars%22%2C%22tag%22%3A%22loss_g%22%7D%2C%7B%22plugin%22%3A%22scalars%22%2C%22tag%22%3A%22val_loss%22%7D%5D&darkMode=true#timeseries&runSelectionState=eyJ2ZXJzaW9uXzAiOmZhbHNlLCJ2ZXJzaW9uXzEiOmZhbHNlfQ%3D%3D) with pinned metrics.

It becomes listenable after 50-60 epoch and starts to be similar after 200 epoch.

Training example on kaggle: https://www.kaggle.com/code/alexeynasibulin/glados-tts-ru-piper

## Notes

Rules for espeak [here](https://github.com/mitrokun/espeak-ng-data/blob/main/ru_rules) looks good, so it is used for training voice too.