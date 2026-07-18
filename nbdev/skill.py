"""Author clear, executable nbdev notebooks where code, prose, examples, outputs, and tests form one coherent narrative.

# The notebook is the product

An nbdev notebook is simultaneously source code, documentation, examples, and tests. Write it to be read from top to bottom. The rendered page should explain the public API, while executing the same cells should build and verify it.

Do not treat an nbdev notebook as a Python module divided arbitrarily into cells. Use the notebook medium deliberately: interleave implementation with explanation, executable examples, useful outputs, plots, images, tables, diagrams, and demonstrations of failure whenever they communicate the idea better than prose alone.

These conventions matter most for published libraries with rendered documentation sites. Internal projects with no docs page can be looser: match the surrounding notebooks' style rather than imposing every rule here.

# Notebooks generate modules

The notebook is the source of truth: `nbdev-export` writes exported cells to the module named by `#| default_exp`, and generated `.py` files are never edited by hand. Each exported section carries a marker like `# %% ../nbs/04_usage.ipynb #a45f753a` naming its source notebook and cell, so module code always leads back to the cell to change. `__all__`, `_modidx.py`, and module docstrings likewise regenerate on export - renames and additions propagate automatically, so never hand-edit them.

The module docstring comes from the notebook's opening markdown: the title cell's `>` description line, joined with every *exported* markdown cell after the H1 (a markdown cell whose first line is `#| export`). For a long module docstring, prefer one exported markdown cell per section over packing everything into the title blockquote; both work.

Not every module must come from a notebook, and projects often mix the two deliberately. Choose per module: notebook-sourced when narrative earns its keep - public API whose docs page matters, code best explained through interleaved prose and examples, tests that double as documentation; plain `.py` when the code is dense interlocking mechanism, iterated quickly, and covered by pytest, where cell-by-cell narrative would add friction rather than clarity. Check the file, never the repo: a `# %%` autogen marker at the top means notebook-sourced, no marker means hand-written and edited directly, and `nbdev-export` only rewrites marked files. Tests follow the source form: example and test cells for notebook modules, `tests/*.py` pytest files for plain ones.

# Choose the kind of page

Decide which form of documentation the notebook provides:

- A **tutorial** teaches through a guided learning experience.
- A **how-to guide** helps a reader accomplish a practical task.
- An **explanation** develops understanding of a focused topic.
- A **reference** describes a technical component and its API.

Do not mix these forms accidentally. A reference page can contain examples, but should remain easy to scan for symbols and behavior. A tutorial should advance in a purposeful sequence rather than becoming an API inventory. A how-to should solve its stated problem without expanding into a general course. An explanation should clarify concepts and trade-offs rather than masquerading as step-by-step instructions.

# Open the notebook well

Start with a markdown cell containing an H1 title and a blockquote subtitle:

```markdown
# Great title

> A short description of what this page provides
```

Then introduce the page briefly. For a reference notebook, describe the component and orient the reader to its main symbols. For a tutorial or how-to, state what the reader will learn or accomplish. For an explanation, name the question or idea under discussion. Get to the subject quickly.

Use headings to make longer pages navigable. H2 headings normally divide major concepts or groups of symbols. Lower-level headings can organize longer discussions, but avoid fragmenting a short narrative into many tiny sections.

# Develop one idea at a time

A productive nbdev rhythm is:

1. Add the smallest useful implementation.
2. Explain what it does and why it has that form.
3. Demonstrate it with executable code.
4. Assert the behavior where an assertion improves the example.
5. Display the result a reader should notice.
6. Continue to the next idea.

This is a pattern, not a demand that every code cell contain one statement. A test or example cell may demonstrate several closely related facts. It must have a markdown introduction that tells the reader what the cell is about to establish. If that introduction becomes complicated, does not naturally introduce everything shown, or reads like an explanation of unrelated checks, the cell is doing too much and should be split. Conversely, prefer extending an existing example cell with a closely related check over adding a near-duplicate cell.

Keep definitions small enough to understand in context. When a class benefits from incremental development, define its core first and add methods later with `@patch`. This lets each method appear beside its explanation and examples. Keep a class together when splitting it would make the API harder, not easier, to understand.

# Prefer helpers with a public purpose

A helper introduced to make the notebook's own examples or tests clearer may also be a useful part of the library. Internal use is often the first evidence that an abstraction is worth exposing, not a reason to hide it.

Ask whether the helper gives users a concise, coherent operation they would otherwise need to reconstruct from lower-level internals. A good public helper:

- removes repeated knowledge of internal data structures
- gives a common operation a clear name and contract
- makes examples and downstream code easier to read
- provides one place to adapt callers when internals change
- is useful independently of the implementation that first needed it

For example, a function that constructs a canonical tool-call object may first appear while building a test fixture, but it is also useful to developers constructing those objects themselves. The fixture is its first consumer, not its justification for being private.

Treat private helpers with some suspicion. An underscore is appropriate for implementation machinery that has no coherent independent contract, but not merely because a function was first written for internal use. If a helper is only useful to the library itself, consider whether it exposes an awkward internal design that should instead become a small, reusable public abstraction.

# Make prose earn its place

Markdown should explain information the code does not express well:

- why an abstraction exists
- what distinction matters
- what behavior the next example demonstrates
- why a design choice was made
- what limitation or failure motivated the implementation
- how a symbol relates to the rest of the API
- which details are guarantees and which merely describe an example

Do not translate code line by line into English. Do not write empty transitions such as “Now we test the function.” State the lesson instead: “A missing leaf returns `None`, so success status alone does not establish existence.”

Place prose where it reads correctly in the generated page. An exported definition is normally followed by markdown explaining the symbol and introducing its first example.

# Keep docstrings short

Use a short docstring to say what a public symbol does. Put extended explanations, examples, trade-offs, warnings, and rich media in markdown cells, where they render properly and can include executable results.

Use docments beside parameters and return values. They keep argument documentation close to the signature without repeating the signature in a long docstring.

Use backticks around related symbols in prose. nbdev can turn symbol references into documentation links, so prefer symbol names over manually maintained documentation URLs.

# Examples are documentation and tests

Write every example as part of the page first, then make it verify behavior where useful. Good examples:

- use realistic, comprehensible values
- show the shortest path to the idea being taught
- produce an informative representation or result
- include direct assertions that reinforce rather than obscure the lesson
- reuse objects introduced naturally earlier in the notebook
- demonstrate important errors with executable failing examples

Avoid test-suite plumbing in reader-facing cells. Dense mocks, deeply nested comprehensions, long setup blocks, and many unrelated assertions make poor documentation even when they test correctly. Extract a tiny helper when setup obscures the behavior. Hide necessary but unreadable checks rather than forcing them into the page narrative.

Do not weaken a clear example merely to tolerate a future change that would invalidate its premise. If an example exists to show that an object contains a particular behavior, it should fail when that behavior disappears so the author notices and reassesses the page.

A code cell often ends with the value that should be displayed. The final line might show an object’s representation, a table, a plot, an image, a diff, a count, or another visual result of what was created or tested. Assertions verify; the final expression teaches. Prefer a useful stored output over ending every cell silently.

# Use notebook outputs deliberately

Notebooks can communicate with more than text. Use plots, images, tables, diagrams, videos, terminal recordings, rich HTML, and custom representations when they make behavior easier to grasp.

Design useful object representations when appropriate. A compact `_repr_markdown_`, table, plot, or structured summary can turn later examples into clear documentation without repeated formatting code.

Stored outputs are part of the explanation. They show the reader what an example produced and preserve evidence from an executed notebook. Keep them focused and readable; do not dump large structures without saying what matters in them.

# Show failures as behavior

Errors are part of an API. When a failure mode matters, demonstrate it with executable code and an assertion such as `expect_fail`, rather than describing it only in prose. A reader should be able to see which input fails and what rule is being enforced.

Keep failure examples focused. A large defensive test covering many hypothetical errors is less useful than one example for each important contract.

# Let state flow downward

Notebook state is sequential. Make that sequence easy to follow:

- keep imports in dedicated import cells
- define values shortly before they are first used
- reuse established objects instead of rebuilding near-duplicates
- avoid reassigning a name when later cells depend on its earlier meaning
- move genuinely shared setup into a small, clearly introduced helper
- end exploratory cells with the expression whose output records what was learned

A reader should not need to search far upward to understand where a value came from. If several later examples rely on setup, introduce the setup explicitly and explain its role.

The import rule is strict, and covers every cell including tests: the docs build executes each cell that contains an import in a fresh namespace where the other cells have not run, so a cell mixing imports with other code either breaks the build with a NameError or silently runs at documentation time.

# Use directives purposefully

`#| default_exp` selects the generated module. `#| export` marks implementation for export. Private underscore-prefixed helpers may be exported with their public consumers without becoming part of the public API. `#| hide` keeps necessary but distracting material off the rendered page. `#| eval: false` is for examples that genuinely must not run automatically, not for suppressing broken cells.

Directives affect both execution and documentation, so apply them according to the role of the whole cell. In particular, an unevaluated cell cannot create state required by later evaluated cells - so newly marking a cell `eval: false` means cascading the directive to the cells that depend on it.

# Prefer executable evidence

Whenever practical, show rather than claim:

- display the object instead of describing its representation
- run the transformation instead of paraphrasing the result
- draw the plot instead of only discussing its shape
- trigger the error instead of merely listing it
- compare outputs when a distinction matters

Executable evidence keeps documentation synchronized with behavior. Assertions turn important examples into regression tests, while visible outputs keep those tests useful to human readers.

# Common authoring failures

Avoid these patterns:

- a large implementation followed much later by one large test section
- several abstractions introduced before any is demonstrated
- markdown that merely narrates the next line of code
- long docstrings carrying material better expressed in notebook cells
- imports mixed into example or test cells
- repeated setup copied across examples
- reader-facing cells dominated by mocks or cleanup machinery
- many unrelated checks under one vague introduction
- assertions that hide the result the reader needs to see
- pages with no clear reader, purpose, or documentation form
- descriptions of behavior that could be demonstrated directly
- large outputs with no guidance about what to notice

The governing test is simple: the notebook should be pleasant and informative to read, convincing when executed, and useful as the source of the library it documents.
"""
