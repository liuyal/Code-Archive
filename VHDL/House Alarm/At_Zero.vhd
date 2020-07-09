LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE ieee.std_logic_arith.all ;

ENTITY At_Zero IS

PORT (
		Port_in : in std_logic_vector (6 downto 0);
		Port_out : out std_logic
);

END ENTITY At_Zero;

ARCHITECTURE Behaviour OF At_Zero IS
	
	
BEGIN

		Port_out <= '1' WHEN Port_in = "0000000" ELSE '0';
		
END Behaviour;
