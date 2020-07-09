LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY Inc6 IS

PORT (
			input  : in std_logic_vector(5 downto 0) ;
			carry :  out std_logic;
			output : out std_logic_vector (5 downto 0)
);
END ENTITY Inc6;

ARCHITECTURE Behaviour OF Inc6 IS

	Signal A : unsigned(5 downto 0);

	Signal WireA : std_logic;
	Signal WireB : std_logic;
	Signal WireC : std_logic;
	Signal WireD : std_logic;
	Signal WireE : std_logic;

BEGIN
	
	A <= unsigned(input)+ "000001";
	
	output <= std_logic_vector(A);
	
	
	--obj0: ENTITY work.IncStage0 Port Map (X0 => input(0), Cout => WireA, S0 => output(0));
	--obj1: ENTITY work.IncStage1 Port Map (Xi => input(1), Cin => WireA, Cout => WireB, Si => output(1));
	--obj2: ENTITY work.IncStage1 Port Map (Xi => input(2), Cin => WireB, Cout => WireC, Si => output(2));
	--obj3: ENTITY work.IncStage1 Port Map (Xi => input(3), Cin => WireC, Cout => WireD, Si => output(3));
	--obj4: ENTITY work.IncStage1 Port Map (Xi => input(4), Cin => WireD, Cout => WireE, Si => output(4));
	--obj5: ENTITY work.IncStage1 Port Map (Xi => input(5), Cin => WireE, Cout => carry, Si => output(5));

END Behaviour;






