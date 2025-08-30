import os
import asyncio


from dotenv import load_dotenv
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain_neo4j import Neo4jGraph
from langchain_core.documents import Document


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
graph = Neo4jGraph(url= os.getenv("NEO4J_URI"),username=os.getenv("NEO4J_USERNAME"), password= os.getenv("NEO4J_PASSWORD"),refresh_schema=False)



llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo")

llm_transformer = LLMGraphTransformer(llm=llm)


text = """
Ananya stared at the clock on her laptop screen. It was 10:45 p.m., and she was still in the middle of a presentation deck for her company’s quarterly review. She worked at a multinational consulting firm, where late nights were the norm. Her phone buzzed on the desk — a text from Rohan.

“Still at work? I just wrapped up my last call.”

Rohan was a senior engineer at a fast-growing product startup. His days started late but often stretched into the night with endless sprints and release deadlines. Ananya smiled faintly and typed back, “Almost done. Coffee tomorrow morning?”

Their lives had become a delicate dance between two demanding corporate worlds. She thrived on structured processes and client interactions, while he lived for innovation and the chaos of building something from scratch. Friends often wondered how they made it work when their schedules barely aligned, but for Ananya and Rohan, the challenge was part of the bond.

Weekdays were a blur of meetings, calls, and deliverables. Sometimes, their only conversations happened over hurried phone calls while rushing between conference rooms or waiting for cabs. Yet, in those fleeting moments, they found comfort. Ananya often teased Rohan about his obsession with product roadmaps, while he joked about her never-ending slide decks.

Saturdays were sacred. No laptops, no calls — just the two of them. They’d pick a quiet café, share stories about their week, and laugh at the absurdities of corporate life. Rohan would talk about bug fixes that broke entire systems; Ananya would narrate the theatrics of boardroom discussions. Despite the differences, they realized their struggles were mirrors of each other — both driven by ambition, yet yearning for balance.

One evening, after another long week, Rohan surprised Ananya with a simple gesture: he had blocked their calendars with a fake “team strategy session” so they could meet for dinner without interruption. Over candlelight, he admitted, “We may work in different worlds, but this — us — is the project I never want to miss a deadline for.”

Ananya laughed, her exhaustion melting away. She realized then that love wasn’t about perfectly aligned schedules or matching job titles. It was about choosing each other, day after day, in the middle of chaos.

Two corporates, two careers, one story — and they were determined to write it together.

"""
documents = [Document(page_content=text)]


async def main():
    """Main asynchronous function to run the graph transformation."""
    graph_documents = await llm_transformer.aconvert_to_graph_documents(documents)
    print(f"Nodes:{graph_documents[0].nodes}")
    print(f"Relationships:{graph_documents[0].relationships}")
    graph.add_graph_documents(graph_documents)


if __name__ == "__main__":
    
    asyncio.run(main())
    

