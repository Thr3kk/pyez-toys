# Update SRX IP-IP tunnel endpoint IP address Utility

At home, I use an IP-IP tunnel to Hurricane Electric to get IPv6 connectivity (grumble, grummble, hey Verizon, what happened to "soon???"). It works very well, but has the minor problem of needing to update the local tunnel endpoint address in the ip-0/0/0.0 IFL any time my WAN IP changes (Yeah, I'm not bucking up for static IPs at home).

Naturally, like many others before me, I use DDNS as a means to keep an up-to-date A record out there for various purposes. I update that using ddclient, running in a Linux VM. I've recently discovered that ddclient also allows a "postscript" option, which will execute a command of my choosing, with the new public IP provided on as an argument to the script. You'll want to configure your DDNS update client to also update the Tunnelbroker end of the tunnel. It was super easy to add a second update stanza to my ddclient.conf file, which allowed me to update Tunnelbroker at the same time I update my other DDNS provider.

This script picks up sys.argv\[1\], which of course is the new IP, and then fills in a Jinja2 template, pushing the resulting config out to the SRX, and boom, v6 tunnel re-establishes automagically.
