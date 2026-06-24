# Third-party licensing report

**Review date:** 2026-06-23  
**Status:** provisional candidate review; not a final SBOM or legal opinion

No exact dependency lock exists, so transitive dependencies, bundled native libraries, notices, and source/relinking obligations cannot be finalized. Exact locked artifacts and included license files must be reviewed.

| Component | Candidate license | Key issue | Status |
|---|---|---|---|
| CPython | PSF | include applicable notices and embedded-component review | provisional |
| PySide6/Qt | LGPL-3.0-only OR GPL alternatives in package metadata | preserve LGPL replacement/relinking rights, notices, and review actual Qt modules/plugins; avoid GPL-only modules without approval | blocking review |
| pyqtgraph | MIT | retain notice | provisional |
| Pydantic | MIT | verify exact artifact | provisional |
| SQLAlchemy/Alembic | MIT | retain notices | provisional |
| PyArrow/Arrow | Apache-2.0 | include LICENSE/NOTICE and review bundled compression/native libraries | provisional |
| DuckDB | MIT | retain notice and inspect bundled extensions/runtime | provisional |
| pytest | MIT | development-only classification | provisional |
| Hypothesis | MPL-2.0 | file-level copyleft implications if modifying covered source; customer OSS policy needed | blocking policy confirmation |
| OpenTelemetry | expected Apache-2.0 | exact packages/versions unresolved | deferred |
| Protobuf or MessagePack | unresolved selection | compare bindings/runtime licenses and footprint | Gate 1 decision |
| Windows credential binding | unresolved selection | prefer direct OS APIs/minimal dependency; verify maintenance/license | blocking |

The customer has not selected a project license. `pyproject.toml` therefore states all rights reserved/project license not yet selected. This must be resolved before external distribution or contribution.

Final release process must generate CycloneDX or SPDX SBOM from the exact hashed Windows lock and installed environment, including Python packages, wheel hashes, native DLLs/bundled libraries, Qt modules/plugins, source/provenance, license expressions, vulnerability scan timestamp, and review disposition. The build must reject floating/unhashed runtime dependencies, unknown/disallowed licenses, unmitigated critical vulnerabilities, and provenance mismatches. Produce third-party notices and required license/source/relinking instructions.

Decision: **PROVISIONAL/BLOCKING**. No distribution approval is granted.
