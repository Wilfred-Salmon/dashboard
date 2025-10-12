from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class ResourceCacher(ABC, Generic[T]):
    _cache: T | None

    def __init__(self) -> None:
        self._cache = None

    @abstractmethod
    def get_resource_to_cache(self) -> T:
        pass

    def cache_resource(self) -> None:
        self._cache = self.get_resource_to_cache()

    def ensure_cache(self) -> None:
        if self._cache is None:
            self.cache_resource()

    def get_cache(self) -> T:
        self.ensure_cache()
        
        return self._cache

    def invalidate_cache(self) -> None:
        self._cache = None
