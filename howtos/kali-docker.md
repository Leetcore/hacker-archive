# Kali Linux in einem Docker Container

Zuerst muss Docker auf deinem System installiert sein.

Kali Linux aus dem Docker Hub ziehen und mit `docker run` starten. Durch `--rm` wird der Container danach wieder gelöscht.

```bash
docker pull kalilinux/kali-rolling
docker run --rm -ti kalilinux/kali-rolling /bin/bash
```

In Kali:
```bash
apt update
apt install kali-tools-top10
```
-v 
--mount src=kali-root,dst=/root --mount src=kali-postgres,dst=/var/lib/postgresql
