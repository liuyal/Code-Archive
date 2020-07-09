LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY Inc19 IS

PORT (
			input  : in std_logic_vector(18 downto 0) ;
			carry :  out std_logic;
			output : out std_logic_vector (18 downto 0)
);
END ENTITY Inc19;

ARCHITECTURE Behaviour OF Inc19 IS

	Signal A : unsigned(18 downto 0);

	Signal WireA : std_logic;
	Signal WireB : std_logic;
	Signal WireC : std_logic;
	Signal WireD : std_logic;
	Signal WireE : std_logic;
	
	Signal bit_19 : std_logic_vector (18 downto 2);
	Signal one : std_logic_vector(1 downto 0);
	
BEGIN

	one <= "01";
	bit_19 <= (others => '0');
	
	A <= unsigned(input)+ (unsigned(bit_19) & unsigned(one));
	
	output <= std_logic_vector(A(18 downto 0));
	
	
END Behaviour;





