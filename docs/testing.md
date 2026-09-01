# Testing

Run the targeted HOOT suites separately:

```sh
scripts/test.sh js-utils
scripts/test.sh js-interaction
scripts/test.sh js-builder-cleanup
```

`scripts/test.sh checkpoint-b3` runs the isolated browser suites and Python module tests. The runner rejects an unsupported descriptor and never falls back to the global Odoo HOOT suite.

The backend leg excludes the HOOT class because the three descriptor legs run
it separately; this prevents Odoo's Chrome post-success process linger from
blocking the remaining real-browser tests.
