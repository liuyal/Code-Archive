LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

LIBRARY WORK;
USE WORK.ALL;

-----------------------------------------------------
--
--  This block will contain a decoder to decode a 4-bit number
--  to a 7-bit vector suitable to drive a HEX dispaly
--
--  It is a purely combinational block (think Pattern 1) and
--  is similar to a block you designed in Lab 1.
--
--------------------------------------------------------

ENTITY digit7seg IS
	PORT(
          digit : IN  std_LOGIC_VECTOR(3 DOWNTO 0);  -- number 0 to 0xF
          seg7 : OUT STD_LOGIC_VECTOR(6 DOWNTO 0)  -- one per segment
	);
END;


ARCHITECTURE behavioral OF digit7seg IS
BEGIN

	WITH digit SELECT
		seg7 <= "1000000" WHEN "0000",
				"1111001" WHEN "0001",
				"0100100" WHEN "0010",
				"0110000" WHEN "0011",
				
				"0011001" WHEN "0100",
				"0010010" WHEN "0101",
				"0000010" WHEN "0110",
				"1111000" WHEN "0111",
				
				"0000000" WHEN "1000",
				"0011000" WHEN "1001",
				"0001000" WHEN "1010",
				"0000011" WHEN "1011",
				
				"0100111" WHEN "1100",
				"0100001" WHEN "1101",
				"0000110" WHEN "1110",
				"0001110" WHEN "1111",
				"1111111" WHEN Others;

END;
