LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY SegDecoder IS

PORT (
		D : IN std_LOGIC_vector(3 DOWNTO 0);
		Z : OUT std_LOGIC_vector (6 DOWNTO 0)
);

END ENTITY SegDecoder;

ARCHITECTURE behaviour OF SegDecoder IS
BEGIN

	WITH D SELECT
		Z <=  "1000000" WHEN "0000", -- 0
				"1111001" WHEN "0001", -- 1 
				"0100100" WHEN "0010", -- 2
				"0110000" WHEN "0011", -- 3
				
				"0011001" WHEN "0100", -- 4
				"0010010" WHEN "0101", -- 5
				"0000010" WHEN "0110", -- 6
				"1111000" WHEN "0111", -- 7
				
				"0000000" WHEN "1000", -- 8
				"0011000" WHEN "1001", -- 9
				"0001000" WHEN "1010", -- A
				"0000011" WHEN "1011", -- B
				
				"0100111" WHEN "1100", -- C
				"0100001" WHEN "1101", -- D
				"0000110" WHEN "1110", -- E
				"0001110" WHEN "1111", -- F
				"1111111" WHEN Others; -- NONE


END ARCHITECTURE behaviour;





