# Buffer of Thoughts: Thought-Augmented Reasoning with Large Language Models 

 <a href='https://arxiv.org/abs/2406.04271'><img src='https://img.shields.io/badge/arXiv-2406.04271-b31b1b.svg'></a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

Official implementation of our [Buffer of Thoughts (BoT)](https://arxiv.org/abs/2406.04271) framework (**NeurIPS 2024 Spotlight**). Affiliation: Peking University, UC Berkeley, Stanford University


## 📢 News
[2025.2] 🎉 We release [ReasonFlux](https://github.com/Gen-Verse/ReasonFlux), a revolutionary inference-scaling paradigm with a hierarchical RL algorithm: enpowering **a 32B model with 500 thought templates to outperform o1-preview and DeepSeek-V3** in reasoning tasks.

| Task           | **ReasonFlux 32B** | **DeepSeek V3** | **OpenAI o1-preview** | **OpenAI o1-mini** | **QWQ 32B-preview** | **GPT 4o** |
| :------------- | :----------------: | :-------------: | :-------------------: | :----------------: | :-----------------: | :--------: |
| MATH           |      **91.2**      |      90.2       |         85.5          |        90.0        |        90.6         |    76.6    |
| AIME 2024      |      **56.7**      |      39.2       |         44.6          |        56.7        |        50.0         |    9.3     |
| Olympiad Bench |      **63.3**      |      55.4       |           -           |        65.3        |        61.2         |    43.3    |
| GaokaoEn 2023  |      **83.6**      |        -        |         71.4          |        78.4        |        65.3         |    67.5    |
| AMC2023        |      **85.0**      |      80.0       |         90.0          |        95.0        |          -          |    47.5    |

[2024.10] 🎉 We release [SuperCorrect](https://github.com/YangLing0818/SuperCorrect-llm) based on Buffer of Thoughts, a new self-correction LLM reasoning framework. Notably, this new SupperCorrect-7B model achieves SOTA performance on MATH and GSM8K benchmarks among all 7B models.

[2024.10] 🎉 We update our repo and release our implementation of **Meta Buffer** and **Buffer Manager**  on math problems such as **GSM8K** based on amazing work [light-RAG](https://github.com/HKUDS/LightRAG).

[2024.6] 🎉 We release our code for evaluation on three benchmarks.

## Introduction

We introduce **BoT**, a novel and versatile thought-augmented reasoning approach designed to enhance the accuracy, efficiency, and robustness of large language models (LLMs). Specifically, we propose a **meta-buffer** to store a series of high-level thoughts, referred to as **thought-templates**, distilled from problem-solving processes across various tasks. For each problem, we retrieve a relevant thought-template and adaptively instantiate it with specific reasoning structures to conduct efficient reasoning. To ensure scalability and stability, we also propose a **buffer-manager** to dynamically update the meta-buffer, thus enhancing its capacity as more tasks are solved. We conduct extensive experiments on 10 challenging reasoning-intensive tasks, achieving significant performance improvements over previous state-of-the-art (SOTA) methods: 11% on Game of 24, 20% on Geometric Shapes, and 51% on Checkmate-in-One. Further analysis demonstrates the superior generalization ability and robustness of our BoT, while requiring only 12% of the cost of multi-query prompting methods (e.g., tree/graph of thoughts) on average. Notably, we find that our **Llama3-8B + BoT has the potential to surpass Llama3-70B** model.

<table class="center">
    <tr>
        <td width=100% style="border: none"><img src="assets/method.png" style="width:100%"></td>
    </tr>
    <tr>
        <td width="100%" style="border: none; text-align: center; word-wrap: break-word">Overview of our BoT</td>
    </tr>
</table>




## Comparison between Different Methods

| Task/Method           | GPT-4 | PAL  | ToT  | Meta Prompting | BoT (Ours) |
| --------------------- | :---: | ---- | ---- | :------------: | :--------: |
| Game of 24            |  3.0  | 64.0 | 74.0 |      67.0      |  **82.4**  |
| MGSM (avg)            | 84.4  | 72.0 | 86.4 |      84.8      |  **89.2**  |
| Multi-Step Arithmetic | 84.0  | 87.4 | 88.2 |      90.0      |  **99.8**  |
| WordSorting           | 80.4  | 93.2 | 96.4 |      99.6      | **100.0**  |
| Python Puzzles        | 31.1  | 47.3 | 43.5 |      45.8      |  **52.4**  |
| Geometric Shapes      | 52.6  | 51.2 | 56.8 |      78.2      |  **93.6**  |
| Checkmate-in-One      | 36.4  | 10.8 | 49.2 |      57.0      |  **86.4**  |
| Date Understanding    | 68.4  | 76.2 | 78.6 |      79.2      |  **88.2**  |
| Penguins              | 71.1  | 93.3 | 84.2 |      88.6      |  **94.7**  |
| Sonnet Writing        | 62.0  | 36.2 | 68.4 |      79.6      |  **80.0**  |


## Evaluation and Inference with Buffer of Thoughts

### 1. Benchmarks 

For now, we release our demo version of BoT based on three different benchmarks:

- **The Game of 24** from [Yao et al., 2023](https://github.com/princeton-nlp/tree-of-thought-llm)
- **Checkmate-in-One** from [the BIG-Bench suite](https://github.com/google/BIG-bench/tree/main) [(BIG-Bench authors, 2023)](https://arxiv.org/abs/2206.04615)
- **Word Sorting** from [BIG-Bench Hard](https://github.com/suzgunmirac/BIG-Bench-Hard) ([Suzgun et al., 2023](https://arxiv.org/abs/2210.09261); [BIG-Bench authors, 2023](https://github.com/google/BIG-bench/tree/main))

### 2. Meta Buffer

For each task, we choose one thought template sampled from our meta-buffer library. You may use our framework to construct your own meta buffer.

### 3. Quick Start

First, set up the environment:

```bash
git clone https://github.com/YangLing0818/buffer-of-thought-llm
cd buffer-of-thought-llm
conda create -n BoT python==3.9 
pip install -r requirements.txt
```

#### 3.1. Inference on math problems

Here we provide our inference code of  **BoT** based on **light-RAG** on GSM8K problems.  We provide some thought templates about math problems in [math.txt](./math.txt)

```python
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
```

Here you can use command below to conduct a quick test with OpenAI api using gpt-4o-mini and text-embedding-3-large by default

```
python inference.py --api_key 'Input your api key here'
```

You can also modify the problem within the prompt to solve different math problems.

(Our code is currently only support online LLMs on math problems, we will soon update and support local models !)

#### 3.2. Running on Three Benchmarks

Our BoT is easy to use. Just run:

```bash
python run_benchmarks.py --task_name 'gameof24' --api_key 'input your API key here if you want to use GPT-4' --model_id 'the model ID of GPT-4 or the path to your local LLM'
```

Here, **--task_name** could be one of gameof24, checkmate, wordsorting.

The **--api_key** is required if you want to use GPT-series; if not, you can skip it.

The **--model_id** should be the model ID of GPT-series like gpt-4o, gpt-4-turbo, or the path to your local LLM if you do not set **--api_key**.

The data for these three tasks are located in the `/benchmarks` directory.

The results generated during the experiment are stored in the `/test_results` directory.

#### 3.3. Validate the Test Results

Run the command below to validate the test results of our BoT:

```python
python validate_results.py --task_name 'gameof24' --test_path 'The path to the .jsonl file you want to validate'
```

This will print out the accuracy of the selected task on your relevant .jsonl file.

## 📖 BibTeX

```
@article{yang2024buffer,
  title={Buffer of Thoughts: Thought-Augmented Reasoning with Large Language Models},
  author={Yang, Ling and Yu, Zhaochen and Zhang, Tianjun and Cao, Shiyi and Xu, Minkai and Zhang, Wentao and Gonzalez, Joseph E and Cui, Bin},
  journal={Advances in Neural Information Processing Systems},
  year={2024}
}
```

## Acknowledgements

The implementation of our Meta Buffer and Buffer Manager is based on  [light-RAG](https://github.com/HKUDS/LightRAG). We want to express our gratitude for their amazing work and we will continue to update and adapt more different RAG frameworks.

