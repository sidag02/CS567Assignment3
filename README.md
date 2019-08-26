# CS567Assignment3

This assignment is based on Reinforcement Learning wherein we had to compute the most optimum path for a car given a specific grid.
The code uses iterative formula to calculate the optimality of each neighbouring square.
The iteration continues till the delta is less than a specific value.
Since, the numbers are decimal, there are a lot of checks done to ensure precision of delta.
I have used various strategies to avoid recomputation and ease of code by using difference in coordinates to calculate the next move, using trigonometry to calculate turns, etc.

