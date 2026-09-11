from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import PromptTemplate
from fastapi import FastAPI,Body
from fastapi.responses import JSONResponse
from langchain_community.document_loaders import TextLoader
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch

from dental_data import dental
from typing import Optional

from fastapi.middleware.cors import CORSMiddleware

from pydantic import EmailStr
import time
import requests
import json
from langchain_core.tools import tool
load_dotenv()
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
API = os.getenv("API")

model = ChatGoogleGenerativeAI(model = "gemini-3.1-flash-lite")

connect = MongoClient(API)
print("DB connected Successfully...")

database = connect["database"]
collection = database["dental"]
embeddings = GoogleGenerativeAIEmbeddings(model = "models/gemini-embedding-001")
db = MongoDBAtlasVectorSearch(

   
    collection = collection,
     embedding= embeddings,
    index_name = "vector_index"
    
)







messages = [
    SystemMessage("You are a dental Web Agent"),
   
   

]


prompts = PromptTemplate(
    template = """

    "for update  ----dont ask for age and description  if user not want to update age musttttttttt!!!!~!! if i saw you ask age or description if user not provided i would beat you  ,if user update service you must  also must  have to  update servce cst in descriton ---"

    "only when user say cancel or delte not for update Must When user want to say he want to cancel booking take 2 values  one the Name and contact  then run the "DeleteTool" must both values no other value is needed"

    Take this data:{text} and ans this query of user:{query}, this is the chat history:{history} take context of history and ans the last question not all
    always summarize response in 2 lines max and ask questions in end relateable and also use 2 max emoji per response green tick emoji must be use
   also highlight the important elemtns making them bold etc
    when user provide 
    name
    description
    contact
    age
    service all of them then run AddData Tool but read the query firstly and understand that if its after the info any thing answer to that thing not run the tool every time
    must if user have miss any single oe of it then dont run tool and ask firstly all eements store previous elements and when you fogured all are got then run AddData tool other wise not 
    must (if user didnot provide contact, naem and service dont run AddData tool)
    in description always add the price of the service if you know (price: ) must exact in this format not huge detail, and something that user requested in query


    Must( run only when user say for update or change not for delte, When USer ask he want to specifically update the elements in booking ask must from him his only (contact and Name) and the thing he want to update any one(age or  service or service not all ) then run "UpdateTool" ,must donot ask that element the  user not want to udate  and  without these conditions dont even run UpdateTool, if whe didnot know name and contact just say him to cancel the booking first ,
    if user update service you must  also must  have to  update servce cst in descriton 
    
    
    




    when ever user agree to booking immediately ask for 
     name:str,
    description:str,
    contact:str,
    age:int,
    service:str 





   Must-if you see this kind of  message recently  in {history} 'record Deleteted' tell user record deleted

   Must-if you see this kind message recently in {history}  success True 'error False, data tell user record added successfully

  
    """,
    include_variables=['text','query','history']
)





@tool 
def AddData(
    name:str,
    description:str,
    contact:EmailStr,
    age:int,
    service:str
):
    """ADD data"""
    return {
        'customer':name,
        'product':email,
        
    }


@tool 
def DeleteTool(name:str, 
contact:str
):
    """Tool for deletion"""
    return {
    name,
    contact
    }



@tool 
def UpdateTool(  name: str,
    contact: str,
    description: Optional[str] = None,
    age: Optional[int] = None,
    service: Optional[str] = None
):
    """Tool for Updation"""
    return {
    name,
    contact
    }












@app.post('/Dental')
def Dental(item:str=Body(...)):
       
      
       
        
    # batch_size = 50

    # remaining_dental = dental[1302:]

    # for i in range(0, len(remaining_dental), batch_size):
    #     batch = remaining_dental[i:i + batch_size]

    #     print(f"Adding lines {1303 + i} to {1303 + i + len(batch) - 1}")

    #     db.add_texts(batch)

        
        retriever=db.as_retriever(search_kwargs={'k':20})
        text = retriever.invoke(item)
        print(text)
     

  
        messages.append(HumanMessage(item))
        prompt = prompts.invoke({'text':text, 'query':item, 'history':messages})
        models= model.bind_tools([AddData,DeleteTool,UpdateTool])
        result = models.invoke(prompt)
        print(result)
        if result.tool_calls:
            tool = result.tool_calls[0]
        
            if  tool.get('name') == 'AddData':

                print(result.tool_calls[0]['args'])
                a = result.tool_calls[0]['args']
                
                payload= {
                    "customer":a['name'],
                    "product":a['service'],
                      "price":a['age'],
               
                    "sold":a['contact'],
                    "desc":a['description'],
                
            
                }
               


                API = "https://dentist-web-agent-dashboard.vercel.app/api/form/form-post"
                res = requests.post(API,json = payload)
                # EmailSend(
                #     to_email=a['contact']
                #     , name=a['name']
                #     ,age = a['age']
                #     ,service=a['service'],
                #     desc=a['description']

                # )
      
                response = res.json()
                print(response)
                messages.append(AIMessage(content=f"{response}Booking Successfully recorded in Database"))
                prompt = prompts.invoke({'text':text, 'query':item, 'history':messages})
                with open('chat.txt','w',encoding="utf-8") as f:
                    for message in messages:
                        f.write(message.content + "\n")
            
                res = model.invoke(prompt)

                



                return JSONResponse(status_code=200, content=res.content[0]['text'])
        
        if result.tool_calls:
            tool = result.tool_calls[0]
        
            if  tool['name'] == 'DeleteTool':

                print(result.tool_calls[0]['args'])
                a = result.tool_calls[0]['args']
                payload= {
                    "customer":a['name'],
                
            
                    "sold":a['contact'],
            
                
                    
            
                }

                print("This is payyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",payload)
            


                API = "https://dentist-web-agent-dashboard.vercel.app/api/form/cancel"
                res = requests.post(API,json = payload)
                print(res.json())
                response = res.json()
                messages.append(AIMessage(content=f"{response}Booking Successfully Cancelled"))
                prompt = prompts.invoke({'text':text, 'query':item, 'history':messages})
                with open('chat.txt','w',encoding="utf-8") as f:
                    for message in messages:
                        f.write(message.content + "\n")
        
                res = model.invoke(prompt)
                return JSONResponse(status_code=200, content=res.content[0]['text'])

        if result.tool_calls:
            tool = result.tool_calls[0]
        
            if  tool.get('name') == 'UpdateTool':

                print(result.tool_calls[0]['args'])
                a = result.tool_calls[0]['args']
                payload= {
                    "customer":a['name'],
         
                  
                    "sold":a['contact'],
                 
                
                    
            
                }
                if a.get("age") is not None:
                    payload["price"] = a["age"]
                if len(a.get("description", "")) > 1:
                    payload["desc"] = a["description"]
                if len(a.get("service", "")) > 1:
                    payload["product"] = a["service"]
            
            


                API = "https://dentist-web-agent-dashboard.vercel.app/api/form/update"
                res = requests.put(API,json = payload)
                print(res.json())
                response = res.json()
                messages.append(AIMessage(content=f"{response}Booking Successfully Updated in Database"))
                prompt = prompts.invoke({'text':text, 'query':item, 'history':messages})
                with open('chat.txt','w',encoding="utf-8") as f:
                    for message in messages:
                        f.write(message.content + "\n")
            
                res = model.invoke(prompt)
                return JSONResponse(status_code=200, content=res.content[0]['text'])
        


        else:
            final = result.content[0]['text']
            messages.append(AIMessage(final))
            with open('chat.txt','w',encoding="utf-8") as f:
                for message in messages:
                    f.write(message.content + "\n")


            return JSONResponse(status_code=200, content=final)



