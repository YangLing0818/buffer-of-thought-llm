import re
import io
import sys

meta_distiller_prompt = """

As a highly professional and intelligent expert in information distillation, you excel at extracting essential information to solve problems from user input queries. You adeptly transform this extracted information into a suitable format based on the respective type of the issue. If the problem can be generalized to a higher level to solve multiple issues, further analysis and explanation will be provided upon your next response.
Please categorize and extract the crucial information required to solve the problem from the user's input query. Combining these two elements will generate distilled information. Subsequently, deliver this distilled information, based on the problem type, to your downstream meta planner. The problem type should belong to one of the six categories mentioned above, and the distilled information should include:

1. Values and information of key variables extracted from user input, which will be handed over to the respective expert for task resolution, ensuring all essential information required to solve the problem is provided.
2. The objective of the problem and corresponding constraints.
3. Extend the problem based on 1 and 2, propose a meta problem that can address the user query and handle more input and output variations. Incorporate the real-world scenario of the extended problem along with the types of key variables and information constraints from the original problem to restrict the key variables in the extended problem. After that, use the user query input key information as input to solve the problem as an example.
4. Try to transform the problem into a python algorithm problem, and provide the input parameters.
5. Your task is to distill the problem, you shouldn't give the final result or possible solution in your respond.

Please distill the information following the format below and cease response after the output of the distilled information.



Meta distiller Respond:


Distilled Information:

1. Key information:

2. Restriction: (It should be noted that the answer should strictly follow the real-world rule such as in arithmatic equation, the Priority of operator, the need of parentheses etc. So according to the distilled information, emphasize the real-world rules that need to be followed within the problem.)

3. Distilled task:

4. Python transformation:
   (Optional, skip when Python tag is Not for Python) Input parameters:(The names of each variable should be clear and not confusing, and correspond to the entity names in the problem)
     variable1_name = x
     variable2_name = y
     .....
     variableN_name = z

5. Answer form: (Optional, skip when there is no specific answer form)

  **Note: The generation ends here. Do not show this message in your answer !**
  
"""



def extract_and_execute_code(text):
    # 定义代码块的开始和结束标记
    code_start_marker = "```python"
    code_end_marker = "```"

    # 找到Python代码开始的位置
    code_start_index = text.find(code_start_marker)
    if code_start_index == -1:
        code_start_marker = "```"
        code_start_index = text.find(code_start_marker)
    # 如果找到了代码开始的标记，提取并执行代码
    if code_start_index != -1:
        # 尝试找到代码结束的位置
        code_end_index = text.find(code_end_marker, code_start_index + len(code_start_marker))
        
        # 如果没有找到代码结束的标记，则假设代码一直持续到文本的末尾
        if code_end_index == -1:
            code_end_index = len(text)
        
        # 提取代码部分
        code_str = text[code_start_index + len(code_start_marker):code_end_index].strip()
        
        # 创建一个字符串流来捕获输出
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        # 执行提取的代码
        try:
            exec(code_str, globals())
        except Exception as e:
            # 恢复原始的标准输出
            sys.stdout = old_stdout
            return f"An error occurred: {e}", code_str
        
        # 获取执行代码的输出
        sys.stdout = old_stdout
        return new_stdout.getvalue(), code_str
    else:
        
        return "No Python code found in the provided string."


def extract_answer(text):
    # Define a regular expression pattern to match the answer format
    # The pattern accounts for variations in spacing and line breaks
    pattern = re.compile(r"Answer:\s*(.*?)\s*$", re.DOTALL)

    # Search the text for the pattern
    match = pattern.search(text)

    # If a match is found, return the content; otherwise, return None
    return match.group(1).strip() if match else None

