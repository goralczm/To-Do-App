from src.task import Task
from src.task_list import TaskList
from src.utils.task_priority import TaskPriority
from src.utils.task_status import TaskStatus
from src.workspace import Workspace

if __name__ == '__main__':
    house_chores_workspace = Workspace('House Chores')

    bathroom_task_list = TaskList('Bathroom')
    kitchen_task_list = TaskList('Kitchen')

    house_chores_workspace.add_task_list(bathroom_task_list)
    house_chores_workspace.add_task_list(kitchen_task_list)

    do_laundry_task = Task('Do Laundry')
    paint_walls_task = Task('Paint Walls', TaskPriority.MEDIUM, TaskStatus.DONE)
    do_dishes_task = Task('Do Dishes', TaskPriority.LOW, TaskStatus.TO_BE_DONE)
    empty_dishwasher_task = Task('Empty Dishwasher', TaskPriority.HIGH, TaskStatus.TO_BE_DONE)
    cook_dinner_task = Task('Cook Dinner', TaskPriority.HIGH, TaskStatus.IN_PROGRESS)

    house_chores_workspace.find_task_list_by_name('Bathroom').add_task(do_laundry_task)
    house_chores_workspace.find_task_list_by_name('Kitchen').add_task(paint_walls_task)
    house_chores_workspace.find_task_list_by_name('Kitchen').add_task(do_dishes_task)
    house_chores_workspace.find_task_list_by_name('Kitchen').add_task(empty_dishwasher_task)
    house_chores_workspace.find_task_list_by_name('Kitchen').add_task(cook_dinner_task)

    house_chores_workspace.sort_tasks_by_status_then_priority()

    print(house_chores_workspace)
