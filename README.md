About
=====

Finite groups spectra and prime graphs.

Usage
=====

Running GUI
-----------
Run `src/main.pyw` to launch GUI.

### Group selection
First thing to do is to specify group type and parameters.

![Group selection](https://raw.github.com/aikoven/calculations/master/doc/group_select.png)

After specifying parameters you might want to change graph calculation algorithm (Prime graph and Fast graph are currently supported), or postpone graph calculation by unselecting 'Show graph' checkbox.

### Group info
When you press 'Go' button, group order, apex and graph will be calculated and shown on the right frame of window.

![Group info](https://raw.github.com/aikoven/calculations/master/doc/group_info.png)

To see factorized form of group order, press 'F' button to the right of order widget.

Apex numbers can be expanded to how they were calculated by pressing 'Expand all' button or by selecting numbers in list and then selecting 'Expand' from right-click menu.

![Expanded apex](https://raw.github.com/aikoven/calculations/master/doc/apex_expanded.png)

Group name, order and apex numbers can be copied to clipboard using right-button menu. Regular or LaTeX forms are supported.

![Right button menu](https://raw.github.com/aikoven/calculations/master/doc/rb_menu.png)

**Search box** can be used to test if specified number is contained in the apex. Arbitrary arithmetic expressions are supported.

![Apex search](https://raw.github.com/aikoven/calculations/master/doc/apex_search.png)

**Cocliques** are not calculated right away, you should press 'Calculate' button. Double-click on coclique in the list to select its vertices in graph window.

![Cocliques](https://raw.github.com/aikoven/calculations/master/doc/cocliques.png)


### Fast graph
Fast graph algorithm is described [here](https://raw.github.com/aikoven/calculations/master/doc/fastgraph.pdf) (Russian)


Running tests
-------------
The whole project is covered with unit-tests, except for gui.
Use `tests/run_all_tests.py` to run them all.

Or you can use `pytest` and run `python -m pytest` or just `py.test` from `src/`.
