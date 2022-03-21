# pygeosolve
Geometric constraint solver for Python. Uses numerical optimisation (via
[SciPy](http://www.scipy.org/)) to determine the solution to a given set of length and
angular constraints.

See the [documentation](https://seands.github.io/pygeosolve/) for more details.

## Potential future features
As stated in the documentation, this project is just a bit of fun. If the developer or
anyone else willing to contribute has time, here are some ideas for improvements to the
library:

- Implement overconstraint detection (e.g. using techniques presented
  [https://doi.org/10.1007/s11831-020-09509-y](here)).
- Implement symbolic parameters such that constraints can reference parameters of
  primitives. For example, it would be nice to be able to constrain a line to match the
  length of another line, even if the length of that other line is a free parameter.
- Implement symbolic solving, which will make solutions more robust and probably easier
  to find when the initial conditions are far from the optimal.
  [SolveSpace](https://solvespace.com/index.pl) for example implements this.
- Implement GUI to let users build and solve a system visually.
- Implement solution selection. Some problems (such as the
  [https://github.com/SeanDS/pygeosolve/blob/master/examples/triangle.py](triangle
  example)) have multiple valid solutions to the given constraints. Right now the
  solution chosen is the one the optimiser happens to converge on, which is sometimes
  not the one that's closest to the initial conditions. It is usually best choose the
  solution that's closest to the initial conditions in order to capture the user's
  intentions. This probably requires a different solver since the current one provides
  only one solution.

## Credits
Sean Leavey
https://github.com/SeanDS/
