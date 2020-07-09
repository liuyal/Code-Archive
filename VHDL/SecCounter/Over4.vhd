LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE ieee.std_logic_arith.all;

ENTITY Over4 IS

PORT (
		Four_in : in std_logic_vector (3 downto 0);
		Four_out : out std_logic
);

END ENTITY Over4;

ARCHITECTURE Behaviour OF Over4 IS

	Signal w0,w1,w2,w3: std_logic;
	
	Signal B : std_logic_vector (3 downto 0);
	
BEGIN
		B(3) <= '0'; 
		B(2) <= '1';
		B(1) <= '0'; 
		B(0) <= '0';
		
		Four_out <= '1' WHEN Four_in > B ELSE '0';
		
END Behaviour;






