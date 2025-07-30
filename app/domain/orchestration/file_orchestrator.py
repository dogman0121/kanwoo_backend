from dataclasses import dataclass
from typing import List, Callable

@dataclass
class FileOrchestratorAction:
    save: Callable[[], None]
    delete: Callable[[], None]


class FileOrchestrator:
    batch_size = 4

    def __init__(self):
        self.actions: List[FileOrchestratorAction] = []

    def _batch_generator(self):
        for idx in range(0, len(self.actions), self.batch_size):
            yield self.actions[idx : idx +  self.batch_size]

    def add_action(self, action: FileOrchestratorAction):
        self.actions.append(action)

    @staticmethod
    def _save(actions: List[FileOrchestratorAction]):
        for action in actions:
            action.save()

    @staticmethod
    def _rollback(actions: List[FileOrchestratorAction]):
        for action in actions:
            action.delete()

    def execute(self):
        batches = list(self._batch_generator())
        successful_batches = []

        try:
            for batch in batches:
                self._save(batch)
                successful_batches.append(batch)
        except Exception as e:
            for batch in successful_batches:
                try:
                    self._rollback(batch)
                except Exception as e:
                    pass

            raise e