LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY System IS

PORT (
		ARM : in std_logic;
		ARM2 : in std_logic;
		ARM2_ENB : in std_logic;
		Clock : in std_logic;
		Doors : in std_logic_vector(3 downto 0);
		

		Ready : out std_logic;
		SysArmed : out std_logic;
		AlarmOn : out std_logic;
		Hold_out : out std_logic;
		Delay_arm_out : out std_logic;
		Delay_Signal_out : out std_logic
);
END ENTITY System;



--*******************************************************************************************
-- BASIC
--*******************************************************************************************



ARCHITECTURE Basic OF System IS
	
	Type StateName Is (UnArmed, Armed , Hold , Alarm_Triggerd);
	Signal PreSt, NextSt : StateName;
	
	Signal Detect_Doors : std_logic;
	Signal Detect_Ready : std_logic;
	Signal Detect_Ready_ARM : std_logic;

Begin 
  
  With Doors select	Detect_Doors <= 
					'0' when "0000",
					'1' when Others;
					
	Detect_Ready_ARM <= '1' when (Detect_Ready And ARM) = '1' else '0';
	
	PreSt <= NextSt when rising_edge (clock);
	
	
	
	
	NextSt <= Unarmed when ( Prest = Alarm_Triggerd And (ARM = '0'))  OR
				
				( Prest = Armed And (ARM = '0') AND (Detect_Doors = '0') ) else
			  
	
	
				 Armed when (Prest = Unarmed and (Detect_Doors = '0') and (ARM = '0') ) else
				 
				 
				 
				 Hold when (Prest = Armed AND (Detect_Doors = '0') AND (ARM ='1')) OR 
				 
				 (Prest = Hold AND (Detect_Doors = '0') AND ARM = '1' ) else   
				 
				 
				 
				 Alarm_Triggerd when (Prest = Hold and Detect_Doors = '1' and ARM = '1' ) OR
				 
				 (Prest = Alarm_Triggerd And (ARM = '1') And (Detect_Doors = '1')) else
				 
				 
				 Unarmed;
				 
				 
	Hold_out <= '1' when PreSt = Hold else '0';			 
	
	SysArmed <= '1' when PreSt = Armed else '0';
	
	AlarmOn <= '1' when PreSt = Alarm_Triggerd else '0';
		
	Detect_Ready <= '1' When Doors = "0000" else '0';
	
	Ready <= Detect_Ready;
	
	
End Basic;







--*******************************************************************************************
-- DELAYS
--*******************************************************************************************



ARCHITECTURE Delays OF System IS
	
	Type StateName Is (UnArmed, Delay, Armed, Delay_arm, Hold, Alarm_Triggerd);
	Signal Prest, NextSt : StateName;
	
	Signal Detect_Doors : std_logic;
	Signal Detect_Ready : std_logic;
	Signal Detect_Ready_ARM : std_logic;
	Signal Delay_signal : std_logic;
	
	Signal ENB : std_logic;


Begin 

	ENB <= Arm2 when arm2_ENB = '1' else '1';
		
  TenSecD : Entity work.TenSecDelay port map (TSD_Clk => Clock, Load => not ARM, TC => Delay_signal);	
  
  With Doors select	Detect_Doors <= 
					'0' when "0000", -- closed
					'1' when Others; -- open
					
	--Detect_Ready_ARM <= '1' when (Detect_Ready And ARM) = '1' else '0';
	
	PreSt <= NextSt when rising_edge (clock);
	
	
	NextSt <= Unarmed when ( Prest = Alarm_Triggerd And (ENB = '0')) OR 
									
									(Prest = Delay_arm  and ENB = '0') else
			  
			  
				 Delay when (Prest = Unarmed and Detect_Doors = '1' and Arm = '0') OR 
				             (Prest = Delay and Delay_signal = '1' and Detect_Doors = '1')else
	
	
	
				 Armed when (Prest = Delay and (Detect_Doors = '0') and Arm = '1')  else  
				 
				 
				 Hold when (Prest = Armed ) OR 
				 (Prest = Hold AND (Detect_Doors = '0') AND ARM = '1' ) else     
				 
				 
				 
				 Delay_arm when ( PreSt = Hold and Detect_Doors = '1' ) OR
				 (Prest = Delay_arm and Delay_signal = '1')else
				 
				 
				 Alarm_Triggerd when (Prest = Delay  and Delay_signal = '0' and detect_Doors = '1' ) OR
											(Prest = Delay_arm  and Delay_signal = '0' and detect_Doors = '1' ) OR
											(Prest = Alarm_Triggerd And (Detect_Doors = '1')) else 
				 
				 unarmed;
				 
	
	
	
	SysArmed <= '1' when PreSt = Armed else '0';
	
	AlarmOn <= '1' when PreSt = Alarm_Triggerd else '0';
	
	Delay_Signal_out <= '1' when PreSt = Delay  else '0';
	
	Delay_arm_out  <= '1' when Prest = Delay_arm  else '0';
	
	Detect_Ready <= '1' When Doors = "0000" else '0';
	
	Ready <= Detect_Ready;
	
	Hold_out <= '1' when PreSt = Hold else '0';	

End Delays;



