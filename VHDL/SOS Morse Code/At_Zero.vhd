LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE ieee.std_logic_arith.all ;

ENTITY At_Zero IS

PORT (
		Six_in : in std_logic_vector (5 downto 0);
		Six_out : out std_logic
);

END ENTITY At_Zero;

ARCHITECTURE Behaviour OF At_Zero IS
	
	
BEGIN

		Six_out <= '1' WHEN Six_in = "000000" ELSE '0';
		
END Behaviour;
