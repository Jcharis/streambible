# import nltk

# nltk.download('wordnet')
# nltk.download('punkt')
# nltk.download('tagsets')
# nltk.download('treebank')
# nltk.download('all-corpora')
import subprocess
cmd = ['python3','-m' ,'textblob.download_corpora' ]
subprocess.run(cmd)
print("Working")