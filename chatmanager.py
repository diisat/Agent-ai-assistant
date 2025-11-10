# chatmanager.py
from agent import get_response

class ChatManager:
    def __init__(self, memory_size: int = 5):
        self.memory = [] 
        self.memory_size = memory_size

    def add_message(self, role: str, content: str):
        self.memory.append({"role": role, "content": content})
        self.memory = self.memory[-(self.memory_size * 2):]

    def get_context(self):
        if not self.memory:
            return "No previous context."
        return "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in self.memory
        )

    def chat(self, user_input: str):
        """
        Returns a generator that yields the assistant response in chunks.
        """
        context_prompt = f"Previous conversation:\n{self.get_context()}\n\nUser's latest query: {user_input}"
        return get_response(context_prompt)

