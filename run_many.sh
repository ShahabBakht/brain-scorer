#!/bin/bash

models=(simmousenet)
max_layer=(11)
width=(64)
for subject in s1;
    do
    for i in "${!models[@]}";
    do
        for layer in $(seq 0 1 "${max_layer[$i]}");
        do
            python train_fmri_convex.py \
                --exp_name 20210108 \
                --layer "$layer" \
                --features "${models[$i]}" \
                --subject "$subject" \
                --width "${width[$i]}" \
                --simmousenet_path /network/tmp1/bakhtias/Results/log_simmousenet_seed10_h1p4_largeRF/ucf101-64_rsenet_dpc-rnn_bs30_lr0.001_seq8_pred3_len5_ds3_train-all/model/epoch100.pth.tar \
                --data_root /network/tmp1/bakhtias/crcns/
                
        done
    done
done