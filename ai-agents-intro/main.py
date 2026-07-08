from google.adk.workflow._base_node import BaseNode

class ExplainerAgent(BaseNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prompt = ""

    def run(self):
        return f"Explication pour : {self.prompt}"

topic = "Python decorators"
agent = ExplainerAgent()
agent.prompt = f"Génère l'explication pour : {topic}"
response = agent.run()
print(response)