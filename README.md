# `dxf2kicad_mod`

Create `Kicad` footprint from `DXF` file. This simple and dirty script was
designed for my own purpose a few years back. At that time, I was using `Kicad`
to design a simple PCB, but the shape of footprint could not be designed using
`Kicad` footprint design tool. A workaround is to create the shape in CAD tools
and convert it to the `Kicad` footprint format. Hence this work was a bit of
hacking.

## How it works

It will read the `DXF` file and find lines and arcs (only supporting these two
types so far) which compose a close-loop graphic, it converts arcs to lines and
connected all lines together using `fp_poly` command in `kicad_mod` file. Each
layer is handled separately, the layer name is converted to layer name in
`kicad_mod` file.

## Limitations

* it only support lines and arcs so far, but it could fulfill my requirement so
  far. In the future, I may add more shape support (by converting the shapes to
  lines)
* each line must connect with another line or arc's beginning or end point very
  precisely, as the algorithm searches the points location only. If it is
  overlapped, it will fail to find the connecting point but it will provide some
  hint to tell you where it is lost, you may check the location if it is
  overlapped or not connected well.
* There must not be a line or arc on top another lines in the same layer due to
  the same reason above. Sometimes, people draws two lines on the same location,
  and it very hard to find where. Again the message in command line will provide
  some hints for you.


## how to use
### install python
### install `dxfgrabber`

```
https://github.com/mozman/dxfgrabber.git
```

### create `DXF` file using `autocad ` or `draftsight`
### using following command line to generate `kicad_mod`

```
python dxf2kicad_mode "Your-dxf-file-name-here" > "your kicad_mod file.kicad_mod"
```
