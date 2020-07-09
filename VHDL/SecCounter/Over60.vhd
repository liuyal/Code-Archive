LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE ieee.std_logic_arith.all ;

ENTITY Over60 IS

PORT (
		A : in std_logic_vector (5 downto 0);
		Z : out std_logic
);

END ENTITY Over60;

ARCHITECTURE Behaviour OF Over60 IS

		--Signal w0,w1,w2,w3,w4,w5 : std_logic;
		--Signal y1,y2,y3 : std_logic;
		Signal B : std_logic_vector (5 downto 0);

BEGIN
		B(5) <= '1'; B(4) <= '1'; B(3) <= '1'; 
		B(2) <= '1'; B(1) <= '0'; B(0) <= '0';
		
		--w0 <= ((A(5) AND Not B(5))NOR(B(5) AND Not A(5))) OR (A(5) AND Not B(5));
	   --w1 <= ((A(4) AND Not B(4))NOR(B(4) AND Not A(4))) OR (A(4) AND Not B(4));
		--w2 <= ((A(3) AND Not B(3))NOR(B(3) AND Not A(3))) OR (A(3) AND Not B(3));
		--w3 <= ((A(2) AND Not B(2))NOR(B(2) AND Not A(2))) OR (A(2) AND Not B(2));
		--w4 <= ((A(1) AND Not B(1))NOR(B(1) AND Not A(1))) OR (A(1) AND Not B(1)); 
		--w5 <= ((A(0) AND Not B(0))NOR(B(0) AND Not A(0))) OR (A(0) AND Not B(0));
		
		--y1 <= w0 AND w1 AND w2; 
		--y2 <= w3 AND w4 AND w5;
		
		
		
		Z <= '1' WHEN A > B ELSE '0';

END Behaviour;








