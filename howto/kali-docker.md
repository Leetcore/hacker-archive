# Prepare Kali Linux docker container

TODO: https://medium.com/@airman604/kali-linux-in-a-docker-container-5a06311624eb

Steps to put kali linux in a docker container:

You have to install docker. After that:

```bash
docker pull kalilinux/kali-rolling
docker run -ti kalilinux/kali-rolling /bin/bash
```

```bash
apt update
apt dist-upgrade
apt autoremove
apt clean
```

```bash
apt install kali-tools-top10
```


--mount src=kali-root,dst=/root --mount src=kali-postgres,dst=/var/lib/postgresql


```bash
docker ps -a

docker commit <CONTAINER ID> kali
```

docker run -ti --rm kali /bin/bash

```bash
apt update  
apt upgrade
apt install man sqlmap tor proxychains kali-tools-top10
```