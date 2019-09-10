# Assignment 1 README

## Team members

- Qi Yang       1511757
- Xinlei Chen   1471613
- Xutong Zhao   1430631

## Execution Instruction

Before running *Go0.py*, reset the python path to a valid path to python3. For instance,

```python
#!/usr/bin/python3
#/usr/local/bin/python3
```

## Assumptions and Explanations

1. For checking wrong color, only to check if the character is 'b' or 'w'. Alternating turns is not enforced. Please refer to [this post](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1107923).
2. `genmove` generates a random move from all legal moves and plays that move. Please refer to [this post](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1107923).
3. If there is already a winner, legal moves be an empty list. Please refer to [this post](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1107923).
4. If one player wins the game, and either the winner or loser plays one additional move using `play` command, output an error message indicating the game is over and do not make the specified move. If one player wins the game, and the winner plays a move using `genmove` command, handle it the same way. Please refer to [this post](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1107866) and [this post](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1107923).
5. No pass move is allowed. Please refer to [this post](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1107923).
6. We did not handle the case when there is a winner or the board is full, and the `gogui-rules_side_to_move` is called. Please refer to [this post](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1110952).
7. The output of `gogui-rules_legal_moves` is sorted using the python sort function (the same as the legal moves function in original *Go0.py*). Please refer to [this post](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1108341).
8. We modified all given python files to implement this assignment. Please refer to [this post](https://eclass.srv.ualberta.ca/mod/forum/discuss.php?d=1108209).

## Acknowledgement
We received constructive replies on the discussion forum from TAs Chao Gao and Chenjun Xiao.