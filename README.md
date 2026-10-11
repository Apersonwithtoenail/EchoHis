# EchoHis

Time-capsule shell. Shows what you typed | days / months / years ago.

## Install

```bash
./install.sh
```

## Use

```bash
echoterm -d 1            # 1 day ago
echoterm -m 1            # 1 month ago
echoterm -y 1            # 1 year ago
echoterm -m 6 -w 7200    # 6 months ago, +/- 2h window
```

## Requires timestamps

Add to `~/.bashrc`:

```bash
export HISTTIMEFORMAT="%F %T "
```

Then restart shell. Without this, `z/.bash_history` has no dates.
