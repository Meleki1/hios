from hios.capabilities.execution.executor import Executor

from hios.capabilities.execution.models.action import Action
from hios.capabilities.execution.models.execution import Execution
from hios.capabilities.execution.models.action import Action, ActionType

class DefaultExecutor(Executor):

    def execute(
        self,
        execution: Execution,
    ) -> Execution:

        plan = execution.decision.plan

        actions = [
            Action(
                name=task.name,
                description=task.description,
                action_type=self._get_action_type(
                    task.name,
                ),
            )
            for task in plan.tasks
        ]

        return Execution(
            id=execution.id,
            decision=execution.decision,
            status=execution.status,
            actions=actions,
        )

    def _get_action_type(
        self,
        task_name: str,
    ) -> ActionType:

        if task_name == "Request Image Evidence":
            return ActionType.IMAGE_REQUEST

        return ActionType.SYSTEM_OPERATION