# Windows and Python compatibility matrix

**Review date:** 2026-06-23  
**Status:** provisional; no clean-Windows test

Python **3.14.6 x64** is the newest stable CPython release identified during Gate 0 and is the provisional `.python-version` candidate. The engineering runtime used for document validation was Linux/Python 3.13.5, so it is not Windows or selected-version evidence.

| Platform | Status | Required evidence |
|---|---|---|
| Windows 11 x86-64 | candidate, untested | exact supported build/edition, clean VM setup, UI/IPC/DPAPI/long-path tests |
| Windows Server x86-64 | not selected | explicit customer requirement and service/session/desktop tests |
| Windows ARM64 | unsupported pending review | native dependency/UI wheel and performance evidence |
| Linux/macOS | research only | never counts as Windows release evidence |

| Component | Current support signal | License | Decision |
|---|---|---|---|
| CPython 3.14.6 | current stable release | PSF | provisional candidate |
| PySide6 6.11.1 | Python >=3.10,<3.15; Python 3.14 classifier; Windows x64 ABI3 wheel | LGPL-3.0-only OR GPL alternatives | candidate; obligations blocking review |
| PyArrow 24.0.0 | documented Windows and Python 3.10–3.14 support | Apache-2.0 | candidate |
| DuckDB 1.5.4 | Python >=3.10; CPython 3.14 Windows x64 wheel observed | MIT | candidate |
| SQLAlchemy 2.0.51 | CPython 3.14 Windows x64 wheel observed | MIT | candidate |
| Alembic 1.18.4 | Python >=3.10 metadata; clean install not run | MIT | candidate |
| pyqtgraph 0.14.0 | Python >=3.10, pure Python; marked beta | MIT | candidate with maturity risk |
| Pydantic/pytest/Hypothesis | modern Python support indicated; exact versions unresolved | MIT/MIT/MPL-2.0 | candidate; exact lock required |
| Windows credential binding | not selected | unresolved | blocking |
| IPC/binary schema | not selected | unresolved | Gate 1 ADR |

Exact direct/transitive dependencies shall be locked with hashes only after a clean Windows resolver/install trial. Package metadata is not execution proof. Evidence must record Windows build, architecture, Python installer provenance/hash, lock hash, package/wheel provenance, Visual C++ runtime state, UI/high-DPI, DPAPI/Credential Manager, SQLite WAL, Parquet/DuckDB, IPC, supervision, crash recovery, backup/restore/update/rollback, and Windows tests.

Current status: `python_compatibility=PROVISIONAL`, `windows_compatibility=NOT_TESTED`, `live_trading=LOCKED`.

Sources: Python downloads, PySide6/Qt for Python, PyArrow installation, DuckDB, SQLAlchemy, Alembic, pyqtgraph, Pydantic, pytest, and Hypothesis official project/package metadata reviewed 2026-06-23.
