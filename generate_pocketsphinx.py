#!/usr/bin/env python
import argparse
import subprocess
from os import environ, path

from pocketsphinx.pocketsphinx import *
from sphinxbase.sphinxbase import *


def generate_transcription(data_dir):

	MODELDIR = "pocketsphinx/model"

	# Create a decoder with certain model
	config = Decoder.default_config()
	config.set_string('-hmm', path.join(MODELDIR, 'en-us/en-us'))
	config.set_string('-lm', path.join(MODELDIR, 'en-us/en-us.lm.bin'))
	config.set_string('-dict', path.join(MODELDIR, 'en-us/cmudict-en-us.dict'))
	decoder = Decoder(config)

	# Decode streaming data.
	decoder = Decoder(config)
	decoder.start_utt()
	stream = open(data_dir, 'rb')
	while True:
		buf = stream.read(1024)
		if buf:
			decoder.process_raw(buf, False, False)
		else:
			break
	decoder.end_utt()
	sentence = [seg.word for seg in decoder.seg()]
	output = ""
	for utt in sentence:
		if utt[0] != "<":
			if utt[-1] == ")":
				output += utt[:-3] + " "
			else:
				output += utt + " "
	print(output[:-1])


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input-file", type=str, help="Absolute path to audio file", required=True)

	args = parser.parse_args()

	audio_src_path = args.input_file

	generate_transcription(audio_src_path)


if __name__ == "__main__":
	main()
