from pawpal_system import Pet, Task, Owner, Schedule






p1 = Pet("max","dog")
p2 = Pet("Hunna", "Spider")

t1 = Task("wash", 200, "high", "Hunna")
t2 = Task("kisses", 20, "low", "max")
t3 = Task("walk", 300, "medium", "max")
t4 = Task("tv", 100, "medium", "Hunna")

bobby = Owner("Bobby","",[p1, p2],[t1,t2,t3])


bobby.add_task(t4)

SunnyDaySched= Schedule(bobby,500)


schedule = SunnyDaySched.generate_schedule()

print(f"\n{'='*35}")
print(f"  PawPal Schedule for {bobby.name}")
print(f"{'='*35}")
for task in schedule:
    print(f"  [{task.priority.upper():6}] {task.title:<10} ({task.time_to_complete} min) — {task.pet_name}")
print(f"{'='*35}\n")

