Κώδικας για τις κάμερες canon a3300  και χρήση του 
[7] https://www.youtube.com/watch?v=vYIL-p9ET4k 

--auto_on.lua

--[[
@title AutoStart
@chdk_version 1.3

@param step Zoom Position (step)
@default step 0
@range step 0 12

--]]

sleep(1000)
set_console_layout(0, 1, 48, 16)

if autostarted() then
print("autostarting")
sleep(2000)
end

if ( get_mode() == false ) then -- switch to shooting mode
set_record(1)
while ( get_mode() == false) do sleep(100) end
sleep(1000)
end

set_zoom(step)
print("zoom step="..step)
sleep(1000)
print("autostart complete")
exit_alt()
sleep(500)

Αυτό το σκριπτακι είναι μονο για canon που υποστηρίζουν chdk .

οδηγίες εγκατάστασης 
καλό είναι όταν γίνουν τα παρακάτω και δούμε ότι δουλεύει μια sd card να γίνει και σε 5 με 6 ακόμα clone sd card γιατί είναι λίγο ταλαιπωρία να σεταριστεί εντάξει.
1 format sd card fat 32 ,copy paste a3300 -c version(οι συγκεκριμένες κάμερες )
2 copy auto_zoom.lua 
3 hardware unlock sd card  case put it on camera power on go to Menu - > Tools - > go down an update firmware
4 press alt key 
5 miscellaneus stuff-> sd card ->make card bootable 
6 hardware put out the sd card from the camera  lock sd card case put it back
7 go to chdk menu script , load scricpt from auto_on.lua
8 set autostart on  script 
- remote with usb signal parameters . 
 1 chdk setting -> enable remot dot -> one push -> quick capture

2 also there u can set grid and cross dot  on liveview

3 use a usb-hub (not all are suitable for this ) to capture with both camera



