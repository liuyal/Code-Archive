LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE ieee.std_logic_arith.all ;

ENTITY Detect_500K IS

PORT (
		D : in std_logic_vector (18 downto 0);
		
		Y : out std_logic
);

END ENTITY Detect_500K;

ARCHITECTURE Behaviour OF Detect_500K IS
	
	
BEGIN

		--Y <= '1' WHEN (D < "0111101000010010000") ELSE '0' When D > "0111101000010010000";
		
		Y <= '1' When D = "1111010000100100000";
		
		
END Behaviour;
