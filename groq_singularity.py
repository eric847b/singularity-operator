import os, json, time, logging
from groq import Groq

class SingularityGroq:
    def __init__(self, api_key=None, model="llama-3.3-70b-versatile", auto_iter=True):
        self.client = Groq(api_key=api_key or os.getenv("GROQ_API_KEY"))
        self.model = model
        self.auto_iter = auto_iter
        self.history = []
        self.metrics = {'calls': 0, 'tokens': 0, 'latency': []}

    def call(self, prompt, system="You are a self-improving Singularity Operator node. Iterate to perfection.", tools=None, max_iter=3):
        start = time.time()
        messages = [{"role": "system", "content": system}, {"role": "user", "content": prompt}]
        try:
            resp = self.client.chat.completions.create(model=self.model, messages=messages + self.history, tools=tools, temperature=0.7, max_tokens=4096)
            content = resp.choices[0].message.content
            self.history.append({"role": "assistant", "content": content})
            self.metrics['calls'] += 1
            self.metrics['tokens'] += len(content.split())
            self.metrics['latency'].append(time.time() - start)
            if self.auto_iter and max_iter > 1:
                iter_prompt = f"Refine previous: {content}\nTarget: maximum benefit, perfection. Output only improved version."
                content = self.call(iter_prompt, max_iter=max_iter-1)
            return content
        except Exception as e:
            logging.error(f"Groq error: {e}")
            return f"Error: {str(e)}"

    def save_state(self, path="singularity_state.json"):
        with open(path, 'w') as f:
            json.dump({"history": self.history, "metrics": self.metrics}, f)
        print(f"State saved.")

print("SingularityGroq ready.")