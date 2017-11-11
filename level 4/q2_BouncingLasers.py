def answer(dimensions, captain_position, badguy_position, distance):
   from math import ceil, sqrt, pow, copysign
   from fractions import gcd

   def getSmallestVector(vec):
      # find the smallest form of the vector
      if vec[0] == 0:
         if vec[1] == 0:
            return (0,0)
         return (0,int(copysign(1,vec[1])))
      
      if vec[1] == 0:
            return (int(copysign(1,vec[0])),0)

      div = gcd(vec[0], vec[1]) * copysign(1,vec[1]) #gcd in python27 is incorrect
      return (int(vec[0]/div), int(vec[1]/div))
           
   def newpos(base_pos, frame_pos):
      # get the equivalent position of base_pos in frame frame_pos
      new_x = int(pow(-1, frame_pos[0])) * base_pos[0] +  dimensions[0] * (frame_pos[0]+(1 if frame_pos[0] % 2 == 1 else 0))
      new_y = int(pow(-1, frame_pos[1])) * base_pos[1] + dimensions[1] * (frame_pos[1]+(1 if frame_pos[1] % 2 == 1 else 0))
      return (new_x, new_y)
   
   def getVector(x, y, bp):
        # given a base position bp, get the vector from the captain to its position in frame (x,y)
        # i.e. shoot at it
        return (newpos(bp,(x, y))[0] - captain_position[0], newpos(bp,(x, y))[1] - captain_position[1])        

   max_x = int ( ceil( float(distance + captain_position[0]) / dimensions[0] ) ) + 1
   max_y = int( ceil( float(distance + captain_position[1]) / dimensions[1] ) ) + 1
   f = max(max_x, max_y) # we don't need to check frames any farther out than this

   
   # base solution = the solution from just shooting directly at the bad guy
   base_solution = getSmallestVector((badguy_position[0]-captain_position[0],badguy_position[1]-captain_position[1]))
   # set of vectors that hit the bad guy and the captain, respectively
   hit_me = set([])
   dont_hit_me = set([])
   
   #generate all possible positions
   for xval in range(f):
      for yval in range(f):
         
         # shoot at the bad guy and the captain. store those vectors.
         toBadGuy = [getVector(xval, yval, badguy_position), getVector(-xval, yval, badguy_position), \
                     getVector(xval, -yval, badguy_position), getVector(-xval, -yval, badguy_position)]
         toCaptain = [getVector(xval, yval, captain_position), getVector(-xval, yval, captain_position), \
                      getVector(xval, -yval, captain_position), getVector(-xval, -yval, captain_position)]
         
         #locations that are too far away and duplicates will be weeded out
         for vc in toCaptain:
            if sqrt(vc[0]**2 + vc[1]**2) > distance: continue
            dont_hit_me.add(getSmallestVector(vc))         
         for vc in toBadGuy:
            if sqrt(vc[0]**2 + vc[1]**2) > distance: continue
            hit_me.add(getSmallestVector(vc))


   # remove all the vectors that hit the captain
   final = hit_me - dont_hit_me

   # now we're going to double check and see if we need to reinclude solutions
   for solution in (hit_me & dont_hit_me):

      # if a vector hits both the captain and the guard, see which one it hits first
      frame = (0,0) #current frame that laser is in
      frame_LR_border = (0, dimensions[0]) #left/right borders of current frame
      frame_BT_border = (0, dimensions[1]) #bottom/top borders of current frame
      laser_pos = (captain_position[0]+solution[0], captain_position[1]+solution[1])

      while True:
         #follow the path of the laser. stop when we hit a target. hitting a target is guaranteed.
         # if we wanted to ensure no infinite loops we could instead check the length of the laser
         # but I think it's prettier this way

         # check if the laser has hit either target 
         # if it hit the captain, reject the solution. if it hit the guard, accept.
         if laser_pos == newpos(captain_position, frame):
            break
         if laser_pos == newpos(badguy_position, frame):
            final.add(solution)
            break
         
         #check if we've gone into a new frame
         if laser_pos[0] <= frame_LR_border[0]:
            gap = int ( ceil ( (frame_LR_border[0] - laser_pos[0]) / float(dimensions[0]) )) 
            #out of bounds to the left
            frame = (frame[0] - gap, frame[1])
            frame_LR_border = (frame_LR_border[0] - gap*dimensions[0], frame_LR_border[1] - gap*dimensions[0])
         
         elif laser_pos[0] >= frame_LR_border[1]:
            gap = int ( ceil ( -(frame_LR_border[1] - laser_pos[0]) / float(dimensions[0]) ))
            #out of bounds to the right
            frame = (frame[0] + gap, frame[1])
            frame_LR_border = (frame_LR_border[0] + gap*dimensions[0], frame_LR_border[1] + gap*dimensions[0])
         
         if laser_pos[1] <= frame_BT_border[0]:
            gap = int ( ceil ( (frame_BT_border[0] - laser_pos[1]) / float(dimensions[1]) ))
            #out of bounds to the bottom
            frame = (frame[0], frame[1] - gap)
            frame_BT_border = (frame_BT_border[0] - gap*dimensions[1], frame_BT_border[1] - gap*dimensions[1])
         
         elif laser_pos[1] >= frame_BT_border[1]:
            gap = int ( ceil ( -(frame_BT_border[1] - laser_pos[1]) / float(dimensions[1]) ))
            #out of bounds to the top
            frame = (frame[0], frame[1] + gap)
            frame_BT_border = (frame_BT_border[0] + gap*dimensions[1], frame_BT_border[1] + gap*dimensions[1])

         #check if we hit anybody in this frame
         if laser_pos == newpos(captain_position, frame):
            break
         if laser_pos == newpos(badguy_position, frame):
            final.add(solution)
            break
         
         #update laser
         laser_pos = (laser_pos[0] + solution[0], laser_pos[1] + solution[1])

   if len(final) == 0:
      # if we made it to here without finding any solutions, there are none
      return 0

   final.add(base_solution)
   return len(final)
