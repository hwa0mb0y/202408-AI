# (1) 기본 LangChain 예제
# pip install langchain openai
# pip install langchain-community  # langchain 내부에서 사용
# pip install langchain-openai

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from huggingface_hub import HuggingFaceHub

from getpass import getpass
import os

# OpenAI API 키를 안전하게 입력받습니다.  
api_key = getpass("OpenAI API 키를 입력하세요: ") 
# os.environ["OPENAI_API_KEY"] = "[OPEN API KEY]"
os.environ["OPENAI_API_KEY"] = api_key

# LLM 모델을 초기화합니다.
# temperature=0.7은 모델의 창의성 수준을 설정
# 2024년 8월 기준 GPT-3.5-turbo 사용
# llm = OpenAI(temperature=0.7, model="gpt-3.5-turbo")
# llm = OpenAI(temperature=0.7, max_tokens=700)  
HuggingFaceHub(
    repo_id="gpt2",  # 모델 이름 (여기서는 "gpt2" 사용)
    model_kwargs={"temperature": 0.7, "max_length": 100},  # 모델 설정
)

# 프롬프트 템플릿을 정의합니다.
# input_variables는 사용자가 입력할 변수를 지정하고, template은 실제 프롬프트의 형식을 정의
# {topic}은 나중에 사용자가 제공할 주제로 대체
# 정확하게 이야기하면 약간은 다른 성격이지만, template는 시스템 메시지의 작은 한 형태로 이해해도 된다.
prompt = PromptTemplate(
    input_variables=["topic"],
    template="{topic}에 대한 한국 내 유명한 블로그 포스트 세 곳을 추천해주세요.",
)

# LLMChain을 생성합니다.
# LLM과 프롬프트 템플릿을 연결하여 LLMChain을 생성
chain = LLMChain(llm=llm, prompt=prompt)

# 체인을 실행합니다.
result = chain.run("파이썬 프로그래밍")
print(result)
