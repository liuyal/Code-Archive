LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;

ENTITY JamesBond IS

PORT (
		Go : in std_logic;
		digit : in std_logic_vector (2 downto 0);
		JB_clk : std_logic;
		
		S0 : out std_logic;
		S1 : out std_logic;
		S2 : out std_logic;
		
		GotCode : out std_logic
);
END ENTITY JamesBond;

ARCHITECTURE Cond OF JamesBond IS

	Type StateName Is (Reset,Code1,Code2,Code3);
	Signal PreSt, NextSt : StateName;

	Signal TenSec : std_logic;
	Signal Correct : std_logic;
	
	Signal GOOD_Seven : std_logic;
	Signal GOOD_Zero : std_logic;
	
Begin 

	TenSecD : Entity work.TenSecDelay port map (TSD_Clk => JB_clk, Load => not Go, TC => TenSec);

	GOOD_Seven <= '1' when digit = "111" and Go = '0' else '0';
	GOOD_Zero <= '1' when digit = "000" and Go = '0' else '0';


	PreSt <= NextSt when rising_edge (Go);
	
	NextSt <= Reset when TenSec = '0' else
	
			


			   Code1 when (Prest = Reset And digit = "000" ) else
				 
				 
				 Code2 when (Prest = Code1 And digit = "000" )  else
				 
				 
				 Code3 when (Prest = Code2 And  digit = "111" )  else

								
								Reset;
				 
				 
		S0 <= '1' when Prest = Reset else '0';
		S1 <= '1' when Prest = Code1 else '0';
		S2 <= '1' when Prest = Code2 else '0';
		
   	GotCode <= '1' when PreSt = Code3 else '0';
	
	
	

End Cond;



