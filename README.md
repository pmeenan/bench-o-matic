# bench-o-matic
Automate running browserbench.org benchmarks

Params:
* `-r,--runs`: Number of runs. i.e. `python3 bom.py --runs 100`

## MacOS
Requires Python 3 native to the system CPU architecture (from brew is an option).

```bash
python3 -m pip install selenium psutil webdriver-manager requests
```

Also need to enable safaridriver support
```
sudo safaridriver --enable
```