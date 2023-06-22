from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain import OpenAI, PromptTemplate
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent

import streamlit as st
from streamlit_chat import message

#Tools the agent use to search the internet
search = SerpAPIWrapper(serpapi_api_key=st.secrets['SERP_API_KEY'])
tools = [
    Tool(
        name = "Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or make research on a particular subject"
    ),
]
template = """You role is a ResearcherBot, you will be given a series of input from a user that is based on a workflow\
You are to take the inputs one after the other and perform each sequencially.
Perform each task specifically and right away without asking further questions..
Your response should be the result of work, except you are not given a specific task.

The inputs you are to run as a workflow will be inputed next by the user.

"""

#memory for the model to remember last inputs from user
memory = ConversationBufferMemory(memory_key="chat_history")

#hardcode AI welcome message
if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

#Define session for user input
if 'requests' not in st.session_state:
    st.session_state['requests'] = []

#add memory to session
if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=memory


st.title("Alphaflow Chatbot")
...
response_container = st.container()
textcontainer = st.container()
#Accept input from user and use split by (-) to return a list 
with textcontainer:
    with st.form(key='myform', clear_on_submit=True):
        queries = st.text_area("Query:", key="input")
        prompts = queries.split("-") # The list of prompt that will be looped over
        #query = [st.text_input("Query: ", key="input")]
        submit = st.form_submit_button("Enter")

llm=OpenAI(openai_api_key=st.secrets['OPENAI_KEY'],temperature=0)
agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory= st.session_state.buffer_memory)
response = agent_chain.run(template)
#If user enters input, loop over input and run the agent
if queries:
    
    for query in prompts:
        with st.spinner("typing..."):
            ...
            response = agent_chain.run(input=query)
            st.session_state.requests.append(query)
            st.session_state.responses.append(response)

with response_container:
    if st.session_state['responses']:
        for i in range(len(st.session_state['responses'])):
            message(st.session_state['responses'][i],key=str(i))
            if i < len(st.session_state['requests']):
                message(st.session_state["requests"][i], is_user=True,key=str(i)+ '_user')

        with st.expander("Show Messages"):
                st.write(agent_chain.memory.buffer)
