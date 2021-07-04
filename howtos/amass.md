# Amass

## Download:

https://github.com/OWASP/Amass

## Nutzung:

```
amass intel -whois -d domain.com -dir results/domain
amass enum -active -d domain.com -dir results/domain_subs
```

Achtung: Bei `-active` kann dein Netzwerk temporär nicht mehr reagieren. Nutze dann besser `-passive`.