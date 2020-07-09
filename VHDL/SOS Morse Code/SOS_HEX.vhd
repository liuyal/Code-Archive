LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY SOS_HEX IS

PORT (
		HEX_clk : in std_logic;
		Hex_out_S : out std_LOGIC_vector (6 downto 0); -- HEX2 and HEX0
		Hex_out_O : out std_LOGIC_vector (6 downto 0) -- HEX1

);
END ENTITY SOS_HEX;

ARCHITECTURE Behaviour OF SOS_HEX IS

	Signal  X, Z : std_LOGIC_vector (6 downto 0);
	Signal A, B : std_LOGIC_vector (3 downto 0);
	
BEGIN
	
	A <= "0101" when rising_edge (HEX_clk);
	B <= "0000" when rising_edge (HEX_clk);

	Decode1: entity work.SegDecoder Port Map (D => A, Y => X);
	
	Decode2: entity work.SegDecoder Port Map (D => B, Y => Z);

	Hex_out_S <= X;
	
	Hex_out_O <= Z;
	
END Behaviour;

