import os
from crewai import Agent, Task, Crew, Process, LLM
from langfuse import Langfuse
from langfuse.decorators import observe, langfuse_context

LANGFUSE_PUBLIC_KEY = os.environ.get("LANGFUSE_PUBLIC_KEY", "your-public-key")
LANGFUSE_SECRET_KEY = os.environ.get("LANGFUSE_SECRET_KEY", "your-secret-key")
LANGFUSE_HOST = os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com")

# Initialize LangFuse
langfuse = Langfuse(
    public_key=LANGFUSE_PUBLIC_KEY,
    secret_key=LANGFUSE_SECRET_KEY,
    host=LANGFUSE_HOST
)



def create_research_agent():
    """Create AI Research Specialist agent"""
    return Agent(
        role="AI Research Specialist",
        goal="Research the latest advancements in AI technology",
        backstory="""You are an AI enthusiast with a passion for staying updated 
        on cutting-edge developments in artificial intelligence. You excel at 
        finding, analyzing, and summarizing the most recent and relevant 
        information about AI advancements.""",
        verbose=True,
        allow_delegation=False,
        # llm=LLM_MODEL  # Uncomment to use custom LLM
    )

def create_writer_agent():
    return Agent(
        role="Technical Writer",
        goal="Write comprehensive reports on AI technology based on research",
        backstory="""You are a skilled technical writer with expertise in 
        translating complex AI concepts into clear and engaging content. 
        You have a talent for creating well-structured, informative reports 
        that are accessible to both technical and non-technical audiences.""",
        verbose=True,
        allow_delegation=False,
        # llm=LLM_MODEL  # Uncomment to use custom LLM
    )


def create_research_task(agent):
    return Task(
        description="""Research the latest advancements in AI technology. 
        
        Focus on:
        1. Recent breakthroughs in AI models and architectures
        2. New applications of AI in various industries
        3. Emerging trends and future directions
        4. Key challenges and ethical considerations
        
        Provide a detailed summary with specific examples and data where available.""",
        agent=agent,
        expected_output="A detailed research summary of AI advancements with specific examples and data.",
    )

def create_writing_task(agent):
    """Create writing task"""
    return Task(
        description="""Write a comprehensive report on the latest advancements 
        in AI technology based on the research provided.
        
        The report should include:
        1. Executive Summary
        2. Key AI Advancements
        3. Industry Applications
        4. Future Trends
        5. Challenges and Considerations
        6. Conclusion
        
        Make it engaging, well-structured, and professionally formatted.""",
        agent=agent,
        expected_output="A well-structured comprehensive report on AI technology (minimum 500 words).",
    )


@observe()
def run_research_crew(research_topic=None):
    
    print("\n" + "="*70)
    print(" STARTING CREWAI MULTI-AGENT SYSTEM")
    print("="*70 + "\n")
    
    # Log to LangFuse
    langfuse_context.update_current_trace(
        name="crewai_research",
        metadata={
            "system": "multi-agent",
            "topic": research_topic or "AI advancements"
        }
    )
    
    print(" Creating agents...")
    research_agent = create_research_agent()
    writer_agent = create_writer_agent()
    
    print(" Creating tasks...")
    research_task = create_research_task(research_agent)
    writing_task = create_writing_task(writer_agent)
    
    if research_topic:
        research_task.description = f"Research {research_topic}. {research_task.description}"
        writing_task.description = f"Write a report about {research_topic}. {writing_task.description}"
    
    print(" Assembling crew...")
    crew = Crew(
        agents=[research_agent, writer_agent],
        tasks=[research_task, writing_task],
        verbose=True,
        process=Process.sequential,
    )
    
    print("\n Executing crew tasks...\n")
    results = crew.kickoff()
    
    # Log results to LangFuse
    langfuse_context.update_current_trace(
        output=str(results)
    )
    
    # Display results
    print("\n" + "="*70)
    print(" CREWAI RESULTS:")
    print("="*70)
    print(results)
    print("="*70 + "\n")
    
    return results

@observe()
def main():
    
    try:
        advanced_results = run_custom_crew(
            topic="Renewable Energy Technologies",
            research_focus="Solar and wind power efficiency improvements",
            output_format="Executive Brief"
        )
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "="*70)
    print("✅ ALL EXAMPLES COMPLETED")
    print("="*70)
    print(f"\n📊 View logs in LangFuse: {LANGFUSE_HOST}")
    
    # Flush LangFuse to ensure all logs are sent
    langfuse.flush()

if __name__ == "__main__":
    main()
Ask AI

Claude
