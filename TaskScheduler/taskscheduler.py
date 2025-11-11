import heapq

# class TaskScheduler:
#     def __init__(self):
#         self.heap = []
#         self.counter = 0  # to preserve insertion order
#
#     def add_task(self, priority_id, task_id, execution_time):
#         # push a tuple with all sorting priorities
#         heapq.heappush(self.heap, (priority_id, execution_time, self.counter, task_id))
#         self.counter += 1
#
#     def get_all_tasks(self):
#         # heapq doesn’t have sorted order by default, so just return in sorted order view
#         # (heap itself is partially sorted, extraction will be O(n log n), but we can snapshot efficiently)
#         sorted_tasks = sorted(self.heap)
#         return [
#             {"task_id": t[3], "priority": t[0], "execution_time": t[1]}
#             for t in sorted_tasks
#         ]
#         # return self.heap
#
#     # def pop_next_task(self):
#     #     """Pop the next highest-priority task efficiently (O(log n))."""
#     #     if not self.heap:
#     #         return None
#     #     priority, exec_time, _, task_id = heapq.heappop(self.heap)
#     #     return {"task_id": task_id, "priority": priority, "execution_time": exec_time}
#
#
# if __name__ == '__main__':
#     scheduler = TaskScheduler()
#     scheduler.add_task(2, "A", 5)
#     scheduler.add_task(1, "B", 10)
#     scheduler.add_task(1, "C", 3)
#     scheduler.add_task(1, "D", 3)
#     scheduler.add_task(2, "E", 2)
#
#     print("All tasks (sorted view):")
#     for t in scheduler.get_all_tasks():
#         print(t)

import heapq
a=[]
a.append(((2, 5,1,"A")))
a.append(((1, 10,2,"B")))
a.append(((1, 5,3,"A")))
a.append(((1,3,4,"C")))
a.append(((2,5,5,"C")))
a.sort()
print(a)

