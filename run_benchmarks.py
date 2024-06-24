import json
from bot_pipeline import BoT
import argparse
import os
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--task_name',type=str,default='gameof24',choices=['gameof24','checkmate','wordsorting'])
parser.add_argument('--api_key',default=None,type=str,help='input your api key here')
parser.add_argument('--model_id',type=str,default='gpt-4o',help='Input model id here, if use local model, input the path to the local model')



GameOf24 = """
Let's play a game called 24. You'll be given four integers, and your objective is to use each number only once, combined with any of the four arithmetic operations (addition, subtraction, multiplication, and division) and parentheses, to achieve a total of 24. For example, if the input is 4, 7, 8, and 8, the output could be 7 * 8 - 4 * 8 = 24. You only need to find one feasible solution!
Input:
"""
CheckmateInOne = """
Given a series of chess moves written in Standard Algebraic Notation (SAN), determine the next move that will result in a checkmate.
Input: 
"""
WordSorting = """
Sort a list of words alphabetically, placing them in a single line of text separated by spaces.
Input:
"""


if __name__ == "__main__":
    args = parser.parse_args()
    task = args.task_name
    api_key = args.api_key
    model_id = args.model_id
    now = datetime.datetime.now()
    timestamp_str = now.strftime("%Y-%m-%d-%H:%M:%S")
    output_dir = 'test_results'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    benchmark_dict = {
        'gameof24':GameOf24,
        'checkmate':CheckmateInOne,
        'wordsorting':WordSorting
    }
    
    path_dict = {
        'gameof24':'benchmarks/gameof24.jsonl',
        'checkmate':'benchmarks/CheckmateInOne.jsonl',
        'wordsorting':'benchmarks/word_sorting.jsonl'
    }
    
    buffer_dict = {
        'gameof24':0,
        'checkmate':1,
        'wordsorting':2
        
    }
    
    user_prompt = benchmark_dict[task]
    path = path_dict[task]    
    problem_id = buffer_dict[task]
    test_bot = BoT(
            user_input = None,
            problem_id= problem_id,
            api_key= api_key,
            model_id= model_id,
            need_check = True
        )
    for line in (open(path)):
        input = json.loads(line)['input']
        user_input = user_prompt + input
        test_bot.update_input(user_input)
        result = test_bot.bot_run()
        tmp = {'input':input,'result':result}
        with open(f'test_results/BoT_{task}_{timestamp_str}.jsonl', 'a+', encoding='utf-8') as file:
            json_str = json.dumps(tmp)
            file.write(json_str + '\n')
