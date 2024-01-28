import os
from crewai import Agent, Task, Crew, Process
from youtube_transcript_api import YouTubeTranscriptApi
from langchain.tools import tool


os.environ["OPENAI_API_KEY"] = "key here"

#GET TRANSCRIPT
def Get_transcript():
  transcript_list = YouTubeTranscriptApi.list_transcripts('7ESeQBeikKs')
  transcript = transcript_list.find_manually_created_transcript(['en'])
  script=transcript.fetch()
  words=''
  for i in range(len(script)):
      words+=script[i]['text']
  print(words)
  return words





#Agent responsible for creating summary

Summarizer = Agent(
  role='Transcript Summarizer',
  goal='Craft a compelling Summary of the given transcript of a Youtube video',
  backstory="""You are a renowned Content Summarizer, known for
  your insightful and engaging summaries.
  You transform complex concepts into compelling narratives.""",
  verbose=True,
  allow_delegation=True,
  tools=[Get_transcript]
)

#Defining task
task2 = Task(
  description="""Using the insights provided, develop an engaging summary
  post that highlights the most important parts of the transcript.
  Your post should be informative yet accessible, catering to a wide audience.
  Make it sound cool, avoid complex words so it doesn't sound like AI.
  Your final answer MUST be the full blog post of at least 4 paragraphs.""",
  agent=Summarizer
)




crew = Crew(
  agents=[Summarizer],
  tasks=[task2],
  verbose=2,
)


result = crew.kickoff()

print("######################")
print(result)
