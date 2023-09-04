# Deleted Message
![challenge](challenge.png)
### Challenge:
##### Cyber Police have seized a computer containing illegal content, but the data stored is secured with a password.

##### A member of the criminal organization owning the computer was arrested. Police suspect that the password was sent to the criminal via SMS, but the message was deleted right before the arrest.

##### You’re given a dump of the data partition of the phone (running Android 6.0). Your job as the forensic specialist is to recover the deleted password.

##### FIles: [data.tar.gz](data.tar.gz)

### Solution:
Literally just grep the file lol

```bash
$ grep --text uctf{ -r
data/com.google.android.gms/databases/icing-indexapi.db:text"uctf{l057_1n_urm14}�
data/com.google.android.gms/databases/icing-indexapi.db:
dateReceived�������٦uctf{l057_1n_urm14}���D�unreadinbox
```

Flag: ```uctf{l057_1n_urm14}```
