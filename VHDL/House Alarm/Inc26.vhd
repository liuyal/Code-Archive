LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY Inc26 IS

PORT (
			input  : in std_logic_vector(25 downto 0) ;
			carry :  out std_logic;
			output : out std_logic_vector (25 downto 0)
);
END ENTITY Inc26;

ARCHITECTURE Behaviour OF Inc26 IS

	Signal A : unsigned(25 downto 0);

	Signal WireA : std_logic;
	Signal WireB : std_logic;
	Signal WireC : std_logic;
	Signal WireD : std_logic;
	Signal WireE : std_logic;
	
	Signal bit_26 : std_logic_vector (25 downto 2);
	Signal one : std_logic_vector(1 downto 0);
	
BEGIN

	one <= "01";
	bit_26 <= (others => '0');
	
	A <= unsigned(input)+ (unsigned(bit_26) & unsigned(one));
	
	output <= std_logic_vector(A(25 downto 0));
	
	
END Behaviour;





