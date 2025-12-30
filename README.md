# CrewAI with LangFuse Integration

A simple multi-agent AI system using CrewAI with LangFuse observability tracking.

## What It Does

This system uses two AI agents working together:
1. **Research Agent** - Researches AI technology advancements
2. **Writer Agent** - Creates comprehensive reports based on research

All activity is logged to LangFuse for monitoring and analysis.

## Quick Start

### 1. Install Dependencies

```bash
pip install crewai langfuse
```

### 2. Set Environment Variables

```bash
# LangFuse credentials (get from https://langfuse.com)
export LANGFUSE_PUBLIC_KEY="your-public-key"
export LANGFUSE_SECRET_KEY="your-secret-key"
export LANGFUSE_HOST="https://cloud.langfuse.com"
```

### 3. Run

```bash
python your_script.py
```

## How It Works

```
Research Agent → Researches topic
       ↓
   Research Summary
       ↓
Writer Agent → Creates report
       ↓
   Final Report
       ↓
LangFuse → Logs everything
```

## What Gets Logged to LangFuse

- Agent activities
- Task execution details
- Final outputs
- Execution metadata
- Timing and performance

## Example Output

The system will:
1. Create a research agent and writer agent
2. Research the specified topic (default: AI technology)
3. Write a comprehensive report
4. Log all steps to LangFuse
