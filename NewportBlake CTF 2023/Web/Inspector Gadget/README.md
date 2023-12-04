# Inspector Gadget
![challenge](challenge.png)
### Challenge:
##### While snooping around this website, inspector gadet lost parts of his flag. Can you help him find it?

##### Links: [inspector-gadget.chal.nbctf.com](inspector-gadget.chal.nbctf.com)

### Solution:

Flag is hidden in 4 parts of the website:

Part 1:
```bash
curl https://inspector-gadget.chal.nbctf.com/gadgetmag.html | grep nbc
    <title>Flag Part 1/4:nbctf{G00d_</title>
```

Part 2:
```bash
curl https://inspector-gadget.chal.nbctf.com/supersecrettopsecret.txt
Flag Part 2/4:
J06_
```

Part 3:
```bash
curl https://inspector-gadget.chal.nbctf.com/ | grep Flag
    <img src="Krooter Gadget.jpg" alt="Flag Part 3/4: D3tect1v3_">

```

Part 4:
```bash
$ curl https://inspector-gadget.chal.nbctf.com/robots.txt
User-agent: *
Disallow: /mysecretfiles.html

$ curl https://inspector-gadget.chal.nbctf.com/mysecretfiles.html | grep flag
    <p>Here's part of the flag for your troubles, part 4/4 G4dg3t352}</p>
```

Flag: ```nbctf{G00d_J06_D3tect1v3_G4dg3t352}```