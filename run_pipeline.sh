#!/bin/sh
if [ -f "$HOME/anaconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/anaconda3/etc/profile.d/conda.sh"
    conda activate MedJarg
elif [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
    conda activate MedJarg
fi

python3  model/simplifier_pipeline.py