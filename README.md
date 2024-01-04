# Desmos Bezier Art

### a small collection of tools I used to create outlined images on desmos

## running

the python code is not very optimized for performance since it relies on a pure python port of [potrace](https://github.com/tatarize/potrace)

> If speed is a requirement for you, use the unix version and the original potrace library
> If you are on windows and don't have access to a unix system, try wsl/wsl2

depending on your choice, install either `pypotrace numpy opencv-python` on unix or `pypotracer numpy opencv-python Pillow` on windows

## copy tool

crappy copy/paste tool specifically designed to help transfer the output txt file to desmos website.
desmos can't handle huge amount of copy and pasted text at once so its necessary to split it up.
one easy way to do that is to use my tool.
the python script will tell you how many line segments were written to the file, so use that as a hint for
what to set the bounds to.

```txt
usage: copytool.exe <filename> <start> <end>

       both <start> and <end> are 0 based inclusive indices for the line segments
       ex. 0 1 copies the first two segments, 2 4 the next three
```

(this mini project was used in a desmos art competition for my calculus class)
here are some examples
![trick](https://www.desmos.com/calculator/jxbegj9lg6)
![popcat](https://www.desmos.com/calculator/g5b3kzajlq))
![santa](https://www.desmos.com/calculator/sevalhi0zk)
