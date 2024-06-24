import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--task_name',type=str,default='gameof24',choices=['gameof24','checkmate','wordsorting'])
parser.add_argument('--test_path',type=str)
if __name__ == "__main__":
    args = parser.parse_args()
    task = args.task_name
    test_path = args.test_path
    benchmark_path_dict = {
        'gameof24':'benchmarks/gameof24.jsonl',
        'checkmate':'benchmarks/CheckmateInOne.jsonl',
        'wordsorting':'benchmarks/word_sorting.jsonl'
    }
    test_path_dict = {
        'gameof24':'test_results/BoT_gameof24.jsonl',
        'checkmate':'test_results/BoT_checkmate.jsonl',
        'wordsorting':'test_results/BoT_wordsorting.jsonl'
    }
    benchmark_path = benchmark_path_dict[task]
    correct = 0
    truth = []
    test = []
    for line in (open(benchmark_path)):
        answer = json.loads(line)['target']
        truth.append(answer)
    for line in (open(test_path)):
        result = json.loads(line)['result']
        result = result.split('\n')[0]
        if task == 'gameof24':
            result = result.split('=')[0]
            test.append(result)
            try:
                if eval(result) == 24:
                    correct += 1
            except:
                continue
        else:
            test.append(result)
    if correct == 0:
        for i in range(len(test)):
            if truth[i] == test[i]:
                correct += 1
    print(f'Total number:{len(test)},Correct number:{correct},Accuracy:{correct/len(test)}')
    
        
            
            
            
                
        
    
