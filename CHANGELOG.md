# Release notes

<!-- do not remove -->

## 2.3.34

### New Features

- Migrate index creation from nbdev-index ([#1478](https://github.com/AnswerDotAI/nbdev/pull/1478)), thanks to [@ncoop57](https://github.com/ncoop57)


## 2.3.33

### New Features

- Improve error handling in `_build_lookup_table` entry points ([#1474](https://github.com/AnswerDotAI/nbdev/pull/1474)), thanks to [@ncoop57](https://github.com/ncoop57)


## 2.3.32

### New Features

- Improve backtick regex matching for function names ([#1469](https://github.com/fastai/nbdev/pull/1469)), thanks to [@ncoop57](https://github.com/ncoop57)
- make `nb_export` a cli [Enhancement] ([#1450](https://github.com/fastai/nbdev/pull/1450)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Make `nbdev_export` work outside nbdev repos ([#799](https://github.com/fastai/nbdev/issues/799))

### Bugs Squashed

- Use `r` strings to avoid new Python SyntaxWarnings in regex ([#1452](https://github.com/fastai/nbdev/issues/1452))
- Nested `lib_path` values break module -> notebook sync ([#1393](https://github.com/fastai/nbdev/issues/1393))


## 2.3.31

### New Features

- test if in `nbdev_repo` & improve `nbdev_export` err message ([#1448](https://github.com/fastai/nbdev/pull/1448)), thanks to [@hamelsmu](https://github.com/hamelsmu)


## 2.3.30

### New Features

- add `skip_procs` to `settings.ini` ([#1445](https://github.com/fastai/nbdev/pull/1445)), thanks to [@hamelsmu](https://github.com/hamelsmu)


## 2.3.29

### New Features

- Add `ai_magics` preprocessor ([#1442](https://github.com/fastai/nbdev/issues/1442))


## 2.3.28

### New Features

- Generate module docstrings from markdown meta summary ([#1440](https://github.com/fastai/nbdev/issues/1440))
- By default create markdown versions of docs too ([#1439](https://github.com/fastai/nbdev/issues/1439))
- add markdown to doc output ([#1438](https://github.com/fastai/nbdev/issues/1438))


## 2.3.27

- No new features or fixes---just an update to the pypi status since we forgot about it!

## 2.3.26

### New Features

- add enable/disable cell number in .py files ([#1428](https://github.com/fastai/nbdev/pull/1428)), thanks to [@dienhoa](https://github.com/dienhoa)
  - When exporting a notebook to a .py file, we currently have something like `# %% {nb_path} {cell_number}` at the beginning of each exported cell.
  - This PR adds one new setting in the setting.ini: `cell_number`. When set to False, we disable the `cell_number` discussed above.
  - Side effect: The `cell_number` is used to update the changes from .py back to the notebook, so disabling it also disables this feature.

### Bugs Squashed

- showdoc: SyntaxWarning: invalid escape sequence with Python 3.12 ([#1396](https://github.com/fastai/nbdev/issues/1396))


## 2.3.25

### New Features

- add `nbdev_requirements` ([#1415](https://github.com/fastai/nbdev/issues/1415))
- Auto-trust notebooks after `nbdev_clean` ([#1414](https://github.com/fastai/nbdev/issues/1414))


## 2.3.23

- Change `jupyter_hooks` default to `False`


## 2.3.22

- Remove max version constraint on ipywidgets dev dependency


## 2.3.21

### Bugs Squashed

- Remove unneeded ipywidgets requirement


## 2.3.20

### Bugs Squashed

- fixes UnboundLocalError: cannot access local variable `_TEMPLATE` where it is not associated with a value ([#1413](https://github.com/fastai/nbdev/pull/1413)), thanks to [@stepetal](https://github.com/stepetal)


## 2.3.19

### Bugs Squashed

- Remove boxes since they broke ToC ([#1411](https://github.com/fastai/nbdev/issues/1411))


## 2.3.18

### New Features

- Add magic `__` symbols to `show_doc` output ([#1410](https://github.com/fastai/nbdev/issues/1410))
- wrap `exports` cells in a shadowed box (like a card) ([#1409](https://github.com/fastai/nbdev/pull/1409)), thanks to [@hamelsmu](https://github.com/hamelsmu)


## 2.3.17

### New Features

- Move `exports` source after the `show_doc` ([#1408](https://github.com/fastai/nbdev/issues/1408))


## 2.3.16

### New Features

- Add code folding for `exports` ([#1407](https://github.com/fastai/nbdev/issues/1407))


## 2.3.15

### Bugs Squashed

- Reverted #1390


## 2.3.14

### New Features

- Add --no_browser option to nbdev_preview ([#1400](https://github.com/fastai/nbdev/pull/1400)), thanks to [@bamford](https://github.com/bamford)
- added conda_user and package_data to cfg_tail ([#1351](https://github.com/fastai/nbdev/pull/1351)), thanks to [@dsm-72](https://github.com/dsm-72)
- add repo and tag options to `nbdev_new` ([#1350](https://github.com/fastai/nbdev/pull/1350)), thanks to [@dsm-72](https://github.com/dsm-72)

### Bugs Squashed

- Changed `serve.proc_nbs` so that it makes use of its arguments `file_glob` and `file_re` ([#1390](https://github.com/fastai/nbdev/pull/1390)), thanks to [@lukastk](https://github.com/lukastk)


## 2.3.13

### New Features

- add support for 3.11 ([#1373](https://github.com/fastai/nbdev/pull/1373)), thanks to [@deven367](https://github.com/deven367)
- update install_quarto to distinguish arm64 and amd64 ([#1356](https://github.com/fastai/nbdev/pull/1356)), thanks to [@JonasHarnau](https://github.com/JonasHarnau)
- allow trailing `:` in directives for YAML compliance ([#1312](https://github.com/fastai/nbdev/pull/1312)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- CI error on uncleaned notebooks suggests upgrading nbdev ([#1308](https://github.com/fastai/nbdev/issues/1308))
- Auto-add index file onto `section` ([#1307](https://github.com/fastai/nbdev/pull/1307)), thanks to [@p4perf4ce](https://github.com/p4perf4ce)
- nbdev_clean: Add trailing newlines to mask diff between Jupyter and VSCode ([#1292](https://github.com/fastai/nbdev/pull/1292)), thanks to [@xl0](https://github.com/xl0)
- exported modules can scrub_magics ([#1250](https://github.com/fastai/nbdev/pull/1250)), thanks to [@yegeniy](https://github.com/yegeniy)
- Add extensions tutorial ([#1228](https://github.com/fastai/nbdev/pull/1228)), thanks to [@muellerzr](https://github.com/muellerzr)

### Bugs Squashed

- pin ipywidgets version ([#1318](https://github.com/fastai/nbdev/pull/1318)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Fix encoding issue for Windows OS User especially for non-English user ([#1314](https://github.com/fastai/nbdev/pull/1314)), thanks to [@JunDamin](https://github.com/JunDamin)


## 2.3.11

### New Features

- add agplv3 license to project options ([#1268](https://github.com/fastai/nbdev/pull/1268)), thanks to [@joel-lbth](https://github.com/joel-lbth)
- add 0 - Pre-planning status to project options ([#1262](https://github.com/fastai/nbdev/pull/1262)), thanks to [@ddobrinskiy](https://github.com/ddobrinskiy)
- add conda installation docs to end-to-end tutorial ([#1215](https://github.com/fastai/nbdev/pull/1215)), thanks to [@restlessronin](https://github.com/restlessronin)

### Bugs Squashed

- Fix `nbdev_conda` error when there are prior release tarballs ([#1280](https://github.com/fastai/nbdev/pull/1280)), thanks to [@restlessronin](https://github.com/restlessronin)
- delete build dir before pypi upload ([#1277](https://github.com/fastai/nbdev/pull/1277)), thanks to [@restlessronin](https://github.com/restlessronin)
- copy contents of `_extensions` folder from nbs ([#1266](https://github.com/fastai/nbdev/pull/1266)), thanks to [@restlessronin](https://github.com/restlessronin)
- Fix `nbdev_update` when `lib_name` and `lib_path` are not the same ([#1254](https://github.com/fastai/nbdev/pull/1254)), thanks to [@BirkhoffG](https://github.com/BirkhoffG)
- Make `nbdev_create_config` write the `black_formatting` setting ([#1235](https://github.com/fastai/nbdev/pull/1235)), thanks to [@dmose](https://github.com/dmose)
- fix order of categories for migration ([#1221](https://github.com/fastai/nbdev/pull/1221)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- make anaconda description links consistent with pypi ([#1214](https://github.com/fastai/nbdev/pull/1214)), thanks to [@restlessronin](https://github.com/restlessronin)
- .get instead of acessing attr ([#1023](https://github.com/fastai/nbdev/pull/1023)), thanks to [@hamelsmu](https://github.com/hamelsmu)


## 2.3.9

### New Features

- utility that creates a `requirements.txt` file from `settings.ini` ([#1202](https://github.com/fastai/nbdev/pull/1202)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- user-friendly error if py file has `# %%` comments with unexpected format ([#1211](https://github.com/fastai/nbdev/pull/1211)), thanks to [@seeM](https://github.com/seeM)
- add parameter for name to `nb_export` ([#1204](https://github.com/fastai/nbdev/pull/1204)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- ensure newline at end of `_modidx.py` ([#1186](https://github.com/fastai/nbdev/issues/1186))

### Bugs Squashed

- end `sidebar.yml` with newline ([#1212](https://github.com/fastai/nbdev/pull/1212)), thanks to [@seeM](https://github.com/seeM)
- fix: incorrect regex pattern for setting `output-file` ([#1210](https://github.com/fastai/nbdev/pull/1210)), thanks to [@seeM](https://github.com/seeM)
- ensure newline at end of `_modidx.py` ([#1209](https://github.com/fastai/nbdev/pull/1209)), thanks to [@seeM](https://github.com/seeM)
- fix: `nbdev_install_quarto` may install and remove unrelated packages ([#1208](https://github.com/fastai/nbdev/pull/1208)), thanks to [@seeM](https://github.com/seeM)
- fix: key error if widgets is missing `state` ([#1207](https://github.com/fastai/nbdev/pull/1207)), thanks to [@seeM](https://github.com/seeM)
-`nbdev_install_quarto` may install and remove unrelated packages ([#1182](https://github.com/fastai/nbdev/issues/1182))
- Key error if widgets is missing `state` ([#1167](https://github.com/fastai/nbdev/issues/1167))


## 2.3.8

### New Features

- better error messages for `nbdev_migrate` ([#1177](https://github.com/fastai/nbdev/issues/1177))
- experimental: Users can provide extra processors via the `procs` key in `settings.ini` ([#1157](https://github.com/fastai/nbdev/pull/1157)), thanks to [@seeM](https://github.com/seeM)
- enable Documentation Only Sites With `nbdev` ( + tutorial ) ([#1121](https://github.com/fastai/nbdev/pull/1121)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- support non-library projects ([#1119](https://github.com/fastai/nbdev/issues/1119))
- throw a warning when imports and code are mixed in a cell ([#714](https://github.com/fastai/nbdev/issues/714))

### Bugs Squashed

- fix duplicated sections in the sidebar ([#1165](https://github.com/fastai/nbdev/pull/1165)), thanks to [@seeM](https://github.com/seeM)
- setting `#| echo` in a cell with `show_doc` causes a Quarto error ([#1163](https://github.com/fastai/nbdev/issues/1163))
- fix copying of index assets ([#1143](https://github.com/fastai/nbdev/pull/1143)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- images in index.ipynb causing deployments issues ([#1140](https://github.com/fastai/nbdev/issues/1140))
- clean takes forever on notebooks with large output ([#1132](https://github.com/fastai/nbdev/issues/1132))
- `nbdev_update` includes folders starting with `_` or `.` (e.g. `.ipynb_checkpoints`) ([#1130](https://github.com/fastai/nbdev/pull/1130)), thanks to [@seeM](https://github.com/seeM)
- `nbdev_new` defaults bool parameters to `False` (e.g. `put_version_in_init`) ([#1129](https://github.com/fastai/nbdev/pull/1129)), thanks to [@seeM](https://github.com/seeM)
- `black_formatting` setting is ignored ([#1122](https://github.com/fastai/nbdev/pull/1122)), thanks to [@jmoralez](https://github.com/jmoralez)
- `nbdev_readme()` fails on the second run for the notebook with support files (e.g. Fig image). ([#1106](https://github.com/fastai/nbdev/issues/1106))
- `nbdev_new` fails with `AttributeError: path_` ([#1063](https://github.com/fastai/nbdev/issues/1063))
- fix #1041 ([#1049](https://github.com/fastai/nbdev/pull/1049)), thanks to [@seeM](https://github.com/seeM)


## 2.3.7

### New Features

- Set recursive `True` by default ([#1117](https://github.com/fastai/nbdev/pull/1117)), thanks to [@seeM](https://github.com/seeM)
- `exec_doc` supports re-rendering widgets ([#1113](https://github.com/fastai/nbdev/pull/1113)), thanks to [@seeM](https://github.com/seeM)
  - If users update widgets with the `exec_doc` directive, the widget "view" is updated (in the cell output), but the old widget "state" is used (in notebook metadata). This refreshes widget state using `ipywidgets.Widget.get_manager_state`.
- `nbdev_new` pins on major+minor version of `nbdev-template` ([#1091](https://github.com/fastai/nbdev/issues/1091))
- `nbdev_proc_nbs` completes all steps to build `_proc` for publishing ([#1086](https://github.com/fastai/nbdev/issues/1086))
- `nbdev_new` defaults `nbs_path` setting to `'nbs'` ([#1083](https://github.com/fastai/nbdev/issues/1083))
  - Since all website files (quarto config, css, images, etc) are in `nbs_path`, the current default `nbs_path='.'` can clutter the root folder.
- `nbdev_new` queries `branch` from GitHub ([#1080](https://github.com/fastai/nbdev/issues/1080))

### Bugs Squashed

- fix exporting `patch_to` which is decorated with `staticmethod` ([#1100](https://github.com/fastai/nbdev/pull/1100)), thanks to [@seeM](https://github.com/seeM)
- `show_doc` errors if a dependency in the `nbdev` group has a sub-dependency that isn't installed ([#1097](https://github.com/fastai/nbdev/issues/1097))
- Running `nbdev_migrate` while upgrading removes nbdev2 compatible directives ([#1089](https://github.com/fastai/nbdev/issues/1089))
- respect `#|hide` and `#|include: false` for showdoc ([#1079](https://github.com/fastai/nbdev/pull/1079)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Export class to library but hide from documentation ([#1076](https://github.com/fastai/nbdev/issues/1076))
- `nbdev_clean` removes widget state ([#1069](https://github.com/fastai/nbdev/issues/1069))
  - If widget state is present, it means the user had intentionally changed settings in their notebook editor.


## 2.3.4

### New Features

- improve jekyll migration ([#1078](https://github.com/fastai/nbdev/pull/1078)), thanks to [@hamelsmu](https://github.com/hamelsmu)

### Bugs Squashed

- skip `_docs` and `_site` in processing ([#1085](https://github.com/fastai/nbdev/issues/1085))
- fix alias bug ([#1075](https://github.com/fastai/nbdev/pull/1075)), thanks to [@hamelsmu](https://github.com/hamelsmu)


## 2.3.3

### New Features

- auto-upgrade `_quarto.yml` for v1.2 ([#1073](https://github.com/fastai/nbdev/issues/1073))
- Add Blog Tutorial ([#1061](https://github.com/fastai/nbdev/pull/1061)), thanks to [@hamelsmu](https://github.com/hamelsmu)


## 2.3.2

### New Features

- Support GitHub Enterprise ([#944](https://github.com/fastai/nbdev/issues/944))

### Bugs Squashed

- `nbdev_new` fails with `AttributeError: path_` ([#1063](https://github.com/fastai/nbdev/issues/1063))


## 2.3.1

### Breaking Changes

- `_quarto.yml` no longer replaced with automatically generated version ([#1059](https://github.com/fastai/nbdev/issues/1059))
  - This was listed in 2.3.0 but wasn't actually included in the release

### Bugs Squashed

- fix `nbdev_update` ([#1058](https://github.com/fastai/nbdev/pull/1058)), thanks to [@seeM](https://github.com/seeM)
  - fix bug in `nbdev.maker.update_import` which meant that `nbdev_update` didn't convert relative imports without `None` module (e.g `from . import foo` -> `from pkg import foo`)
  - fix `FileNotFoundError` in `nbdev_update` by passing the correct py module and corresponding notebook paths
  - fix `nbdev_update` introducing whitespace changes to notebooks


## 2.3.0

### Breaking Changes

- `_quarto.yml` no longer replaced with automatically generated version
  - You can now customise your `_quarto.yml` file and it will not be overridden by nbdev
  - This means that `custom_host` and `custom_port` in `settings.ini` are no longer supported -- use the standard quarto configuration instead
- Parallel ipynb filter ([#961](https://github.com/fastai/nbdev/issues/961))
  - `ipynb-filters` in `_quarto.yml` is no longer needed or recommended. Instead, nbdev preprocesses your notebooks in parallel into a folder called `_proc` before calling quarto
  - The new processing system generally results in speedups of around 10x compared to the previous approach
- Deprecate `config_key` in favor of `get_config` ([#856](https://github.com/fastai/nbdev/pull/856)), thanks to [@seeM](https://github.com/seeM)

### New Features

- Setting `put_version_in_init ` to make adding `__version__` to `__init__.py` optional ([#1051](https://github.com/fastai/nbdev/pull/1051)), thanks to [@MichaelJFishmanBA](https://github.com/MichaelJFishmanBA)
- `nbdev_new` support for GitHub Enterprise ([#1043](https://github.com/fastai/nbdev/pull/1043)), thanks to [@seeM](https://github.com/seeM)
- Use `GITHUB_TOKEN` if present for `nbdev.release` ([#1025](https://github.com/fastai/nbdev/issues/1025))
- Support non qmd py rendering scripts ([#1014](https://github.com/fastai/nbdev/issues/1014))
- Use penultimate suffix for extension of rendered .py scripts ([#1010](https://github.com/fastai/nbdev/issues/1010))
- Print `nbdev_test` cell errors to stderr instead of using `logging.warning` ([#1003](https://github.com/fastai/nbdev/issues/1003))
- Make nb meta `display_name` consistent with `name` to simplify diffs ([#995](https://github.com/fastai/nbdev/issues/995))
- Windows support for clean nb ([#989](https://github.com/fastai/nbdev/pull/989)), thanks to [@jvanelteren](https://github.com/jvanelteren)
- Preview support for parallel filter ([#976](https://github.com/fastai/nbdev/issues/976))
- Settings.ini option for choosing preview listen port ([#967](https://github.com/fastai/nbdev/issues/967))
- Vscode extension for nbdev which cleans notebooks ([#952](https://github.com/fastai/nbdev/issues/952))
- Authenticate nbdev-template github API call ([#940](https://github.com/fastai/nbdev/issues/940))
- Add `printit` arg to `nbdev_filter` so it can be called with `fname` and still print to stdout ([#931](https://github.com/fastai/nbdev/pull/931)), thanks to [@seeM](https://github.com/seeM)
- Run `nbdev_readme` in `nbdev_new` ([#919](https://github.com/fastai/nbdev/pull/919)), thanks to [@seeM](https://github.com/seeM)
- Improve config documentation in `read` module ([#864](https://github.com/fastai/nbdev/pull/864)), thanks to [@seeM](https://github.com/seeM)
- Simplify `jupyter_hooks` configuration ([#780](https://github.com/fastai/nbdev/pull/780)), thanks to [@seeM](https://github.com/seeM)

### Bugs Squashed

- Class method doclinks target `mod.html#method` instead of `mod.html#class.method` ([#1046](https://github.com/fastai/nbdev/pull/1046)), thanks to [@seeM](https://github.com/seeM)
- "Bad credentials" error in `nbdev_new` if GitHub Enterprise `GH_HOST` and `GITHUB_TOKEN` are used ([#1038](https://github.com/fastai/nbdev/issues/1038))
- Suppress `UserWarning` for unset `GITHUB_TOKEN` in `nbdev_new` ([#1028](https://github.com/fastai/nbdev/pull/1028)), thanks to [@seeM](https://github.com/seeM)
- `nbdev.release` uses `cfg.lib_name` instead of `cfg.repo` ([#1024](https://github.com/fastai/nbdev/pull/1024)), thanks to [@seeM](https://github.com/seeM)
- `nbdev_test` does not restore the original working directory ([#1004](https://github.com/fastai/nbdev/issues/1004))
- `clean_ids` corrupts string outputs ([#794](https://github.com/fastai/nbdev/pull/794)), thanks to [@seeM](https://github.com/seeM)


## 2.2.10

### Bugs Squashed

- missing `doc_path.name` in `_docs` move ([#973](https://github.com/fastai/nbdev/issues/973))


## 2.2.9

### New Features

- Experimental: pre-commit hooks ([#959](https://github.com/fastai/nbdev/pull/959)), thanks to [@seeM](https://github.com/seeM)
- setup GitHub repo automatically ([#955](https://github.com/fastai/nbdev/pull/955)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Authenticate nbdev-template github API call ([#940](https://github.com/fastai/nbdev/issues/940))
- Support module level docstrings ([#473](https://github.com/fastai/nbdev/issues/473))

### Bugs Squashed

- `show_doc` includes parsed sections from numpy docstrings ([#964](https://github.com/fastai/nbdev/issues/964))
- `AnnAssign` object has no attribute 'targets' ([#953](https://github.com/fastai/nbdev/issues/953))
- Exported images not found in docs ([#951](https://github.com/fastai/nbdev/issues/951))
- fix #769 ([#946](https://github.com/fastai/nbdev/pull/946)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- `recursive` in settings.ini ignored ([#942](https://github.com/fastai/nbdev/issues/942))
- Wrong source link when using @patch ([#939](https://github.com/fastai/nbdev/issues/939))
- Deploy Action fails with `ModuleNotFoundError: No module named 'https://github'` ([#936](https://github.com/fastai/nbdev/issues/936))
- Recursive mode doesn't seem to work when running `nbdev_preview` ([#935](https://github.com/fastai/nbdev/issues/935))
- Update All Python Scripts to nbs similar to `nbdev_update_lib` in v1 ([#769](https://github.com/fastai/nbdev/issues/769))


## 2.2.7

### New Features

- Add `printit` arg to `nbdev_filter` so it can be called with `fname` and still print to stdout ([#931](https://github.com/fastai/nbdev/pull/931)), thanks to [@seeM](https://github.com/seeM)
- Run `nbdev_readme` in `nbdev_new` ([#919](https://github.com/fastai/nbdev/pull/919)), thanks to [@seeM](https://github.com/seeM)
- In `nbdev_prepare()` auto render README if needed ([#913](https://github.com/fastai/nbdev/issues/913))
- Filter keys stored in modidx settings ([#903](https://github.com/fastai/nbdev/issues/903))
- Regression: reintroduce `[source]` link ([#692](https://github.com/fastai/nbdev/issues/692))

### Bugs Squashed

- Deploy Action fails with `ModuleNotFoundError: No module named 'https://github'` ([#936](https://github.com/fastai/nbdev/issues/936))
- Correct cell index in `nbdev_update` ([#934](https://github.com/fastai/nbdev/pull/934)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Handle repo names with dashes and correct index page rendering with file attachments ([#930](https://github.com/fastai/nbdev/pull/930)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- `IPython.display.Image(embed=True)` results in incorrect image reference in GitHub Pages ([#924](https://github.com/fastai/nbdev/issues/924))
- `nbdev_preview` not starting if there is a folder with no notebook in it ([#922](https://github.com/fastai/nbdev/issues/922))
- Fix images ([#918](https://github.com/fastai/nbdev/pull/918)), thanks to [@seeM](https://github.com/seeM)
- `nbdev_update` creates a new cell, instead of updating the original code ([#775](https://github.com/fastai/nbdev/issues/775))


## 2.2.6

### New Features

- Build `_modidx.py` on demand in order to git conflicts ([#911](https://github.com/fastai/nbdev/issues/911))
- Add source link to index ([#909](https://github.com/fastai/nbdev/issues/909))
- Order left navigation sections using numeric prefix ([#901](https://github.com/fastai/nbdev/issues/901))
- Automatic rendering of python files with frontmatter ([#895](https://github.com/fastai/nbdev/issues/895))

### Bugs Squashed

- Make sure `#|exec_doc` triggers an update even when there is no export or show_doc ([#906](https://github.com/fastai/nbdev/pull/906)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- allow nbdev directives to work with cell magic ([#905](https://github.com/fastai/nbdev/pull/905)), thanks to [@hamelsmu](https://github.com/hamelsmu)


## 2.2.0
### Breaking Changes

- Combine preprocs and postprocs into new `Processor` class ([#874](https://github.com/fastai/nbdev/issues/874))
- Rename `nbdev.read` to `nbdev.config` ([#879](https://github.com/fastai/nbdev/issues/879))
- Use H3 for functions and properties, instead of H4 ([#875](https://github.com/fastai/nbdev/issues/875))
- Remove `nbflags` directive ([#871](https://github.com/fastai/nbdev/issues/871))
- Deprecate `config_key` in favor of `get_config` ([#856](https://github.com/fastai/nbdev/pull/856)), thanks to [@seeM](https://github.com/seeM)

### New Features

- Add simple qmd generation functions in `nbdev.qmd` ([#893](https://github.com/fastai/nbdev/issues/893))
- Add `FrontmatterProc` ([#890](https://github.com/fastai/nbdev/issues/890))
- Improvements to `nbdev_new` and `nbdev_create_config` ([#878](https://github.com/fastai/nbdev/pull/878)), thanks to [@seeM](https://github.com/seeM)
  - `nbdev_create_config` infers settings from git/GitHub, prompts for missing settings, and renders the settings file with commented sections
  - `nbdev_new` uses `nbdev_create_config` instead of a file provided by `nbdev-template`, which means it'll benefit from future improvements to `nbdev_create_config` as well as always using latest defaults
- Add frontmatter bullet point processor ([#873](https://github.com/fastai/nbdev/issues/873))
- Allow specifying port for preview ([#872](https://github.com/fastai/nbdev/pull/872)), thanks to [@dleen](https://github.com/dleen)
- `nbdev_new` renders notebooks with information from your config file ([#866](https://github.com/fastai/nbdev/pull/866)), thanks to [@seeM](https://github.com/seeM)
- Improve config documentation in `read` module ([#864](https://github.com/fastai/nbdev/pull/864)), thanks to [@seeM](https://github.com/seeM)
- Install quarto without root access ([#860](https://github.com/fastai/nbdev/issues/860))
- Explain more detail during quarto installation process ([#859](https://github.com/fastai/nbdev/issues/859))
- Automatically maintain `__version__` in `__init__.py` ([#854](https://github.com/fastai/nbdev/issues/854))
- Prettify output for `nbdev_test` ([#849](https://github.com/fastai/nbdev/pull/849)), thanks to [@deven367](https://github.com/deven367)
- Ignore .ipynb_checkpoints folder in module dir ([#848](https://github.com/fastai/nbdev/pull/848)), thanks to [@dleen](https://github.com/dleen)
- Escape Footnotes from Docments Table ([#847](https://github.com/fastai/nbdev/pull/847)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Include filename in `nbdev_export` warning when nbdev1 syntax is used ([#838](https://github.com/fastai/nbdev/pull/838)), thanks to [@seeM](https://github.com/seeM)
- Show title if nbdev_filter errors ([#828](https://github.com/fastai/nbdev/pull/828)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Added "topics" to match GitHub's terminology ([#817](https://github.com/fastai/nbdev/pull/817)), thanks to [@tylere](https://github.com/tylere)
- Accelerate `quarto preview` ([#748](https://github.com/fastai/nbdev/issues/748))
- Throw a warning when imports and code are mixed in a cell ([#714](https://github.com/fastai/nbdev/issues/714))
- Make conda release work for anyone ([#653](https://github.com/fastai/nbdev/issues/653))

### Bugs Squashed

- `_all_` works for strings but not objects in py3.7 ([#870](https://github.com/fastai/nbdev/issues/870))
- `show_doc` `title_level` argument has no effect ([#869](https://github.com/fastai/nbdev/issues/869))
- `show_doc` sometimes does not show wrapped functions correctly ([#863](https://github.com/fastai/nbdev/issues/863))
- `show_doc` treats functions decorated with `lru_cache` as classes ([#862](https://github.com/fastai/nbdev/pull/862)), thanks to [@seeM](https://github.com/seeM)
- Fix `show_doc` signature whitespace removal ([#855](https://github.com/fastai/nbdev/pull/855)), thanks to [@seeM](https://github.com/seeM)
- `nbdev_new` doesn't infer anything if no gitconfig ([#846](https://github.com/fastai/nbdev/issues/846))
- `show_doc` paremeter default may render as footnote ([#796](https://github.com/fastai/nbdev/issues/796))
- Conda description is empty ([#745](https://github.com/fastai/nbdev/issues/745))


## 2.1.6

### New Features

- add `nbdev_conda` to create and upload conda packages ([#850](https://github.com/fastai/nbdev/issues/850))


## 2.1.4

### New Features

- Add `custom_quarto_yml` setting ([#842](https://github.com/fastai/nbdev/pull/842)), thanks to [@benoit-cty](https://github.com/benoit-cty)
- Display multiline docstrings ([#841](https://github.com/fastai/nbdev/issues/841))
- Include filename in `nbdev_export` warning when nbdev1 syntax is used ([#835](https://github.com/fastai/nbdev/issues/835))
- Streamline `nbdev_new`: outputs are now in color, you can pass `--lib_name`, and it calls `nbdev_export` ([#820](https://github.com/fastai/nbdev/pull/820)), thanks to [@seeM](https://github.com/seeM)
- A command for uploading to the test pypi server ([#818](https://github.com/fastai/nbdev/pull/818)), thanks to [@tourdownunder](https://github.com/tourdownunder)
- Include notebook title in `nbdev_preview` error message ([#802](https://github.com/fastai/nbdev/issues/802))
- Migrate collapsible code cell directives ([#783](https://github.com/fastai/nbdev/pull/783)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Simplify `jupyter_hooks` configuration ([#780](https://github.com/fastai/nbdev/pull/780)), thanks to [@seeM](https://github.com/seeM)
- Support `nbdev_install_hooks` in  non-nbdev repos ([#779](https://github.com/fastai/nbdev/pull/779)), thanks to [@seeM](https://github.com/seeM)
- Allow users to provide user-level settings in ~/.config/nbdev/settings.ini ([#778](https://github.com/fastai/nbdev/pull/778)), thanks to [@seeM](https://github.com/seeM)
- Support `nbdev_install_hooks` in  non-nbdev repos ([#777](https://github.com/fastai/nbdev/issues/777))
- Port `doc()` from nbdev1 ([#772](https://github.com/fastai/nbdev/issues/772))
- Make `show_doc` for function parameter defaults concise and deterministic ([#771](https://github.com/fastai/nbdev/issues/771))
- Clean `id` from text `repr` outputs to further avoid git merge conflicts ([#749](https://github.com/fastai/nbdev/issues/749))
- Add repo root to sys path on exec ([#735](https://github.com/fastai/nbdev/issues/735))
- Use frontmatter `eval` and `showdoc` for controlling notebook execution ([#734](https://github.com/fastai/nbdev/issues/734))

### Bugs Squashed

- #|exports directive does not show source code in the docs ([#822](https://github.com/fastai/nbdev/issues/822))
- nbdev commands fail when `doc_path` contains whitespace ([#813](https://github.com/fastai/nbdev/pull/813)), thanks to [@mone27](https://github.com/mone27)
- `show_doc` html renderer is incorrectly formatted ([#808](https://github.com/fastai/nbdev/issues/808))
- `show_doc` cell output is incorrectly styled ([#807](https://github.com/fastai/nbdev/issues/807))
- links aren't rendered as code ([#795](https://github.com/fastai/nbdev/pull/795)), thanks to [@seeM](https://github.com/seeM)
- `clean_ids` corrupts string outputs ([#794](https://github.com/fastai/nbdev/pull/794)), thanks to [@seeM](https://github.com/seeM)
- quarto frontmatter is removed ([#789](https://github.com/fastai/nbdev/issues/789))
- `nbdev_merge` fails on `git stash pop` conflict ([#787](https://github.com/fastai/nbdev/pull/787)), thanks to [@seeM](https://github.com/seeM)
- Hooks search Jupyter start directory instead of notebook directory for settings file ([#784](https://github.com/fastai/nbdev/pull/784)), thanks to [@dleen](https://github.com/dleen)
- Allow for dash in Quarto directives ([#782](https://github.com/fastai/nbdev/pull/782)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Fix directive migration when there is no test flag ([#781](https://github.com/fastai/nbdev/pull/781)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- `nbdev_prepare` throws BrokenProcessPool error on MacOS ([#731](https://github.com/fastai/nbdev/issues/731))
- settings.ini not inferred by `nbdev_new` on newly cloned repo on MacOS ([#710](https://github.com/fastai/nbdev/issues/710))


## 2.1.2

### New Features

- use global defaults instead of respecifying each time ([#770](https://github.com/fastai/nbdev/pull/770)), thanks to [@seeM](https://github.com/seeM)
- `get_config` works without a settings file ([#768](https://github.com/fastai/nbdev/pull/768)), thanks to [@seeM](https://github.com/seeM)
- add site url ([#767](https://github.com/fastai/nbdev/pull/767)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- add `show_src` to display rich source code ([#763](https://github.com/fastai/nbdev/pull/763)), thanks to [@seeM](https://github.com/seeM)
- add support for `#|exports` ([#762](https://github.com/fastai/nbdev/issues/762))
- `nbdev_merge` prints info like `git merge` ([#753](https://github.com/fastai/nbdev/issues/753))
- helpers to convert fp front matter to quarto front matter ([#750](https://github.com/fastai/nbdev/pull/750)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Streamline default settings ([#747](https://github.com/fastai/nbdev/issues/747))
- Config keys (and their defaults) should all be documented in one place
- add `user` option to `jupyter_hooks` setting ([#738](https://github.com/fastai/nbdev/pull/738)), thanks to [@seeM](https://github.com/seeM)
- Add appropriate `output-file` to existing frontmatter ([#728](https://github.com/fastai/nbdev/issues/728))

### Bugs Squashed

- `nbdev_prepare` sometimes throws BrokenProcessPool error on MacOS ([#731](https://github.com/fastai/nbdev/issues/731))
- Incorrect relative import from package root inside nested module ([#773](https://github.com/fastai/nbdev/issues/773))
- Jupyter hooks break in environments without `nbdev` installed ([#760](https://github.com/fastai/nbdev/issues/760))
- `nbdev_fix` breaks with empty `ours` patch ([#752](https://github.com/fastai/nbdev/issues/752))
- fix `nbdev_merge` during rebase; fix `nbdev_fix` `nobackup` default ([#737](https://github.com/fastai/nbdev/pull/737)), thanks to [@seeM](https://github.com/seeM)
- non-notebooks do not have nbformat field ([#732](https://github.com/fastai/nbdev/pull/732)), thanks to [@dleen](https://github.com/dleen)


## 2.1.1

### New Features

- add tools from fastrelease to nbdev ([#733](https://github.com/fastai/nbdev/issues/733))

### Bugs Squashed

- fix `nbdev_test` with no `--fname` in non-nbdev repos ([#730](https://github.com/fastai/nbdev/pull/730)), thanks to [@seeM](https://github.com/seeM)
- Auto-generated showdoc headers not in ToC ([#703](https://github.com/fastai/nbdev/issues/703))


## 2.1.0

### Breaking Changes

- `nbdev_sidebar` now looks for `.qmd` files instead of `.md` files

### New Features

- automatically add `output:asis` for showdoc cells ([#726](https://github.com/fastai/nbdev/issues/726))
- accelerate `nbdev_readme` ([#715](https://github.com/fastai/nbdev/issues/715))
- deterministic `show_doc` and `DocmentTbl` `repr` ([#707](https://github.com/fastai/nbdev/pull/707)), thanks to [@seeM](https://github.com/seeM)

### Bugs Squashed

- KeyError 'repo' when trying to create a new nbdev project with `nbdev_new` ([#720](https://github.com/fastai/nbdev/issues/720))
- `show_doc` ends the details column at any `|` character ([#712](https://github.com/fastai/nbdev/issues/712))
- only add to `.gitattributes` if missing ([#706](https://github.com/fastai/nbdev/pull/706)), thanks to [@seeM](https://github.com/seeM)


## 2.0.7

### New Features

- git merge hooks: automatically resolve conflicts and render markers as separate cells ([#704](https://github.com/fastai/nbdev/pull/704)), thanks to [@seeM](https://github.com/seeM)
- Allow clean to keep some metadata keys ([#672](https://github.com/fastai/nbdev/pull/672)), thanks to [@dleen](https://github.com/dleen)
- enable mac terminal install instead of visual installer ([#705](https://github.com/fastai/nbdev/pull/705)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Conditional content for markdown vs HTML for README ([#694](https://github.com/fastai/nbdev/pull/694)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Export a single module ([#652](https://github.com/fastai/nbdev/issues/652))

### Bugs Squashed

- Re-enable Mac CI [#425](https://github.com/fastai/nbdev/issues/425))


## 2.0.6

### New Features

- new jupyter save hook to clean NBs ([#697](https://github.com/fastai/nbdev/issues/697)), thanks to [@seeM](https://github.com/seeM)
- new directive `exec_doc` to auto-exec cell when building docs ([#699](https://github.com/fastai/nbdev/issues/699))
- automatically escape YAML strings for title and description in frontmatter ([#691](https://github.com/fastai/nbdev/issues/691))
- add `unbump` param to `nbdev_bump_version` ([#689](https://github.com/fastai/nbdev/issues/689))
- install ghapi automatically ([#690](https://github.com/fastai/nbdev/issues/690))


## 2.0.5

### New Features

- add `nbdev_readme` ([#688](https://github.com/fastai/nbdev/issues/688))


## 2.0.4

### New Features

- add `readme_nb` config option ([#668](https://github.com/fastai/nbdev/issues/668))

### Bugs Squashed

- `exporti` cells can cause showdocs exec to fail ([#679](https://github.com/fastai/nbdev/issues/679))
- missing .html suffix in links ([#674](https://github.com/fastai/nbdev/issues/674))
- Add early return ([#670](https://github.com/fastai/nbdev/pull/670)), thanks to [@dleen](https://github.com/dleen)


## 2.0.0

- From-scratch rewrite of nbdev! nbdev now uses [Quarto](https://quarto.org/) to create beautiful and full-featured websites
- nbdev2 is much faster than previous versions
- Note that you should run `nbdev_migrate_directives` after upgrading to use the new comment directive format (e.g `#| export` instead of `#export`)


## 1.2.11

### New Features

- support py310 style union annotations ([#636](https://github.com/fastai/nbdev/pull/636)), thanks to [@seeM](https://github.com/seeM)

### Bugs Squashed

- fix `show_doc` for properties ([#635](https://github.com/fastai/nbdev/pull/635)), thanks to [@seeM](https://github.com/seeM)
- `nbdev_nb2md` throws error when called in a notebook ([#381](https://github.com/fastai/nbdev/issues/381))


## 1.2.10

### New Features

- Added webrick spec to Gemfile. ([#615](https://github.com/fastai/nbdev/pull/615)), thanks to [@MarkB2](https://github.com/MarkB2)
- Change doc() default for docments ([#611](https://github.com/fastai/nbdev/pull/611)), thanks to [@muellerzr](https://github.com/muellerzr)
- Better checks for cls and self ([#596](https://github.com/fastai/nbdev/pull/596)), thanks to [@muellerzr](https://github.com/muellerzr)
- Use the kernel defined in the kernelspec ([#594](https://github.com/fastai/nbdev/pull/594)), thanks to [@dleen](https://github.com/dleen)
- Add in repr for delegates ([#589](https://github.com/fastai/nbdev/pull/589)), thanks to [@muellerzr](https://github.com/muellerzr)

### Bugs Squashed

- Keep module in name when getting the "qualname" ([#606](https://github.com/fastai/nbdev/pull/606)), thanks to [@muellerzr](https://github.com/muellerzr)
- Fix decimal bug ([#604](https://github.com/fastai/nbdev/pull/604)), thanks to [@muellerzr](https://github.com/muellerzr)
- Use the kernel defined in the kernelspec ([#594](https://github.com/fastai/nbdev/pull/594)), thanks to [@dleen](https://github.com/dleen)
- Misc bug fixes + tests ([#593](https://github.com/fastai/nbdev/pull/593)), thanks to [@muellerzr](https://github.com/muellerzr)


## 1.2.9

### New Features

- Implement `show_doc` for dataclass ([#622](https://github.com/fastai/nbdev/pull/622)), thanks to [@MarkB2](https://github.com/MarkB2)

### Bugs Squashed

- Fix show doc for object, class methods. ([#621](https://github.com/fastai/nbdev/pull/621)), thanks to [@v-ahuja](https://github.com/v-ahuja)
- Fix show doc for keywords. ([#619](https://github.com/fastai/nbdev/pull/619)), thanks to [@v-ahuja](https://github.com/v-ahuja)
- Including `@dataclass` breaks `nbdev_build_lib` ([#595](https://github.com/fastai/nbdev/issues/595))
- `nbdev_nb2md` throws error when called in a notebook ([#381](https://github.com/fastai/nbdev/issues/381))


## 1.2.7

### Bugs Squashed

- Don't build NBs with no `#default_exp`

## 1.2.6

### New Features

- `nbdev_build_libs` now works on a single file even without a `settings.ini` or any `#default_exp` cell
- Handle `#|` as directive prefix

### Bugs Squashed

- nbdev_nb2md throws error when called in a notebook ([#381](https://github.com/fastai/nbdev/issues/381))


## 1.2.5

### New Features

- Update dependencies


## 1.2.3

### Bugs Squashed

- Pin jinja2 due to deprecation bug in nbconvert

## 1.2.2

### New Features

- Update dependencies


## 1.2.1

### New Features

- Make sure docments have linking capability ([#585](https://github.com/fastai/nbdev/pull/585)), thanks to [@muellerzr](https://github.com/muellerzr)
- better logging for duplicate titles ([#584](https://github.com/fastai/nbdev/pull/584)), thanks to [@hamelsmu](https://github.com/hamelsmu)

### Bugs Squashed

- Fix repr issue with `show_doc` ([#588](https://github.com/fastai/nbdev/pull/588)), thanks to [@muellerzr](https://github.com/muellerzr)


## 1.2.0

- upgrade nbconvert dep to v6

## 1.1.23

### Bugs Squashed

- fix verbose flag

## 1.1.20

### New Features

- skip symlinks in recursive glob ([#515](https://github.com/fastai/nbdev/issues/515))


## 1.1.15

### Breaking Changes

- make recursive behavior for `nbdev_build_docs` consistent with `nbdev_build_lib` ([#467](https://github.com/fastai/nbdev/pull/467)), thanks to [@hamelsmu](https://github.com/hamelsmu)

### New Features

- Allow for a one-time only (potentially) .py -> .ipynb generation ([#369](https://github.com/fastai/nbdev/issues/369))

### Bugs Squashed

- Images with `attachment:` break export ([#501](https://github.com/fastai/nbdev/pull/501)), thanks to [@yacchin1205](https://github.com/yacchin1205)
- Docs nav doesn't work on gitlab ([#488](https://github.com/fastai/nbdev/pull/488)), thanks to [@tcapelle](https://github.com/tcapelle)
- clean up all instances of recursive ([#470](https://github.com/fastai/nbdev/pull/470)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- After 'conda install -c fastai nbdev', error "`HTMLExporter` object has no attribute `template_path`" ([#431](https://github.com/fastai/nbdev/issues/431))


## 1.1.13

### New Features

- support windows ([#392](https://github.com/fastai/nbdev/pull/392)), thanks to [@mszhanyi](https://github.com/mszhanyi)
- `nbdev_new`: get template from latest release asset ([#382](https://github.com/fastai/nbdev/pull/382)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Add more license options

### Bugs Squashed

- Fix recursive flag ([#433](https://github.com/fastai/nbdev/pull/433)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- conda not installing nbdev properly on WSL2 ([#430](https://github.com/fastai/nbdev/issues/430))
- fix nb2md ([#424](https://github.com/fastai/nbdev/pull/424)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- `nbdev_build_lib` seems to convert more notebooks than expected ([#423](https://github.com/fastai/nbdev/issues/423))
- fix default arg issue with `nbdev_update_lib` ([#416](https://github.com/fastai/nbdev/pull/416)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- `nbdev_update_lib` errors out when fname not supplied ([#415](https://github.com/fastai/nbdev/issues/415))
- `nbdev_new` fails on calling the GitHub API without guidance ([#404](https://github.com/fastai/nbdev/issues/404))
- fix recurse issue ([#391](https://github.com/fastai/nbdev/pull/391)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- `nbdev_build_docs`----ModuleNotFoundError: No module named 'fastcore' ([#390](https://github.com/fastai/nbdev/issues/390))
- `nbdev_test_nbs` --fname broke in 1.1.7 ([#388](https://github.com/fastai/nbdev/issues/388))
- set recursive=True for docs ([#387](https://github.com/fastai/nbdev/pull/387)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- fix url for getting branch ([#386](https://github.com/fastai/nbdev/pull/386)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- `nbdev_nb2md` throws error when called in a notebook ([#381](https://github.com/fastai/nbdev/issues/381))


## 1.1.12

### New Features

- `nbdev_new` should grab files from a release asset in `nbdev_template` ([#383](https://github.com/fastai/nbdev/issues/383))
- Use Jekyll Theme instead of vendoring all required files ([#379](https://github.com/fastai/nbdev/issues/379))
- Create relevant directories in `docs/_data` if do not already exist ([#377](https://github.com/fastai/nbdev/issues/377))


## 1.1.6

### New Features

- Clean Google Colab metadata and line endings ([#364](https://github.com/fastai/nbdev/pull/364)), thanks to [@muellerzr](https://github.com/muellerzr)
- add ability to find notebooks recursively ([#359](https://github.com/fastai/nbdev/pull/359)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- Add `bare` flag to `nbdev_build_lib` ([#336](https://github.com/fastai/nbdev/issues/336))
- install git hooks in `nbdev_new` ([#308](https://github.com/fastai/nbdev/issues/308))
- `nbdev_new` now works on an existing cloned repo, instead of creating a new repo ([#307](https://github.com/fastai/nbdev/issues/307))

### Bugs Squashed

- `nbdev_update_lib --fname notebook.ipynb` crashes (while `nbdev_update_lib` works) ([#341](https://github.com/fastai/nbdev/issues/341))
- Copy new files only if they don't exist for nbdev_new ([#309](https://github.com/fastai/nbdev/issues/309))


## 1.1.3

### New Features

- Place source code below heading on #exports ([#265](https://github.com/fastai/nbdev/pull/265)), thanks to [@hamelsmu](https://github.com/hamelsmu)


## 1.1.2

### Bugs Squashed

- update fastcore requirement ([#281](https://github.com/fastai/nbdev/issues/281))


## 1.1.1

### New Features

- Make CLI faster by removing unneeded imports and moving CLI commands to source modules ([#271](https://github.com/fastai/nbdev/issues/271))
- Move `Config` to fastcore ([#280](https://github.com/fastai/nbdev/issues/280))

## 1.1.0
### Breaking Changes

- Remove magics ([#269](https://github.com/fastai/nbdev/issues/269))
- Removed callbacks ([#253](https://github.com/fastai/nbdev/pull/253)), thanks to [@pete88b](https://github.com/pete88b)
- move conda packager to `fastrelease` ([#252](https://github.com/fastai/nbdev/issues/252))

### New Features

- Place source code below heading on #exports ([#265](https://github.com/fastai/nbdev/pull/265)), thanks to [@hamelsmu](https://github.com/hamelsmu)
- always skip cells labeled "skip" in test ([#257](https://github.com/fastai/nbdev/issues/257))

## 1.0.17

### Bugs Squashed

- restrict nbconvert<6 to avoid upgrade problems ([#249](https://github.com/fastai/nbdev/issues/249))

## 1.0.16

### Bugs Squashed

- When generating docs, import cells are run even if not exported ([#248](https://github.com/fastai/nbdev/issues/248))

## 1.0.15

### New Features

- add option to not exec nb for fastpages ([#244](https://github.com/fastai/nbdev/issues/244))
- Enable Codespaces for nbdev ([#243](https://github.com/fastai/nbdev/issues/243))

### Bugs Squashed

- Fix: correct notebook2html path operation for Windows. ([#239](https://github.com/fastai/nbdev/issues/239))

## 1.0.13

### New Features

- remove numpy conda dep and update to fastcore 1.0.5 ([#241](https://github.com/fastai/nbdev/issues/241))

### Bugs Squashed

- allow nbdev imports when not in an nbdev project ([#238](https://github.com/fastai/nbdev/issues/238))

## 1.0.10

### New Features

- Magic flags for tests ([#232](https://github.com/fastai/nbdev/pull/232))
- Add ability to have Colab badges on pages ([#210](https://github.com/fastai/nbdev/pull/210))
- Support for `doc_path` ([#235](https://github.com/fastai/nbdev/pull/235))

### Bugs Squashed

- Remove colab vendor specific tags which cause `nbdev_build_docs` to fail ([#207](https://github.com/fastai/nbdev/pull/207))
- hooks folder inside .git must be manually created before `nbdev_install_git_hooks` ([#230](https://github.com/fastai/nbdev/pull/230))
- updates to how backtick names are converted to doc links ([#218](https://github.com/fastai/nbdev/pull/218))

## Version 1.0.0

- Initial release


