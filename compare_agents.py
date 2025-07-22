import time
import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, os.path.abspath("./agno"))
sys.path.insert(0, os.path.abspath("./crewai"))
sys.path.insert(0, os.path.abspath("./langchain"))
sys.path.insert(0, os.path.abspath("./langgraph"))

from test_agno.climate_agent import ClimateAgent as AgnoClimateAgent
from test_crewai.climate_agent import ClimateAgent as CrewAICLimateAgent
from test_langchain.climate_agent import ClimateAgent as LangChainClimateAgent
from test_langgraph.climate_agent import ClimateAgent as LangGraphClimateAgent

def extract_advice(result) -> str:
    """Extract advice from different result formats."""
    if isinstance(result, dict):
        for key in ['advice', 'final_output', 'output', 'result', 'response']:
            if key in result and result[key]:
                return str(result[key])
        
        for key, value in result.items():
            if isinstance(value, str) and value.strip():
                return value
        
        return str(result)
    
    elif isinstance(result, str):
        return result
    
    elif hasattr(result, 'raw'):
        raw_result = result.raw
        if isinstance(raw_result, list) and len(raw_result) > 0:
            return str(raw_result[-1])
        return str(raw_result)
    
    else:
        return str(result)

def benchmark_agent(agent_class, city: str, label: str) -> Dict[str, Any]:
    """Benchmark a single agent's response time for a climate question."""
    agent = agent_class()
    start = time.time()
    result = agent.get_climate_info(city)
    end = time.time()
    agent.close() if hasattr(agent, "close") else None
    
    print(f"  DEBUG - {label} result type: {type(result)}")
    if isinstance(result, dict):
        print(f"  DEBUG - {label} result keys: {list(result.keys())}")
    
    advice = extract_advice(result)
    
    return {
        "framework": label,
        "city": city,
        "response_time": end - start,
        "advice": advice,
        "full_result": result
    }

def main():
    city = "Paris"
    question = f"What is the climate like in {city}?"
    print(f"Benchmarking all agents for: {question}\n")
    results = []

    agents = [
        (AgnoClimateAgent, "Agno"),
        (CrewAICLimateAgent, "CrewAI"),
        (LangChainClimateAgent, "LangChain"),
        (LangGraphClimateAgent, "LangGraph"),
    ]

    for agent_class, label in agents:
        print(f"Running {label} agent...")
        try:
            res = benchmark_agent(agent_class, city, label)
            results.append(res)
            print(f"  Done in {res['response_time']:.2f} seconds.")
        except Exception as e:
            print(f"  Error running {label}: {e}")
            results.append({"framework": label, "city": city, "response_time": None, "advice": str(e), "full_result": None})

    print("\nResults:")
    print(f"{'Framework':<10} | {'Time (s)':<10} | {'Advice (truncated)':<50}")
    print("-" * 80)
    for res in results:
        time_str = f"{res['response_time']:.2f}" if res['response_time'] is not None else "ERROR"
        advice = res['advice']
        if len(advice) > 50:
            advice = advice[:47] + '...'
        print(f"{res['framework']:<10} | {time_str:<10} | {advice:<50}")

    with open("agent_benchmark_results.txt", "w") as f:
        f.write(f"Benchmark results for question: {question}\n")
        f.write("=" * 80 + "\n\n")
        
        for res in results:
            f.write(f"Framework: {res['framework']}\n")
            f.write(f"Response Time: {res['response_time']}s\n")
            f.write(f"City: {res['city']}\n")
            f.write(f"Advice:\n{res['advice']}\n")
            f.write("-" * 80 + "\n\n")

    with open("agent_benchmark_full_results.txt", "w") as f:
        f.write(f"Full benchmark results for question: {question}\n")
        f.write("=" * 80 + "\n\n")
        
        for res in results:
            f.write(f"Framework: {res['framework']}\n")
            f.write(f"Response Time: {res['response_time']}s\n")
            f.write(f"City: {res['city']}\n")
            f.write(f"Full Result Type: {type(res['full_result'])}\n")
            f.write(f"Full Result:\n{res['full_result']}\n")
            f.write("=" * 80 + "\n\n")

if __name__ == "__main__":
    main() 