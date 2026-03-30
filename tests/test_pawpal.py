import pytest
from pawpal_system import Pet, Task, Owner, Schedule


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_owner(*tasks):
    """Return an Owner pre-loaded with the given Task objects."""
    owner = Owner("Tester", "", [Pet("max", "dog")], [])
    for t in tasks:
        owner.add_task(t)
    return owner


# ---------------------------------------------------------------------------
# Existing tests (kept)
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# sort_by_time — happy paths
# ---------------------------------------------------------------------------

def test_sort_by_time_returns_chronological_order():
    t1 = Task("dinner",   20, "medium", "max", time="18:00")
    t2 = Task("walk",     30, "medium", "max", time="07:00")
    t3 = Task("medicine", 5,  "high",   "max", time="12:30")
    owner = make_owner(t1, t2, t3)
    result = Schedule(owner).sort_by_time()
    assert [t.time for t in result] == ["07:00", "12:30", "18:00"]


def test_sort_by_time_single_task_returns_that_task():
    t = Task("walk", 30, "high", "max", time="09:00")
    owner = make_owner(t)
    result = Schedule(owner).sort_by_time()
    assert result == [t]


def test_sort_by_time_does_not_mutate_original_list():
    t1 = Task("b", 10, "low", "max", time="10:00")
    t2 = Task("a", 10, "low", "max", time="07:00")
    owner = make_owner(t1, t2)
    original_order = list(owner.tasks)
    Schedule(owner).sort_by_time()
    assert owner.tasks == original_order


# ---------------------------------------------------------------------------
# sort_by_time — edge cases
# ---------------------------------------------------------------------------

def test_sort_by_time_empty_task_list_returns_empty():
    owner = Owner("Tester", "", [], [])
    result = Schedule(owner).sort_by_time()
    assert result == []


def test_sort_by_time_already_sorted_stays_same():
    t1 = Task("a", 10, "low", "max", time="06:00")
    t2 = Task("b", 10, "low", "max", time="14:00")
    owner = make_owner(t1, t2)
    result = Schedule(owner).sort_by_time()
    assert result == [t1, t2]


def test_sort_by_time_same_hour_ordered_by_minutes():
    t1 = Task("a", 10, "low", "max", time="08:45")
    t2 = Task("b", 10, "low", "max", time="08:05")
    owner = make_owner(t1, t2)
    result = Schedule(owner).sort_by_time()
    assert result[0].time == "08:05"
    assert result[1].time == "08:45"


# ---------------------------------------------------------------------------
# Recurrence — happy paths
# ---------------------------------------------------------------------------

def test_complete_and_recur_marks_original_complete():
    owner = make_owner()
    t = Task("feed", 10, "high", "max", recur_days=1)
    owner.add_task(t)
    t.complete_and_recur(owner)
    assert t.completed == True


def test_complete_and_recur_adds_new_task_to_owner():
    owner = make_owner()
    t = Task("feed", 10, "high", "max", recur_days=1)
    owner.add_task(t)
    before = len(owner.tasks)
    t.complete_and_recur(owner)
    assert len(owner.tasks) == before + 1


def test_complete_and_recur_new_task_is_not_completed():
    owner = make_owner()
    t = Task("feed", 10, "high", "max", recur_days=1)
    owner.add_task(t)
    new_task = t.complete_and_recur(owner)
    assert new_task.completed == False


def test_complete_and_recur_new_task_preserves_properties():
    owner = make_owner()
    t = Task("feed", 15, "high", "max", time="07:00", recur_days=7)
    owner.add_task(t)
    new_task = t.complete_and_recur(owner)
    assert new_task.title == "feed"
    assert new_task.time_to_complete == 15
    assert new_task.priority == "high"
    assert new_task.pet_name == "max"
    assert new_task.time == "07:00"
    assert new_task.recur_days == 7


# ---------------------------------------------------------------------------
# Recurrence — edge cases
# ---------------------------------------------------------------------------

def test_complete_and_recur_non_recurring_returns_none():
    owner = make_owner()
    t = Task("one-off", 30, "low", "max", recur_days=0)
    owner.add_task(t)
    result = t.complete_and_recur(owner)
    assert result is None


def test_complete_and_recur_non_recurring_does_not_add_task():
    owner = make_owner()
    t = Task("one-off", 30, "low", "max", recur_days=0)
    owner.add_task(t)
    before = len(owner.tasks)
    t.complete_and_recur(owner)
    assert len(owner.tasks) == before


# ---------------------------------------------------------------------------
# Conflict detection — happy paths
# ---------------------------------------------------------------------------

def test_detect_conflicts_flags_overlapping_tasks():
    # walk: 07:00–07:30, feed: 07:15–07:30 → overlap
    t1 = Task("walk", 30, "medium", "max",   time="07:00")
    t2 = Task("feed", 15, "high",   "max",   time="07:15")
    owner = make_owner(t1, t2)
    warnings = Schedule(owner).detect_conflicts()
    assert len(warnings) == 1
    assert "walk" in warnings[0]
    assert "feed" in warnings[0]


def test_detect_conflicts_flags_exact_same_start_time():
    t1 = Task("walk",  30, "medium", "max",   time="08:00")
    t2 = Task("groom", 20, "low",    "Hunna", time="08:00")
    owner = make_owner(t1, t2)
    warnings = Schedule(owner).detect_conflicts()
    assert len(warnings) == 1


def test_detect_conflicts_cross_pet_overlap_is_caught():
    # Two different pets, same overlapping window
    t1 = Task("walk",  60, "high", "max",   time="09:00")
    t2 = Task("spray", 30, "low",  "Hunna", time="09:30")
    owner = make_owner(t1, t2)
    warnings = Schedule(owner).detect_conflicts()
    assert len(warnings) == 1


def test_detect_conflicts_returns_warning_strings():
    t1 = Task("a", 60, "high", "max", time="08:00")
    t2 = Task("b", 60, "low",  "max", time="08:30")
    owner = make_owner(t1, t2)
    warnings = Schedule(owner).detect_conflicts()
    assert all(isinstance(w, str) for w in warnings)
    assert all("WARNING" in w for w in warnings)


# ---------------------------------------------------------------------------
# Conflict detection — edge cases
# ---------------------------------------------------------------------------

def test_detect_conflicts_no_overlap_returns_empty():
    # walk ends 07:30, feed starts 08:00 → clear gap
    t1 = Task("walk", 30, "medium", "max", time="07:00")
    t2 = Task("feed", 15, "high",   "max", time="08:00")
    owner = make_owner(t1, t2)
    assert Schedule(owner).detect_conflicts() == []


def test_detect_conflicts_back_to_back_tasks_no_conflict():
    # t1 ends exactly when t2 starts → not an overlap
    t1 = Task("walk", 30, "medium", "max", time="07:00")  # ends 07:30
    t2 = Task("feed", 15, "high",   "max", time="07:30")  # starts 07:30
    owner = make_owner(t1, t2)
    assert Schedule(owner).detect_conflicts() == []


def test_detect_conflicts_single_task_no_conflict():
    owner = make_owner(Task("walk", 30, "medium", "max", time="09:00"))
    assert Schedule(owner).detect_conflicts() == []


def test_detect_conflicts_empty_task_list_no_conflict():
    owner = Owner("Tester", "", [], [])
    assert Schedule(owner).detect_conflicts() == []


def test_detect_conflicts_does_not_raise_on_bad_data():
    # Should return warnings, never crash
    t1 = Task("a", 30, "low", "max", time="08:00")
    t2 = Task("b", 30, "low", "max", time="08:00")
    owner = make_owner(t1, t2)
    try:
        Schedule(owner).detect_conflicts()
    except Exception:
        pytest.fail("detect_conflicts raised an exception unexpectedly")


# ---------------------------------------------------------------------------
# filter_tasks — happy paths & edge cases
# ---------------------------------------------------------------------------

def test_filter_by_pet_returns_only_that_pets_tasks():
    t1 = Task("walk",  30, "medium", "max",   time="07:00")
    t2 = Task("spray", 10, "low",    "Hunna", time="08:00")
    owner = make_owner(t1, t2)
    result = owner.filter_tasks(pet_name="max")
    assert all(t.pet_name == "max" for t in result)
    assert len(result) == 1


def test_filter_by_completed_false_excludes_done_tasks():
    t1 = Task("walk",  30, "medium", "max", time="07:00")
    t2 = Task("feed",  10, "high",   "max", time="08:00")
    t2.mark_complete()
    owner = make_owner(t1, t2)
    result = owner.filter_tasks(completed=False)
    assert all(not t.completed for t in result)


def test_filter_combined_pet_and_status():
    t1 = Task("walk",  30, "medium", "max",   time="07:00")
    t2 = Task("spray", 10, "low",    "Hunna", time="08:00")
    t1.mark_complete()
    owner = make_owner(t1, t2)
    result = owner.filter_tasks(pet_name="max", completed=False)
    assert result == []


def test_filter_pet_with_no_tasks_returns_empty():
    owner = make_owner(Task("walk", 30, "medium", "max", time="07:00"))
    result = owner.filter_tasks(pet_name="Hunna")
    assert result == []
