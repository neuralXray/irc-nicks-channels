## Find Nicks and Chanels

Find nicks that have been connected with a given ident or ip, the channels where they have been and the first and last seen datetime.


## Installation

```
mkdir irc-nicks-channels
cd irc-nicks-channels
git clone https://github.com/neuralXray/irc-nicks-channels.git
```

## Execute

Set the parent location of the irc logs at `nicks_channels.config.example`, and rename to `nicks_channels.config`. The assumed structure is as follows: `irc.server.com/year-month/#channel.log`.

Log format parameters at the upper part of script `utils.py`.

```
python3 nicks_channels.py irc.server.com nick ident ip [months=1]
```

## Support the developer

* Bitcoin: 1GDDJ7sLcBwFXg978qzCdsxrC8Ci9Dbgfa
* Monero: 4BGpHVqEWBtNwhwE2FECSt6vpuDMbLzrCFSUJHX5sPG44bZQYK1vN8MM97CbyC9ejSHpJANpJSLpxVrLQ2XT6xEXR8pzdCT
* Litecoin: LdaMXYuayfQmEQ4wsgR2Tp6om78caG3TEG
* Ethereum: 0x7862D03Dd9Dd5F1ebc020B2AaBd107d872ebA58E
* PayPal: paypal.me/neuralXray

