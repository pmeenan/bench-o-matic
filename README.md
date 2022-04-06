# bench-o-matic
Automate running browserbench.org benchmarks

## MacOS
Dependencies:

```bash
sudo chown -R $(whoami) /usr/local/bin /usr/local/etc /usr/local/sbin /usr/local/share /usr/local/share/doc
chmod u+w /usr/local/bin /usr/local/etc /usr/local/sbin /usr/local/share /usr/local/share/doc
brew install python3 pip3 chromedriver geckodriver
pip3 install selenium psutil
sudo safaridriver --enable
```