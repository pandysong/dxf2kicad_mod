# dxf2kicad_mod
create kicad footprint from dxf file
## How it works
it will read the dxf file and find lines and arcs (only supporting thes two types so far) which compose a close-loop grahpic, it converts arcs to lines and connected all lines togethers using fp_poly command in kicad_mod file. each layer is handled seperately, the layer name is converted to layer name in kicad_mod file.
## limitations
* it only support lines and arcs so far, but it could fullfill my requirement so far. in the future, I may add more shape support (by converting the shapes to lines)
* each line must connect with another line or arc's begning or end point very precisely, as the algorithm searches the points location only. if it is overlapped, it will fail to find the connecting point but it will provide some hint to tell you where it is lost, you may check the location if it is overlapped or not connected well.
* there must not be a line or arc on top another lines in the same layer due to the same reason above. sometimes, people draws two lines on the same location, and it very hard to find where. again the message in command line will provide some hints for you.


## how to use
### install python
### install dxfgrabber
http://pythonhosted.org/dxfgrabber/#
### create dxf file using autocad or draftsight
### using following command line to generate kicad_mod
python dxf2kicad_mode "Your-dxf-file-name-here" > "your kicad_mod file.kicad_mod"
