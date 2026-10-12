# EchoHis

Time-capsule shell. Shows what you typed N days / months / years ago.

## Install

```bash
git clone https://github.com/Apersonwithtoenail/EchoHis.git
cd EchoHis
./install.sh
```

## Use

```bash
echoterm -d 1            # 1 day ago
echoterm -m 1            # 1 month ago
echoterm -y 1            # 1 year ago
echoterm -m 6 -w 7200    # 6mo ago, +/- 2h
echoterm -d 0 -f git      # today, only "git" commands
echoterm -s git          # search ALL history
echoterm --on 2026-10-11   # specific date
echoterm --top            # most-used commands
echoterm --random         # random moment
```

## Requires timestamps

Add to `~/.bashrc`:

```bash
export HISTTIMEFORMAT="%F %T "
```

Restart shell. Without this, `~/.bash_history has no dates.

## License

MIT
