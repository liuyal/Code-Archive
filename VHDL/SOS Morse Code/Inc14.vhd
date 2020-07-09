LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY Inc14 IS

PORT (
			input  : in std_logic_vector(13 downto 0) ;
			carry :  out std_logic;
			output : out std_logic_vector (13 downto 0)
);
END ENTITY Inc14;

ARCHITECTURE Behaviour OF Inc14 IS

	Signal A : unsigned(13 downto 0);

	Signal WireA : std_logic;
	Signal WireB : std_logic;
	Signal WireC : std_logic;
	Signal WireD : std_logic;
	Signal WireE : std_logic;
	
	Signal bit_14 : std_logic_vector (13 downto 2);
	Signal one : std_logic_vector(1 downto 0);
	
BEGIN

	one <= "01";
	bit_14 <= (others => '0');
	
	A <= unsigned(input)+ (unsigned(bit_14) & unsigned(one));
	
	output <= std_logic_vector(A(13 downto 0));
	
	
END Behaviour;






