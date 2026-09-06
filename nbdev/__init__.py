"""Create delightful software with Jupyter Notebooks

Modules:

- `nbdev.extract_attachments`: A preprocessor that extracts all of the attachments from the notebook file. The extracted attachments are returned in the 'resources' dictionary.
- `nbdev.moddocs`: # Module docs: creating them from existing notebooks
- `nbdev.skill`: Author nbdev notebooks as source, documentation, examples, and tests. Ensure this guidance is in context before any notebook edit."""

__version__ = "3.3.16"

from .doclinks import nbdev_export
from .showdoc import show_doc

