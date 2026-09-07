# AGENTS.md

## Link checking

LinkChecker takes ~50s to run. Do not pipe its output directly to `grep` or other
filters in a single command, as the shell will block until completion. Instead,
write output to a log file first, then process the log file. This also saves time
when you need to change the processing command — you can re-run the grep/sort on
the existing log file instead of re-running LinkChecker each time.

```bash
./linkchecker.py /tmp/linkchecker-output.log
grep "Result" /tmp/linkchecker-output.log | sort | uniq -c | sort -rn
```

To also produce a list of ignored URLs for manual checking:
```bash
./linkchecker.py /tmp/linkchecker-output.log --ignored /tmp/ignored-urls.log
cat /tmp/ignored-urls.log
```
