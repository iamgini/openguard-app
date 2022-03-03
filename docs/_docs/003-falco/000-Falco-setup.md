# Falco configs


## Installing Falco
https://falco.org/docs/getting-started/installation/

```shell
## Trust the falcosecurity GPG key, configure the apt repository, and update the package list:
curl -s https://falco.org/repo/falcosecurity-3672BA8F.asc | apt-key add -
echo "deb https://download.falco.org/packages/deb stable main" | tee -a /etc/apt/sources.list.d/falcosecurity.list
apt-get update -y

## Install kernel headers:
apt-get -y install linux-headers-$(uname -r)

##Install Falco:
apt-get install -y falco

## start falco
systemctl start falco
systemctl status falco
```

## Uninstall Falco

```shell
apt-get remove falco
```


## Falco rules

https://securityhub.dev/falco-rules/file-integrity-monitoring


```yaml
## /etc/falco/falco_rules.local.yaml


- rule: Detect File Permission or Ownership Change
  desc: detect file permission/ownership change
  condition: >
    spawned_process and proc.name in (chmod, chown) and proc.args contains "/tmp/"
  output: >
    File below a known directory has permission or ownership change (user=%user.name
    command=%proc.cmdline file=%fd.name parent=%proc.pname pcmdline=%proc.pcmdline gparent=%proc.aname[2])
  priority: WARNING
  tags: [filesystem]
```


https://falco.org/blog/falco-security-audit/


## Configure Falco Alerts

```yaml
## /etc/falco/falco.yaml

## configure http_output to openguard api
http_output:
  enabled: True
  url: http://192.168.56.1:8000/app/api/incident_report/
  user_agent: "falcosecurity/falco"

## configure json_output
# Whether to output events in json or text
json_output: true
```
 