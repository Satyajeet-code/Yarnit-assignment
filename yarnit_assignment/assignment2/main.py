from flask import Flask, render_template, request
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

  
from dotenv import load_dotenv
load_dotenv()
groq=os.getenv('GROQ_API_KEY')

def marketing_content(formats,topic,emotion,length):


  llm=ChatGroq(groq_api_key=groq, model_name="Llama3-8b-8192")
  prompt = ChatPromptTemplate.from_messages([
    ("system", f"Please create a {formats} for the topic asked by the user with {emotion} within {length} characters. Use appropriate emojis wherever applicable. Make sure to be fully sure of the answers you provide."),
    ("user", f"Question:{topic}, Format:{formats}, Emotion:{emotion}, Length:{length}")
  ])
  output_parser=StrOutputParser()
  chain=prompt|llm|output_parser
  print("------------------------- Answer ---------------------")
  response=chain.invoke({'question':topic, 'Format':formats, 'Emotion':emotion, 'Length':length})
  print(response)
  response=response.replace("*","\n")
  return response

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
  if request.method == "POST":
    formats = request.form.get("format")
    topic = request.form.get("topic")
    emotion = request.form.get("emotion")
    length = request.form.get("length")
    output=marketing_content(formats,topic,emotion,length)

  else:
    formats = ""
    topic = ""
    length = ""
    emotion = ""
    output = ""
  return render_template("index.html", format=formats, topic=topic,length=length,emotion=emotion, output=output)

if __name__ == "__main__":
  app.run(debug=True)