from ollama import chat

class OllamaClient():
    from typing import List, Optional
    messages: Optional[str]
    llm_model: str
    llm_context: str
    prompt_counter: int

    def __init__(self, llm_model: str, llm_context: str):
        self.llm_model = llm_model
        self.llm_context = llm_context
        self.messages = [
          {
            'role': 'system',
            'content': llm_context,
          },
        ]
        self.prompt_counter = 0

    def prompt(self, prompt: str) -> str:
        self.messages += [
            {
                'role': 'user',
                'content': prompt,
            }
        ]
        response = chat(
            self.llm_model,
            messages=self.messages
        )
        self.messages += [
            {
                'role': 'assistant',
                'content': response.message.content,
            }
        ]
        self.prompt_counter += 1
        return response.message.content
        
    def get_verses_for_point(self, outline_point: str) -> str:
        prompt = f"Give me a list of all the verse references in \"{outline_point}\"."
        return self.prompt(prompt)
    
    def reset(self) -> None:
        self.prompt_counter = 0
        self.messages = []

    def run_all(self) -> List[str]:
        self.reset()
        responses = []
        for pt in self.outline_points:
            responses.append(self.get_verses(pt))
        self.reset()
        return responses