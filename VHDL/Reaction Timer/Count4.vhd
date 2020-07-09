LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.numeric_std.all;

ENTITY Count4 IS
PORT (
		D : in std_LOGIC_vector (3 downto 0);
		clk_in_count4 : in std_logic;
		enb : in std_logic;
		Loads : in std_logic;
		Q: out std_LOGIC_vector (3 downto 0)
		
);
END ENTITY Count4;

ARCHITECTURE Behaviour OF Count4 IS

	Signal MO_0,MO_1,MO_2, MO_3 : std_logic;

	Signal A,B,C,E : std_LOGIC;
	
	Signal ANDA, ANDB, ANDC, ANDD : std_LOGIC;
	
	Signal y : std_LOGIC_vector (3 downto 0);

Begin
	
	
	A <= Enb XOR y(0);
	MO_0 <= D(0) When Loads = '1' Else A;
	y(0) <= MO_0 when rising_edge(clk_in_count4);

	ANDA <= Enb AND y(0);
	
	B <= y(1) XOR ANDA;
	MO_1 <= D(1) When (Loads = '1') Else B;
	y(1) <= MO_1 when rising_edge(clk_in_count4);
	
	ANDB <= ANDA AND y(1);
	
	C <= y(2) XOR ANDB;
	MO_2 <= D(2) When (Loads = '1') Else C;
	y(2) <= MO_2 when rising_edge(clk_in_count4);
	
	ANDC <= ANDB AND y(2);
	
	E <= y(3) XOR ANDC;
	MO_3 <= D(3) When (Loads = '1') Else E;
	y(3) <= MO_3 when rising_edge(clk_in_count4);
	
	Q <= Y;


END Behaviour;
