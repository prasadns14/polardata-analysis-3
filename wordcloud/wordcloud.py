from tika import parser, language
from nltk import pos_tag,word_tokenize,FreqDist
import argparse 
import os 
import fnmatch
import json
from pandas import read_table

def get_sweet_words():
	sweet_data = read_table("sweet_ontology.tsv",header=None,error_bad_lines=False)
	return [x[1][0] for x in sweet_data.iterrows() if x[1][1] != 'O']

def get_nouns(text):
	words = [x[0].lower() for x in pos_tag(word_tokenize(text)) if x[1] in noun_tags and x[0] in sweet_words]
	if words:
		return words[:30]
	else:
		return []

def load_topics(filename):
	languages.append(language.from_file(filename))
	parser_obj = parser.from_file(filename)
	if 'content' in parser_obj and parser_obj['content']:
		words.extend(get_nouns(parser_obj['content']))
	if 'metadata' in parser_obj:
		metadata_dict = parser_obj['metadata']
		if 'Author' in metadata_dict:
			if type(metadata_dict['Author']) == type([]):
				metadata.append(metadata_dict['Author'][0])
			else:	
				metadata.append(metadata_dict['Author'])

		if 'xmp:CreatorTool' in metadata_dict:
			if type(metadata_dict['xmp:CreatorTool']) == type([]):
				metadata.extend(metadata_dict['xmp:CreatorTool'])
			else:	
				metadata.append(metadata_dict['xmp:CreatorTool'])

		if 'Content-Type' in metadata_dict:
			if type(metadata_dict['Content-Type']) == type([]):
				metadata.append(metadata_dict['Content-Type'][0])
			else:
				metadata.append(metadata_dict['Content-Type'])
		if 'Company' in metadata_dict:
			if type(metadata_dict['Company']) == type([]):
				metadata.append(metadata_dict['Company'][0])
			else:
				metadata.append(metadata_dict['Company'])

if __name__ == "__main__":
	args_parser = argparse.ArgumentParser()
	args_parser.add_argument('-dir', '--rootdir', required=True, help='Please enter a rootdir')
	args = args_parser.parse_args()
	filenames = [os.path.join(dirpath, f) for dirpath, dirnames, files in os.walk(args.rootdir) for f in fnmatch.filter(files, '*')]

	languages = []
	words = []
	metadata = []
	noun_tags = ["NN","NNP"]
	sweet_words = get_sweet_words()
	
	map(load_topics,filenames)
	for i in metadata:
		if type(i)!=type("") and type(i)!=type(u"aa"):
			print i, type(i)
	with open("wordcloud_text.json","w") as f:
		json.dump([{"text":k,"size":v} for k,v in FreqDist(words).iteritems()],f)
	with open("wordcloud_metadata.json","w") as f:
		json.dump([{"text":k,"size":v} for k,v in FreqDist(metadata).iteritems()],f)
	with open("wordcloud_language.json","w") as f:
		json.dump([{"text":k,"size":v} for k,v in FreqDist(languages).iteritems()],f)
