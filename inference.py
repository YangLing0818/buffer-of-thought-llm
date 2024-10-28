from bot_pipeline import BoT
import argparse

parser = argparse.ArgumentParser(description='Use of argparse')

parser.add_argument('--llm_model',type=str,default='gpt-4o-mini',help='Model id of LLMs')
parser.add_argument('--embedding_model',type=str,default='text-embedding-3-large',help='Model id of embedding model')
parser.add_argument('--api_key',type=str,help='The api key of user')
parser.add_argument('--base_url',type=str,default='https://api.openai.com/v1/',help='we also support Open AI-like chat/embeddings APIs')
parser.add_argument('--rag_dir',type=str,default='./math',help='The path to save the meta buffer')

args = parser.parse_args()

llm_model = args.llm_model
embedding_model = args.embedding_model
api_key = args.api_key
base_url = args.base_url
rag_dir = args.rag_dir

prompt = "Solve the problem: Raymond and Samantha are cousins. Raymond was born 6 years before Samantha. Raymond had a son at the age of 23. If Samantha is now 31, how many years ago was Raymond's son born?"

bot = BoT(
          user_input= prompt, 
          api_key = api_key,
          model_id = llm_model,
          embedding_model = embedding_model,
          base_url = base_url,
          rag_dir = rag_dir
          )
bot.bot_inference()
