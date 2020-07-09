
LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;


ENTITY IncStage1 IS

PORT (
			Xi,Cin : IN std_logic ;
			Cout, Si : OUT std_logic
		
);

END ENTITY IncStage1;



ARCHITECTURE Behaviour OF IncStage1 IS



BEGIN

	Si <= Xi XOR Cin after 4 ns;
	Cout <= Cin AND Xi after 4 ns;


END Behaviour;
