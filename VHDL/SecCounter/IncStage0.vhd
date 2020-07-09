LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;


ENTITY IncStage0 IS

PORT (
			X0: IN std_logic ;
			Cout, S0 : OUT std_logic
	
);

END ENTITY IncStage0;


ARCHITECTURE Behaviour OF IncStage0 IS


BEGIN

	S0 <= X0 XOR '1' after 4 ns;
	Cout <= X0;

END Behaviour;
