import whisper
from langchain.llms import OpenAI
from langchain.agents import initialize_agent
from langchain.agents.agent_toolkits import ZapierToolkit
from langchain.utilities.zapier import ZapierNLAWrapper
import os
from dotenv import load_dotenv

load_dotenv()
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def email_summary(file):

    # large language model
    llm = OpenAI(temperature=0)

    # initialize zapier
    zapier = ZapierNLAWrapper()
    tookit = ZapierToolkit.from_zapier_nla_wrapper(zapier)

    # The agent used here is a "zero-shot-react-description" agent
    # zero-shot means the agent functions on the current action only - it has no memory
    # it uses the React framework to decide which tool to use, based solely on the tool's description.
    agent = initialize_agent(tookit.get_tools(), llm, agent="zero-shot-react-description", verbose=True)

    # specify model here its Base
    model = whisper.load_model("base")

    # transcribe audio file
    result = model.transcribe(file)
    print(result["text"])

    # send email using zapier
    agent.run("Send an email to quangtrandn93@gmail.com via gmail summarizing the following "
              "text provided below: " + result["text"])