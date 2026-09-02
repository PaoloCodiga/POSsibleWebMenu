# Testing

Run the targeted HOOT suites separately:

```sh
scripts/test.sh js-utils
scripts/test.sh js-interaction
scripts/test.sh js-builder-cleanup
scripts/test.sh js-builder-configuration
```

`scripts/hoot.sh` runs the complete project HOOT matrix. It loads only the
project modules and never falls back to the global Odoo HOOT suite.

`scripts/test.sh checkpoint-b3` runs the historical B3 isolated browser suites
and Python module tests. The release additionally runs the C3 real-Chrome tour
from a fresh installed database, then verifies a separate module update.

The backend leg excludes the HOOT class because the targeted HOOT matrix runs
it separately; this prevents duplicate browser-suite execution.
