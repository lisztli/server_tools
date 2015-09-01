# FR_Proxy

## What does 「FR_Proxy 」 stand for?

Fxxk Relay Proxy!

Our servers are all hide after the relay machines, which need the RSA Token when you are connected.
So I will write a proxy just to bypass the relay machines.


## Does the 「port foward」or modify sshd_config work?

No. The security team will scan the ports on the machine, and send you an email about this unsecured behaive.

### How does the fr_proxy work?

just like this:

```
+-----------+       +-------------+              +----------------+      +-------------+
|           |       |             |              |                |      |             |
|  ssh      +-------> FR_Client   +--------------> FR_Server      +------> SSHD        |
|  127.0.0.1|       | bind 8627   |              |                |      | Port 22     |
|  +p 8627  |       |             |              |                |      |             |
|           |       |             |              |                |      |             |
+-----------+       +-------------+              +----------------+      +-------------+

```

## Does fr_proxy safe?

Yes. The crawler of security team will never found the FR_Server is a ssh proxy.

## Usage

### The Server

```Bash
./fr_server -h 127.0.0.1 -p 8627
```

### The Client
```Bash
# ./fr_client -h bind_ip -p bind_port -s server_host:port -t ssdh_host:port
./fr_client -h 127.0.0.1 -p 8627 -s 127.0.0.1:8627 -t10.11.12.13:22
ssh user@127.0.0.1 -p 8627
```
