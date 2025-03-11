from brein.utils.log import log
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
import time
from typing import TypeVar, Generic

from brein.utils.uuid import uuid_generator


Payload = TypeVar("Payload")


@dataclass
class Task(Generic[Payload], ABC):
    payload: Payload
    id: str = field(default_factory=uuid_generator)
    retries: int = 0
    max_retries: int = 3
    next_retry_time: float = 0
    retry_base_delay: int = 5  # Base delay in seconds

    @abstractmethod
    def execute(self):
        """Task-specific logic"""
        pass

    def schedule_retry(self):
        """Calculate next retry time using exponential backoff"""
        self.retries += 1
        if self.retries > self.max_retries:
            log.error(f"Task {self.id} failed after {self.max_retries} retries")
            return False
        delay = self.retry_base_delay * (2**self.retries)
        self.next_retry_time = time.time() + delay
        log.warning(
            f"Task {self.id} failed. Retry {self.retries}/{self.max_retries} in {delay}s"
        )
        return True
