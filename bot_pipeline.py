import transformers
import torch
import http.client
import json
from accelerate import infer_auto_device_map
from meta_buffer_utilis import meta_distiller_prompt,extract_and_execute_code
from test_templates import game24,checkmate,word_sorting

class Pipeline:
    def __init__(self,model_id,api_key=None):
        self.api = False
        self.local = False
        self.model_id = model_id
        if api_key is None:
            self.local = True
            self.pipeline = transformers.pipeline(
        "text-generation",
        model=self.model_id,
        model_kwargs={"torch_dtype": torch.bfloat16},
        device_map = 'auto'
        )
        else:
            self.api = True
            self.api_key = api_key
    def get_respond(self,meta_prompt,user_prompt):
        if self.api:
            conn = http.client.HTTPSConnection("api.openai.com")
            payload = json.dumps({
            "model": self.model_id,
            "messages": [
                {
                    "role": 'assistant',
                    "content": meta_prompt
                },
                {
                    "role": 'user',
                    "content": user_prompt
                },
            ]
            })
            headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Content-Type': 'application/json'
            }
            conn.request("POST", "/v1/chat/completions", payload, headers)
            res = conn.getresponse()
            data = res.read()
            text = data.decode("utf-8")
            dict_object = json.loads(text)
            respond = dict_object['choices'][0]['message']['content']
            return respond
        else:
            messages = [
            {"role": "system", "content": meta_prompt},
            {"role": "user", "content": user_prompt},
        ]

            prompt = self.pipeline.tokenizer.apply_chat_template(
                    messages, 
                    tokenize=False, 
                    add_generation_prompt=True
            )

            terminators = [
                self.pipeline.tokenizer.eos_token_id,
                self.pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
            ]

            outputs = self.pipeline(
                prompt,
                max_new_tokens=2048,
                eos_token_id=terminators,
                do_sample=True,
                temperature=0.4,
                top_p=0.9,
            )
            respond = outputs[0]["generated_text"][len(prompt):]
            return respond
            

        
class BoT:
    def __init__(self, user_input,problem_id,api_key=None,model_id=None):
        self.api_key = api_key
        self.model_id = model_id
        self.pipeline = Pipeline(self.model_id,self.api_key)
        self.user_input = user_input
        # Only for test use, stay tuned for our update
        self.problem_id = problem_id 
        
    def problem_distillation(self):
        print(f'User prompt:{self.user_input}')
        self.distilled_information = self.pipeline.get_respond(meta_distiller_prompt, self.user_input)
        print(f'Distilled information:{self.distilled_information}')
        
    def buffer_retrieve(self):
        # For initial test use, we will later update the embedding retrieval version to support more 
        if self.problem_id == 0:
            self.thought_template = game24
        elif self.problem_id == 1:
            self.thought_template = checkmate
        elif self.problem_id == 2:
            self.thought_template = word_sorting
            
    def reasoner_instantiation(self):
        # Temporay using selection method to select answer extract method
        problem_id_list = [0,1,2]
        self.instantiation_instruct = """
You are an expert in problem analysis and can apply previous problem-solving approaches to new issues. The user will provide a specific task description and a thought template. Your goal is to analyze the user's task and generate a specific solution based on the thought template. If the instantiated solution involves Python code, only provide the code and let the compiler handle it. If the solution does not involve code, provide a final answer that is easy to extract from the text.
        """
        
        self.formated_input = f"""
Distilled information:
{self.distilled_information}
Thought template:
{self.thought_template}

Instantiated Solution:
Please analyze the above user task description and thought template, and generate a specific, detailed solution. If the solution involves Python code, only provide the code. If not, provide a clear and extractable final answer.        
        """

        self.result = self.pipeline.get_respond(self.instantiation_instruct,self.formated_input)
        print(f'Instantiated reasoning result: {self.result}')
        if self.problem_id in problem_id_list:
            self.final_result, code_str = extract_and_execute_code(self.result)
            print(f'The result of code execution: {self.final_result}')
        else:
            self.final_result = self.result 

    
    def bot_run(self):
        self.problem_distillation()
        self.buffer_retrieve()
        self.reasoner_instantiation()
        return self.final_result
    
    
    
        
           
            
            
        