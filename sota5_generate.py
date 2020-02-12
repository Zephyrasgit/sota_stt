#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import subprocess

def run_julius(audio_src, output_dir):
    #helper function to edit file required for Julius input
    def edit_test_dbl(audio_src):
        textpath = "/root/ENVR-v5.4.Dnn.Bin/test.dbl"
        with open(textpath, 'w') as file:
            file.write(audio_src)
        return

    edit_test_dbl(audio_src)
    terminal_command = "/root/julius/julius/julius -C /root/ENVR-v5.4.Dnn.Bin/julius.jconf -dnnconf /root/ENVR-v5.4.Dnn.Bin/dnn.jconf -quiet > " + output_dir + "/julius_stt.txt 2>&1"
    subprocess.call(terminal_command, shell=True)
    return

def run_wav2letter(audio_src, output_dir):
    terminal_command = "/root/wav2letter/build/inference/inference/examples/simple_streaming_asr_example --input_files_base_path ~/model --input_audio_file " + audio_src + " > " + output_dir + "/wav2letter_stt.txt 2>&1"
    subprocess.call(terminal_command, shell=True)
    return

def run_deepspeech(audio_src, output_dir):
    terminal_command = "deepspeech --model /root/deepspeech-0.6.1-models/output_graph.pbmm --lm /root/deepspeech-0.6.1-models/lm.binary --trie /root/deepspeech-0.6.1-models/trie --audio " + audio_src + " > " + output_dir + "/deepspeech_stt.txt 2>&1"
    subprocess.call(terminal_command, shell=True)
    return

def run_pocketsphinx(audio_src, output_dir):
    terminal_command = "cd /root/pocketsphinx-python && python generate_pocketsphinx.py -i " + audio_src + " > " + output_dir + "/pocketsphinx_stt.txt 2>&1 && cd /root"
    subprocess.call(terminal_command, shell=True)
    return

def run_kaldi(audio_src, output_dir):
    def get_kaldi_input_wav(audio_src, output_dir):
        intermediate_file_path = "/root/" + output_dir + "/kaldi_intermediate.wav"
        if os.path.exists(intermediate_file_path):
            os.remove(intermediate_file_path)
        terminal_command = "ffmpeg -loglevel panic -i " + audio_src + " -acodec pcm_s16le -ac 1 -ar 8000 " + output_dir + "/kaldi_intermediate.wav"
        subprocess.call(terminal_command, shell=True)
        return
    
    get_kaldi_input_wav(audio_src, output_dir)
    terminal_command = "cd /root/kaldi/egs/aspire/s5 && online2-wav-nnet3-latgen-faster --online=false --do-endpointing=false --frame-subsampling-factor=3 --config=/root/kaldi/egs/aspire/s5/exp/tdnn_7b_chain_online/conf/online.conf --max-active=7000 --beam=15.0 --lattice-beam=6.0 --acoustic-scale=1.0 --word-symbol-table=/root/kaldi/egs/aspire/s5/exp/tdnn_7b_chain_online/graph_pp/words.txt /root/kaldi/egs/aspire/s5/exp/tdnn_7b_chain_online/final.mdl /root/kaldi/egs/aspire/s5/exp/tdnn_7b_chain_online/graph_pp/HCLG.fst 'ark:echo utterance-id1 utterance-id1|' 'scp:echo utterance-id1 " + output_dir + "/kaldi_intermediate.wav|' 'ark:|lattice-best-path --acoustic-scale=0.1 ark:- ark,t:- | /root/kaldi/egs/aspire/s5/utils/int2sym.pl -f 2- /root/kaldi/egs/aspire/s5/exp/tdnn_7b_chain_online/graph_pp/words.txt' > " + output_dir + "/kaldi_stt.txt 2>&1" + " && rm " + output_dir + "/kaldi_intermediate.wav && cd /root" 
    subprocess.call(terminal_command, shell=True)
    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", type=str, help="Absolute path to audio file", required=True)
    parser.add_argument("-o", "--output-dir", type=str, help="Absolute path to output directory", required=True)
    
    args = parser.parse_args()
    
    audio_src_path = args.input_file
    output_dir = args.output_dir
    
    #create directory if it does not exist
    if not os.path.isdir(output_dir):
        os.mkdir(output_dir)
    
    #julius
    run_julius(audio_src_path, output_dir)
    #deepspeech
    run_deepspeech(audio_src_path, output_dir)
    #kaldi
    run_kaldi(audio_src_path, output_dir)
    #pocketsphinx
    run_pocketsphinx(audio_src_path, output_dir)
    #w2l
    run_wav2letter(audio_src_path, output_dir)
    
    

if __name__ == '__main__':
    main()

