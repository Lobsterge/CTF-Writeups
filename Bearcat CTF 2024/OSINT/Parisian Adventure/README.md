# Parisian Adventure [OSINT]

### Challenge:
Can you find the Google Maps Plus code for this location? Submit flag in the form BCCTF{4GJ3+W5 Cincinnati, Ohio}
##### Files: [is_it_paris.png](is_it_paris.png)

### Solution:
We can find the GPS position of where the photo was taken from the exif metadata:

```bash
$ exiftool is_it_paris.png
GPS Position                    : 22 deg 8' 39.00" N, 113 deg 33' 47.00" E
```

Using the coordinates we can find the place on [google maps](https://www.google.com/maps/place/22%C2%B008'39.0%22N+113%C2%B033'47.0%22E/).

Flag: ```BBCTF{4HV7+M67 Cotai, Macao}```