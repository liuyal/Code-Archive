LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY TenSecDelay IS

PORT (
		TSD_Clk : in std_logic;
		Load : in std_logic;
		
		TC : out std_logic
);
END ENTITY TenSecDelay;

ARCHITECTURE Cond OF TenSecDelay IS

	Signal W : Std_logic_vector (10 downto 0);
	
	Signal Pulse : std_logic;
   
Begin

   
	 
	Seq : Entity work.Sequencer port map (clk_Seq => TSD_Clk,ENB => Load, Q => W );
	
	With W select Pulse <=  '0' when "00000000000",
									'1' when others;
	
	
	TC <= Load OR Pulse;
	

END Cond;





