from pawpal_system import Pet, Task


def test_mark_complete_changes_task_status():
    task = Task("walk", 30, "medium", "max")
    assert task.completed == False
    result = task.mark_complete()
    assert result == True
    assert task.completed == True


def test_add_task_to_pet_increases_task_count():
    pet = Pet("max", "dog")
    assert len(pet.tasks) == 0
    pet.add_task(Task("walk", 30, "medium", "max"))
    assert len(pet.tasks) == 1
