from typing import Dict
from abc import ABC, abstractmethod

class CacheResolverMixin(ABC):

    @abstractmethod
    def resolve(actor) -> Dict:
        pass
