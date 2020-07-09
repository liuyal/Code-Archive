LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
Use ieee.numeric_std.all;

LIBRARY WORK;
USE WORK.ALL;

ENTITY BCD12 IS
PORT (
	BCD_in : in std_logic_vector  (11 downto 0);
	Bout : out std_logic_vector  (15 downto 0)
);
END ENTITY BCD12;

ARCHITECTURE Behaviour OF BCD12 IS
	
	signal A4, B4, C4, D4 : unsigned (3 downto 0);
	signal unsignB : unsigned (15 downto 0);
	
BEGIN

	A4 <= to_unsigned(to_integer(unsigned(BCD_in))/1000 mod 10,A4'length);
	B4 <= to_unsigned(to_integer(unsigned(BCD_in))/100 mod 10, B4'length);
	C4 <= to_unsigned(to_integer(unsigned(BCD_in))/10 mod 10, C4'length);
	D4 <= to_unsigned(to_integer(unsigned(BCD_in)) mod 10, D4'length);

	unsignB <= A4 & B4 & C4 & D4;

	Bout <= std_logic_vector(unsignB);

END ARCHITECTURE Behaviour;
