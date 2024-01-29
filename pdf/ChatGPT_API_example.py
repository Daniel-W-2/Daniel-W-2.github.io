# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 18:54:40 2024

@author: Dan
"""

from openai import OpenAI

client = OpenAI(api_key="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")

def gpt_response(prompt): 
    gpt_response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = [{"role": "user","content": prompt}],
        temperature = 0.5
)
    return gpt_response.choices[0].message.content


gpt_response('write a couplet about data')

### 

text = 'As a data scientist, you will extract, analyse and interpret large amounts of data from a range of sources, using algorithmic, data mining, artificial intelligence, machine learning and statistical tools, to make it accessible to businesses. Once you have interpreted the data, you will present your results using clear and engaging language. You will use your technical, analytical and communication skills to collect and examine data to help a business find patterns and solve problems. This can be for many purposes, for example, predicting what customers will buy or tackling plastic pollution.'

instructions = 'you will be provided a job description delimited by triple backticks, if that description includes the word data, summarize the top 3 skills required'

output_format = 'use the following format for the output: - Skill_1: <first skill> \n - Skill_2: <second_skill> \n  - Skill_3: <third_skill> \n'

prompt = instructions + output_format + f"```{text}"
              
print(gpt_response(prompt))  
