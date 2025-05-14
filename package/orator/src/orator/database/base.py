from abc import abstractmethod, ABC

class Database(ABC):
	@abstractmethod
	def create_agent(self, llm):
		raise NotImplementedError

__all__ = ["Database"]
