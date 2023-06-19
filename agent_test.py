from langchain.agents import Tool
from langchain.agents import AgentType
from langchain.memory import ConversationBufferMemory
from langchain import OpenAI
from langchain.utilities import SerpAPIWrapper
from langchain.agents import initialize_agent

import streamlit as st
from streamlit_chat import message

search = SerpAPIWrapper(serpapi_api_key=st.secrets['SERP_API_KEY'])
tools = [
    Tool(
        name = "Current Search",
        func=search.run,
        description="useful for when you need to answer questions about current events or the current state of the world"
    ),
]

memory = ConversationBufferMemory(memory_key="chat_history")
if 'responses' not in st.session_state:
    st.session_state['responses'] = ["How can I assist you?"]

if 'requests' not in st.session_state:
    st.session_state['requests'] = []

if 'buffer_memory' not in st.session_state:
            st.session_state.buffer_memory=memory


st.title("Alphaflow Chatbot")
...
response_container = st.container()
textcontainer = st.container()

with textcontainer:
    with st.form(key='myform', clear_on_submit=True):
        queries = st.text_area("Query:", key="input")
        prompts = queries.split("-")
        #query = [st.text_input("Query: ", key="input")]
        submit = st.form_submit_button("Enter")

llm=OpenAI(openai_api_key=st.secrets['OPENAI_KEY'],temperature=0)
agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, verbose=True, memory= st.session_state.buffer_memory)

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
