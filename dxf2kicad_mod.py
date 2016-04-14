# refer to http://pythonhosted.org/dxfgrabber/#
# Note that there must not a line or shape overlapped
import dxfgrabber 
import math
import sys
global debug 
global distance_error
global body_head
global body_end
global fp_poly_head
global fp_poly_end

debug = 0
distance_error = 1e-2
body_head = "\n\
(module dxfgeneratedcopper (layer F.Cu) (tedit 0) \n\
  (fp_text reference G*** (at 0 -4) (layer F.SilkS) hide \n\
    (effects (font (thickness 0.2))) \n\
  ) \n\
  (fp_text value value (at 0 4) (layer F.SilkS) hide \n\
    (effects (font (thickness 0.2))) \n\
  ) "

body_end = "\n)"

fp_poly_head =   "(fp_poly \
  (pts "
fp_poly_end_1 = " ) \n\
	(layer "

fp_poly_end_2 = " ) (width 0.001)) "

def	get_start_end_pts(entity):
	if "LINE" == entity.dxftype:
		if debug:
			print  >>sys.stderr,"LINE ", entity.start, entity.end
		return (entity.start,entity.end)
	elif "ARC" == entity.dxftype:
		start = ( entity.center[0] + entity.radius * math.cos(entity.startangle/180*math.pi), \
			entity.center[1] + entity.radius * math.sin(entity.startangle/180*math.pi), 0)
		end = ( entity.center[0] + entity.radius * math.cos(entity.endangle/180*math.pi), \
			entity.center[1] + entity.radius * math.sin(entity.endangle/180*math.pi), 0)
		if debug:
			print  >>sys.stderr,"ARC ", start, end
		return (start,end)
	else:
		print >>sys.stderr, "[Error]: Unexpceted dxftype ",  entity.dxftype 
		
		
def print_points(ety,direction):

	points = []
	if 'LINE' == ety.dxftype:
		points = [ety.start,ety.end]
	elif 'ARC' == ety.dxftype:
		step = 1.0/ety.radius
		angle = ety.startangle
		
		if debug:
			print >>sys.stderr,"angle", ety.startangle, ety.endangle
		
		if (ety.startangle > ety.endangle):
			ety.endangle += 360
		while (1):
			points.append( (ety.center[0] + ety.radius * math.cos(angle/180*math.pi), \
			ety.center[1] + ety.radius * math.sin(angle/180*math.pi)))
			angle +=  step
			
			if (angle > ety.endangle):
				break
	else:
		print "[Error]: Unexpceted dxftype ",  entity.dxftype

	if direction == -1:
		points.reverse()
	
	for point in points:
		print "(xy ", point[0]," ", -point[1],")" #in KiCad Y axis has opposite direction
	

def start_new_shape():
	global current_shape,points,point_to_close,pts_next
	if len(not_processed_data) >0:
		current_shape = not_processed_data.pop();#pick up one
		points = get_start_end_pts(current_shape)
		point_to_close = points[0];
		pts_next =points[1];
		
		if debug:
			print >>sys.stderr,"starting point",point_to_close
		print fp_poly_head
		print_points(current_shape,1)
	
#dxf = dxfgrabber.readfile("test4-R2000-2002.dxf")
dxf = dxfgrabber.readfile(sys.argv[1])

if debug:
	print >>sys.stderr,"DXF version: {}", dxf.dxfversion
header_var_count = len(dxf.header) # dict of dxf header vars
layer_count = len(dxf.layers) # collection of layer definitions
block_definition_count = len(dxf.blocks) #  dict like collection of block definitions
entity_count = len(dxf.entities) # list like collection of entities
if debug:
	print >>sys.stderr,"Entity Count:"
	print >>sys.stderr,entity_count

layers = set([entity.layer for entity in dxf.entities])
if debug:
	print >>sys.stderr,layers



print body_head


for layer in layers:

	not_processed_data = set([entity for entity in dxf.entities if entity.layer == layer])

	pts_next = None
	pts = None

	start_new_shape()

	if debug :
		print >>sys.stderr,"Not Processed Shape: ", len(not_processed_data)

	while (1):

		if pts_next == None:
			if debug:
				print >>sys.stderr, "pts_next is None"
			break #stop 
		pts = pts_next
		
		if debug:
			print >>sys.stderr,"Searching entity which is connected with ", pts
		#get_start_end_pts(current_shape)
		matched_entity = None
		pts_next = None
		for entity in not_processed_data:
			points = get_start_end_pts(entity)
			x = points[0][0]
			y = points[0][1]
			if (math.fabs(x-pts[0]) < 5e-2) and (math.fabs(y-pts[1]) < 5e-2):
				#matched
				matched_entity = entity
				direction = 1 #from start to end
				pts_next = points[1]
				if debug:
					print >>sys.stderr,"Got the Point", x, y
				break;
			x = points[1][0]
			y = points[1][1]
			if (math.fabs(x-pts[0]) < distance_error) and (math.fabs(y-pts[1]) < distance_error):
				#matched
				matched_entity = entity
				direction = -1 #from end to start
				pts_next = points[0]
				if debug:
					print >>sys.stderr,"Got the Point", x, y
				break;
				
		
		if matched_entity == None:
			
			if debug:
				print >>sys.stderr,"No matching found, check if we could close the loop"
				
			if (math.fabs(point_to_close[0]-pts[0]) < distance_error) and \
				(math.fabs(point_to_close[1]-pts[1]) < distance_error):
				if debug:
					print >>sys.stderr,"shape closed at", pts
				print "(xy ", pts[0]," ", -pts[1],")" 
				print fp_poly_end_1, layer, fp_poly_end_2
						
				#find next shape
				start_new_shape()
					
				if debug :
					print >>sys.stderr,"Not Processed Shape: ", len(not_processed_data)
			else:
				print >>sys.stderr, "[Error] unconnected Point:",pts ," on layer", layer
				print >>sys.stderr, "        there may be overlapped lines or arcs or unclosed shape, please double check the dxf file"
				
				break;
		else:
			if debug:
				print >>sys.stderr, "now print the line on,", matched_entity
			print_points(matched_entity,direction)
			if debug:
				print >>sys.stderr, "removed from the set,", matched_entity
			not_processed_data.remove(matched_entity) #remove from the set
			
			if debug :
				print  >>sys.stderr,"Not Processed Shape: ", len(not_processed_data)
				
print body_end