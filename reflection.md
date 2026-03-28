# PawPal+ Project Reflection

## 1. System Design
Core actions
-add pet and owner info
-add tasks
-view tasks
-generate schedule

Objects
### Pet 
 Attributes: name, animal
 Methods: delete pet, add pet

### Task
Attributes - time to complete, priority
Methods - set time, set priority, view tasks, delete task, add task, update task

### Shcedule
Attributes- schedule
Methods - generate schedule, delete schedule

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design consists of 4 core classes
- What classes did you include, and what responsibilities did you assign to each? The classes were pet - Attributes: name, animal
 Methods: delete pet, add pet

 owner - attributes: name, pets. 
 Methods: delete pet, add pet

 task
 Attributes: time to complete, priority
 methods: set time, set priority, view tasks, delete task, add task, update task

 Shcedule
Attributes- schedule
Methods - generate schedule, delete schedule

 
**b. Design changes**

- Did your design change during implementation?
yes
- If yes, describe at least one change and why you made it.
I connected a couple of classes together makeing them have some kind of relationship. 
e.g linking task to pet, task now has a pet_name property to know what pet has a task

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
It first goes with priority above all, then breaks priority ties(same priority) using duration. shorter tasks first.
for the time constraint/budget, the tasks are picked in a greedy manner until no time left.
- How did you decide which constraints. mattered most?
The constraint thats very specific and chosen by the user "Priority" 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
The greedy manner definitely, it does not go as deep to know which task should be done at what time. this can be bad because a high priority task may take too much time and leave little to no time left for another high priority task
- Why is that tradeoff reasonable for this scenario?
Its reasonable because there are other attributes used for sorting and prioritizing. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
