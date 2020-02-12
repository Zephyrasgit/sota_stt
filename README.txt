Pre-running requirements:
1. Move generate_pocketsphinx.py into pocketsphinx-python directory, ie.
$ root@8cdea9a869a5:~/sota_stt# mv generate_pocketsphinx.py /root/pocketsphinx-python/

2. Run .sh files in pocketsphinx-python directory for pocketsphinx to work properly
$ root@8cdea9a869a5:~/pocketsphinx-python# . cmd.sh && . path.sh

To run all 5 (Wav2Letter@anywhere, Julius, Kaldi, Deepspeech, Pocketspinx) 
SOTA STTs on a single audio (.wav files only), run the following command 
at the /root directory:

$ root@8cdea9a869a5:~# python sota5_generate.py -i absolute_path_to_audio_file -o absolute_path_to_output_directory

eg: root@8cdea9a869a5:~# python /root/sota_stt/sota5_generate.py -i /root/audio/DR7_FCAU0_SX47_01.wav -o /root/outputs

Expected output should be 5 text files (.txt files) of the output from each of the STT systems.
