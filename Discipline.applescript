on block_me(start_time, stop_time, grace_time)
	
	set start_block to date start_time of (current date)
	set stop_block to date stop_time of (current date)
	
	if start_block < stop_block then # everything happens on same day
		
		if (current date) < start_block then return
		if (current date) + grace_time > stop_block then return
		
	else # block crosses midnight
		
		if (current date) ≥ start_block then # we are in the middle of a block that ends tomorrow
			
			set stop_block to date stop_time of ((current date) + days)
			
		else # we did not start a block today
			
			if (current date) + grace_time > stop_block then return
			
		end if
		
		# else, we are in the middle of a block that ends today, so business as usual
		
	end if
	
	if isblockactive() then
		display notification "Block already running!" with title "Discipline active"
		return
	end if
	
	show_warning(stop_time, grace_time)
	delay grace_time
	
	set block_duration to getblockduration(stop_block)
	start_selfcontrol(block_duration)
	
end block_me


on getblockduration(stop_block)
	return (stop_block - (current date) + 30) div minutes as number
end getblockduration

on isblockactive()
	try
		do shell script "defaults read org.eyebeam.SelfControl"
	on error
		display notification "Check your SelfControl Installation" with title "Couldn't read defaults"
	end try
	
	set far_future to "4001-01-01 00:00:00 +0000" #used by BlockStartedDate when inactive
	try
		do shell script "defaults read org.eyebeam.SelfControl | grep " & quoted form of far_future
		return false
	on error
		try
			do shell script "defaults read org.eyebeam.SelfControl | grep BlockStartedDate"
			return true
		on error
			return false
		end try
	end try
end isblockactive

on start_selfcontrol(block_duration)
	set my_id to do shell script "id -u $(whoami)" #get my (non-root) id
	
	set my_pw to do shell script "security find-generic-password -wl \"Applescript\""
	
	try
		do shell script "defaults write org.eyebeam.SelfControl BlockDuration -int " & block_duration
		-- do shell script "defaults write org.eyebeam.SelfControl BlockStartedDate -date \"$(date)\""
		
		do shell script "/Applications/SelfControl.app/Contents/MacOS/org.eyebeam.SelfControl " & my_id & " --install" password my_pw with administrator privileges
		-- tell application "SelfControl" to activate
		
	on error
		display notification "Could not start block!" with title "Error"
		return
	end try
end start_selfcontrol


on show_warning(stop_time, grace_time)
	display notification "Start working in " & write_time(grace_time) & "!" with title "Discipline until " & stop_time
end show_warning


on write_time(secs)
	
	set mins to secs div 60
	set rem_secs to secs mod 60
	
	if mins = 0 then
		if secs = 1 then return "1 second"
		return secs & " seconds"
	end if
	
	set timestamp to mins & " minute"
	if mins > 1 then set timestamp to timestamp & "s"
	
	if rem_secs = 0 then return timestamp
	if rem_secs = 1 then return timestamp & ", 1 second"
	return timestamp & ", " & rem_secs & " seconds"
	
end write_time
