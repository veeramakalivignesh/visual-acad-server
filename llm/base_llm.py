class BaseLLM:
    
    def __init__(self, name='None'):
        self.name = name

    def get_result(self, system_prompt, user_prompt):
        pass

    def get_result_with_history(self, system_prompt, chat_history):
        pass
